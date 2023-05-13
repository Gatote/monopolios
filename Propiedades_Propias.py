import mysql.connector
import streamlit as st
import time
import pandas as pd

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
    cursor.execute(f"SELECT nombre, color FROM propiedades where dueño = '{Nombre_Jugador}'")
        
    # Recuperar los nombres y los emojis de los colores de las propiedades disponibles como una lista de tuplas
    propiedades_disponibles = []
    for nombre, color in cursor.fetchall():
        emoji_color = colores_emoji[color]
        propiedades_disponibles.append((nombre, emoji_color))

    # Cerrar la conexión a la base de datos
    conn.close()

    return propiedades_disponibles

def Consultar_Casas(Nombre_Propiedad):
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

    res = cursor.fetchall()[0][0]

    # Cerrar la conexión a la base de datos
    conn.close()
    return res

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

    # Hacer un SELECT que incluya la columna 'color'
    cursor.execute(f"SELECT renta, renta_grupo, renta_1, renta_2, renta_3, renta_4, renta_5 FROM propiedades WHERE nombre = '{Nombre_Propiedad}'")

    res = cursor.fetchall()[0][0]

    # Cerrar la conexión a la base de datos
    conn.close()
    return res

def main(Nombre_Jugador):
    propiedades_propias = Consultar_propiedades_Propias(Nombre_Jugador)
    col1_comprar_propiedad, col2_comprar_propiedad, col3_comprar_propiedad, col4_comprar_propiedad, col5_comprar_propiedad = st.columns(5)
    opciones = [f"{nombre} {emoji}" for nombre, emoji in propiedades_propias]
    with col1_comprar_propiedad:
        Propiedad_Seleccionada = st.selectbox('Propiedad', opciones)
    with col2_comprar_propiedad:
        emojis = list(colores_emoji.values())
        for i in emojis:
            Propiedad_Seleccionada = Propiedad_Seleccionada.replace(f" {i}","")
        nivel_renta = Consultar_Casas(Propiedad_Seleccionada)
        if nivel_renta >= 1 and nivel_renta <=4:
            st.write(f'{nivel_renta-1} casas')
        