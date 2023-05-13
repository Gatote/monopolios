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


def main(Nombre_Jugador):
    #%d %e %f %g %i %u
    col1_cobro_banco, col2_cobro_banco, col3_cobro_banco, a2, a3, a4 = st.columns(6)
    with col1_cobro_banco:
        razon_cobrar = st.selectbox('Razon', ['Vuelta', 'Impuestos', 'Vuelta doble!'], 0, help = 'Motivo para cobrar del banco')
            
    with col2_cobro_banco:  
        if razon_cobrar == 'Vuelta':
            if st.button('Cobrar', key = 'Cobrar_Vuelta'):
                Recibir_Dinero_Vuelta(Nombre_Jugador)
        elif razon_cobrar == 'Vuelta doble!':
            if st.button('Cobrar', key = 'Cobrar_Vuelta'):
                Recibir_Dinero_Vuelta_Doble(Nombre_Jugador)
        if razon_cobrar == 'Impuestos':
            cantidad_a_recibir_banco = st.number_input('Cantidad recibida',0,999999,0,5)

    with col3_cobro_banco:
        if razon_cobrar == 'Impuestos':
            if st.button('Cobrar', key = 'Cobrar_Dinero', disabled = cantidad_a_recibir_banco == 0 or cantidad_a_recibir_banco > 999999):
                Recibir_Dinero_Banco(Nombre_Jugador, cantidad_a_recibir_banco, razon_cobrar)
    