import mysql.connector
import streamlit as st
import time
import pandas as pd

def Otros_Jugadores(Nombre_Jugador):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT
    cursor.execute(f"SELECT nombre FROM jugadores where nombre <> '{Nombre_Jugador}' AND activo = 1")
        
    # Obtener todas las filas y agregarlas a una lista
    resultados = []
    for fila in cursor.fetchall():
        resultados.append(fila[0])

    # Cerrar la conexión a la base de datos
    conn.close()

    # Devolver la lista de resultados
    return resultados

    

def Pagar_A_Jugador(v1,v2,v3):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT
    cursor.callproc('Pagar_A_Jugador', (v1,v2,v3))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

# Diccionario que asocia cada nombre de color con el emoji correspondiente
colores_emoji = {
    "Marron": "🟤",
    "Celeste": "🔵",
    "Morado": "🟣",
    "Naranja": "🟠",
    "Rojo": "🔴",
    "Amarillo": "🟡",
    "Verde": "🟢",
    "Azul": "🔵",
    "Negro": "⚫",
    "Servicio": "🔧"
}

def Consultar_Propiedades_No_Propias(Nombre_Jugador):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT
    cursor.execute(f"SELECT nombre, color FROM propiedades where dueño = '{Nombre_Jugador}' AND hipotecado = 0")
        
    # Recuperar los nombres y los emojis de los colores de las propiedades disponibles como una lista de tuplas
    propiedades_disponibles = []
    for nombre, color in cursor.fetchall():
        emoji_color = colores_emoji[color]
        propiedades_disponibles.append((nombre, emoji_color))

    # Cerrar la conexión a la base de datos
    conn.close()

    return propiedades_disponibles

def Consultar_Renta(Nombre_Propiedad):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    try:
        # Llamar al procedimiento almacenado
        cursor.callproc('Consultar_Renta', [Nombre_Propiedad])
        res=[[]]
        if res == [[]]:
            res = [[0]]
        # Obtener el resultado del procedimiento almacenado
        for result in cursor.stored_results():
            res = result.fetchall()
        
        # Confirmar los cambios en la base de datos
        conn.commit()

        return res[0][0]

    except mysql.connector.Error as error:
        print("Error al ejecutar el procedimiento almacenado: {}".format(error))

    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()


def main(Nombre_Jugador,Dinero_Jugador, Multiplicador_Exponencial):
    Otros_Jugadores_Para_Pagar = Otros_Jugadores(Nombre_Jugador)
    if Otros_Jugadores_Para_Pagar == []:
        st.warning("No hay otros jugadores en el juego")
    else:
        jugador2 = st.selectbox('Jugador a pagar', Otros_Jugadores_Para_Pagar)
        
        if jugador2 != None:
            Razon_Pagar_Jugador = st.selectbox("Razon",["Renta", "Fortuna o arca comunal"]) 
            
            
            
            # if Razon_Pagar_Jugador == "Renta":



            if Razon_Pagar_Jugador == "Renta":
                Propiedades_No_Propias = Consultar_Propiedades_No_Propias(jugador2)
                if Propiedades_No_Propias != []: 
                    opciones = [f"{nombre} {emoji}" for nombre, emoji in Propiedades_No_Propias]
                    Propiedad_Seleccionada = st.selectbox('Propiedad', opciones)
                    t_Propiedad_Seleccionada = Propiedad_Seleccionada.split()[-1]
                    #st.write(t_Propiedad_Seleccionada)
                    emojis = list(colores_emoji.values())
                    for i in emojis:
                        Propiedad_Seleccionada = Propiedad_Seleccionada.replace(f" {i}","")
                else:
                    st.error('No tiene propiedades disponibles para cobrar renta')
                    Propiedad_Seleccionada = None
                    t_Propiedad_Seleccionada = ""
                valor_pago = 0
                #st.write(Propiedad_Seleccionada)
                #consultar precio de renta
                Monto_A_Pagar_Jugador = Consultar_Renta(Propiedad_Seleccionada)
                #st.write(t_Propiedad_Seleccionada)
                if t_Propiedad_Seleccionada in ["🔧"]:
                    valor_pago = st.number_input(label = 'Valor de pago',min_value = 0, value = 0, step = (1 * Multiplicador_Exponencial), help = 'Total de pago a jugador',key='valorpago_renta')
                elif t_Propiedad_Seleccionada in ["⚫"]:
                    valor_pago = st.select_slider("Valor de pago",[25,50,100,200], help = 'Total de pago a jugador',key='valorpago_renta', value = 25)
                    #valor_pago = st.number_input(label = 'Valor de pago',min_value = 0, value = 0, step = (25 * Multiplicador_Exponencial), help = 'Total de pago a jugador',key='valorpago_renta')
                    if st.button(f'Pagar ${valor_pago * Multiplicador_Exponencial}', disabled = valor_pago > Dinero_Jugador or valor_pago == 0, key = 'Pagar_Renta'):
                        Pagar_A_Jugador(Nombre_Jugador,jugador2, valor_pago * Multiplicador_Exponencial)

                elif Monto_A_Pagar_Jugador == None or not t_Propiedad_Seleccionada in ["⚫", "🔧"]:
                    if st.button(f'Pagar ${Monto_A_Pagar_Jugador * Multiplicador_Exponencial}', disabled = Monto_A_Pagar_Jugador > Dinero_Jugador or Monto_A_Pagar_Jugador == 0, key = 'Pagar_Renta'):
                        Pagar_A_Jugador(Nombre_Jugador,jugador2,Monto_A_Pagar_Jugador * Multiplicador_Exponencial)

            elif Razon_Pagar_Jugador == "Fortuna o arca comunal":
                valor_pago = st.number_input(label = 'Valor de pago',min_value = 0,  max_value = 999999, value = 0, step = 50, help = 'Total de pago a jugador',key='valorpago')
                if valor_pago > 0:
                    if st.button(f'Pagar ${valor_pago}', disabled = valor_pago > Dinero_Jugador or valor_pago == 0, key = 'Pagar_Casa'):
                        Pagar_A_Jugador(Nombre_Jugador,jugador2,valor_pago * Multiplicador_Exponencial)