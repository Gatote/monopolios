import mysql.connector
import streamlit as st
import time
import pandas as pd

def Pagar_A_Banco(Nombre_Jugador,Monto_A_Pagar_Banco):
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
    cursor.callproc('Pagar_A_Banco', (Nombre_Jugador,Monto_A_Pagar_Banco))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def Pagar_Impuestos(Nombre_Jugador,Monto_A_Pagar_Banco, Habilitar_Para_Libre):
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
    cursor.callproc('Pagar_Impuestos', (Nombre_Jugador, Monto_A_Pagar_Banco, Habilitar_Para_Libre))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def Pagar_Carcel(Nombre_Jugador):
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
    cursor.callproc('Pagar_carcel', (Nombre_Jugador,))
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

def Consultar_propiedades_Propias(Nombre_Jugador):
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
    cursor.execute(f"SELECT nombre, color FROM propiedades where dueño = '{Nombre_Jugador}' AND hipotecado = 0 AND color <> 'Servicio' AND color <> 'Negro'")
        
    # Recuperar los nombres y los emojis de los colores de las propiedades disponibles como una lista de tuplas
    propiedades_disponibles = []
    for nombre, color in cursor.fetchall():
        emoji_color = colores_emoji[color]
        propiedades_disponibles.append((nombre, emoji_color))

    # Cerrar la conexión a la base de datos
    conn.close()

    return propiedades_disponibles

def Consultar_Precio_Casa(Nombre_Propiedad):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )   
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT que incluya la columna 'color'
    cursor.execute(f"SELECT costo_casa FROM propiedades WHERE nombre = '{Nombre_Propiedad}'")

    try:
        res = cursor.fetchall()[0][0]
    except:
        res = 0
    # Cerrar la conexión a la base de datos
    conn.close()
    return res

def Comprar_Casa(Nombre_Propiedad):
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
    cursor.callproc('Comprar_Casa', (Nombre_Propiedad,))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def main(Nombre_Jugador, Dinero_Jugador, Impuestos_Para_Parada_Libre):
    col1_pago_banco, col2_pago_banco, col3_pago_banco, col4_pago_banco, col5_pago_banco, col6_pago_banco = st.columns(6)
    with col1_pago_banco:
        Razon_Para_Pagar = st.selectbox('Razon', ['Carcel', 'Impuestos', 'Fortuna o Arca Comunal', 'Comprar casa'], 0, help = 'Motivo para cobrar del banco')
    with col2_pago_banco:
        if Razon_Para_Pagar == 'Carcel':
            st.write('')
            Monto_A_Pagar_Banco = 50
            if st.button(f'Pagar ${Monto_A_Pagar_Banco}', disabled = not Monto_A_Pagar_Banco > 0 or Monto_A_Pagar_Banco > Dinero_Jugador):
                Pagar_Carcel(Nombre_Jugador)
        elif Razon_Para_Pagar == 'Impuestos':
            Monto_A_Pagar_Banco = st.number_input('Cantidad',0,200,0,100)
        elif Razon_Para_Pagar == 'Fortuna o Arca Comunal':
            Monto_A_Pagar_Banco = st.number_input('Cantidad',0,999999,0,10)
        elif Razon_Para_Pagar == 'Comprar casa':
            propiedades_propias = Consultar_propiedades_Propias(Nombre_Jugador)
            if propiedades_propias != []: 
                opciones = [f"{nombre} {emoji}" for nombre, emoji in propiedades_propias]
                Propiedad_Seleccionada = st.selectbox('Propiedad', opciones)
                emojis = list(colores_emoji.values())
                for i in emojis:
                        Propiedad_Seleccionada = Propiedad_Seleccionada.replace(f" {i}","")
            else:
                st.error('No tienes propiedades disponibles para construir')
                Propiedad_Seleccionada = None

    with col3_pago_banco:
        if Razon_Para_Pagar == 'Impuestos':
            if st.button(f'Pagar ${Monto_A_Pagar_Banco}', disabled = not Monto_A_Pagar_Banco > 0 or Monto_A_Pagar_Banco > Dinero_Jugador, key = 'Pagar_impuestos'):
                Pagar_Impuestos(Nombre_Jugador, Monto_A_Pagar_Banco, Impuestos_Para_Parada_Libre)
        elif Razon_Para_Pagar == 'Fortuna o Arca Comunal':
            if st.button(f'Pagar ${Monto_A_Pagar_Banco}', disabled = not Monto_A_Pagar_Banco > 0 or Monto_A_Pagar_Banco > Dinero_Jugador, key = 'Pagar_Fortuna'):
                Pagar_A_Banco(Nombre_Jugador,Monto_A_Pagar_Banco)
        elif Razon_Para_Pagar == 'Comprar casa':
            if Propiedad_Seleccionada != None:
                Monto_A_Pagar_Banco = Consultar_Precio_Casa(Propiedad_Seleccionada)
                if Monto_A_Pagar_Banco == None:
                    st.error('No puedes contruir en esta propiedad')
                else:
                    if st.button(f'Pagar ${Monto_A_Pagar_Banco}', disabled = Monto_A_Pagar_Banco > Dinero_Jugador or Monto_A_Pagar_Banco == 0, key = 'Pagar_Casa'):
                        Comprar_Casa(Propiedad_Seleccionada)
