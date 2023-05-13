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
    cursor.execute(f"SELECT nombre FROM jugadores where nombre <> '{Nombre_Jugador}'")
        
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

def main(Nombre_Jugador,Dinero_Jugador):
    col1_pago,col2_pago,col3_pago = st.columns(3)
    with col1_pago:
        jugador2 = st.selectbox('Jugador a pagar', Otros_Jugadores(Nombre_Jugador))
    with col2_pago:
        valor_pago = st.number_input(label = 'Valor de pago',min_value = 0,  max_value = 999999, value = 0, step = 50, help = 'Total de pago a jugador',key='valorpago')
    with col3_pago:
        if st.button(label = f'Pagar {valor_pago} a {jugador2}', help = 'Pagar a jugador', disabled = Dinero_Jugador < valor_pago):
            
            Pagar_A_Jugador(Nombre_Jugador,jugador2,valor_pago)