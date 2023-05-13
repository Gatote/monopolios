import mysql.connector
import streamlit as st
import time
import pandas as pd

def Rendirse_Compartir(Nombre_Jugador):
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
    cursor.callproc('Rendirse_Compartir', (Nombre_Jugador,))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def Rendirse_Abandono(Nombre_Jugador):
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
    cursor.callproc('Rendirse_Abandono', (Nombre_Jugador,))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()

def main(Nombre_Jugador):
    accion = st.selectbox('Accion', ['Seleccionar', 'Sin dinero suficiente para pagar', 'Abandonar', 'Abandonar y compartir'])
    if accion == 'Sin dinero suficiente para pagar':
        st.selectbox('Jugador',[])
    elif accion == 'Abandonar':
        st.write('Al confirmar todas tus propiedades se devolveran al banco, incluyendo el dinero')
        if st.button('Confirmar'):
            Rendirse_Abandono(Nombre_Jugador)
    elif accion == 'Abandonar y compartir':
        st.write('Al confirmar darás todo tu dinero, tus propiedades se devolveran al banco y se repartirá al resto de jugadores')
        if st.button('Confirmar'):
            Rendirse_Compartir(Nombre_Jugador)
