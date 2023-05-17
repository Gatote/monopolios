import mysql.connector
import streamlit as st
import time
import pandas as pd

def Recibir_Dinero_Vuelta(Nombre_Jugador):
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
    cursor.callproc('Recibir_Dinero_Vuelta', (Nombre_Jugador,))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def Recibir_Dinero_Vuelta_Doble(Nombre_Jugador):
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
    cursor.callproc('Recibir_Dinero_Vuelta_Doble', (Nombre_Jugador,))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def Recibir_Dinero_Banco(v1,v2,v3):
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
    cursor.callproc('Recibir_Dinero_Banco', (v1,v2,v3))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def Vender_Casa(Nombre_Propiedad):
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
    cursor.callproc('Vender_Casa', (Nombre_Propiedad,))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()
    
def Hipotecar_Propiedad(Nombre_Propiedad):
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
    cursor.callproc('Hipotecar_Propiedad', (Nombre_Propiedad,))
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
    cursor.execute(f"SELECT nombre, color FROM propiedades where dueño = '{Nombre_Jugador}' AND hipotecado = 0")
        
    # Recuperar los nombres y los emojis de los colores de las propiedades disponibles como una lista de tuplas
    propiedades_disponibles = []
    for nombre, color in cursor.fetchall():
        emoji_color = colores_emoji[color]
        propiedades_disponibles.append((nombre, emoji_color))

    # Cerrar la conexión a la base de datos
    conn.close()

    return propiedades_disponibles

def Consultar_propiedades_Propias_Para_Hipotecar(Nombre_Jugador):
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
    cursor.execute(f"SELECT nombre, color FROM propiedades where dueño = '{Nombre_Jugador}' AND hipotecado = 0 AND nivel_renta = 1")
        
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

def Consultar_Numero_Casas(Nombre_Propiedad):
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
    cursor.execute(f"SELECT nivel_renta FROM propiedades WHERE nombre = '{Nombre_Propiedad}'")
    try:
        res = cursor.fetchall()[0][0]
    except: 
        res = 0
    # Cerrar la conexión a la base de datos
    conn.close()
    return res

def Consultar_Hipoteca(Nombre_Propiedad):
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
    cursor.execute(f"SELECT hipoteca FROM propiedades WHERE nombre = '{Nombre_Propiedad}'")
    try:
        res = cursor.fetchall()[0][0]
    except:
        res=0
    # Cerrar la conexión a la base de datos
    conn.close()
    return res

def main(Nombre_Jugador, Bono_Salida):
    #%d %e %f %g %i %u
    col1_cobro_banco, col2_cobro_banco, col3_cobro_banco, a2, a3, a4 = st.columns(6)
    with col1_cobro_banco:
        if not Bono_Salida:
            opciones = ['Vuelta', 'Impuestos', 'Vender casa', 'Hipotecar']
        else:
            opciones = ['Vuelta', 'Impuestos', 'Vuelta doble!', 'Vender casa', 'Hipotecar']
        razon_cobrar = st.selectbox('Razon', opciones, 0, help = 'Motivo para cobrar del banco')
            
    with col2_cobro_banco:  
        if razon_cobrar == 'Vuelta':
            if st.button('Cobrar $200', key = 'Cobrar_Vuelta'):
                Recibir_Dinero_Vuelta(Nombre_Jugador)

        elif razon_cobrar == 'Vuelta doble!':
            if st.button('Cobrar $400', key = 'Cobrar_Vuelta'):
                Recibir_Dinero_Vuelta_Doble(Nombre_Jugador)

        elif razon_cobrar == 'Impuestos':
            cantidad_a_recibir_banco = st.number_input('Cantidad recibida',0,999999,0,5)

        elif razon_cobrar == 'Vender casa':
            propiedades_propias = Consultar_propiedades_Propias(Nombre_Jugador)
            
            if propiedades_propias == []:
                st.error('No tienes construcciones en tus propiedades')
            else:
                opciones = [f"{nombre} {emoji}" for nombre, emoji in propiedades_propias]
                Propiedad_Seleccionada = st.selectbox('Propiedad', opciones, key = 'Propiedad_Vender_casa')
                emojis = list(colores_emoji.values())
                for i in emojis:
                    Propiedad_Seleccionada = Propiedad_Seleccionada.replace(f" {i}","")

        elif razon_cobrar == 'Hipotecar':
            propiedades_propias = Consultar_propiedades_Propias_Para_Hipotecar(Nombre_Jugador)
            if propiedades_propias == []:
                st.error('No tienes propiedades disponibles para hipotecar')
            else:
                opciones = [f"{nombre} {emoji}" for nombre, emoji in propiedades_propias]
                Propiedad_Seleccionada = st.selectbox('Propiedad', opciones, key = 'Propiedad_Vender_casa')
                emojis = list(colores_emoji.values())
                for i in emojis:
                    Propiedad_Seleccionada = Propiedad_Seleccionada.replace(f" {i}","")

    with col3_cobro_banco:
        if razon_cobrar == 'Impuestos':
            if st.button(f'Cobrar ${cantidad_a_recibir_banco}', key = 'Cobrar_Dinero', disabled = cantidad_a_recibir_banco == 0 or cantidad_a_recibir_banco > 999999):
                Recibir_Dinero_Banco(Nombre_Jugador, cantidad_a_recibir_banco, razon_cobrar)
        elif razon_cobrar == 'Vender casa':
            try:
                if Consultar_Numero_Casas(Propiedad_Seleccionada) <2:
                    st.warning('No tienes casas en esa propiedad')
                else:
                    if st.button(f'Cobrar ${int(Consultar_Precio_Casa(Propiedad_Seleccionada)/2)}', key = 'Cobro_Casa'):
                        Vender_Casa(Propiedad_Seleccionada)
            except:
                None
        elif razon_cobrar == 'Hipotecar':
            try:
                Dinero_A_Recibir = int(Consultar_Hipoteca(Propiedad_Seleccionada))
                if st.button(f'Cobrar ${Dinero_A_Recibir}', key = 'Cobro_Casa', disabled = Dinero_A_Recibir == 0):
                    Hipotecar_Propiedad(Propiedad_Seleccionada)
            except:
                None