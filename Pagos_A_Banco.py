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

def Pagar_Impuestos(Nombre_Jugador,Monto_A_Pagar_Banco):
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
    cursor.callproc('Pagar_Impuestos', (Nombre_Jugador,Monto_A_Pagar_Banco))
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


def main(Nombre_Jugador, Dinero_Jugador):
    col1_pago_banco, col2_pago_banco, col3_pago_banco, col4_pago_banco, col5_pago_banco, col6_pago_banco = st.columns(6)
    with col1_pago_banco:
        Razon_Para_Pagar = st.selectbox('Razon', ['Carcel', 'Impuestos', 'Fortuna o Arca Comunal'], 0, help = 'Motivo para cobrar del banco')
    with col2_pago_banco:
        if Razon_Para_Pagar == 'Carcel':
            st.write('')
            Monto_A_Pagar_Banco = 50
            if st.button(f'Pagar {Monto_A_Pagar_Banco}', disabled = not Monto_A_Pagar_Banco > 0 or Monto_A_Pagar_Banco > Dinero_Jugador):
                Pagar_Carcel(Nombre_Jugador)
        elif Razon_Para_Pagar == 'Impuestos':
            Monto_A_Pagar_Banco = st.number_input('Cantidad',0,999999,0,100)
        elif Razon_Para_Pagar == 'Fortuna o Arca Comunal':
            Monto_A_Pagar_Banco = st.number_input('Cantidad',0,999999,0,10)

    with col3_pago_banco:
        if Razon_Para_Pagar == 'Impuestos':
            if st.button(f'Pagar {Monto_A_Pagar_Banco}', disabled = not Monto_A_Pagar_Banco > 0 or Monto_A_Pagar_Banco > Dinero_Jugador, key = 'Pagar_impuestos'):
                Pagar_Impuestos(Nombre_Jugador,Monto_A_Pagar_Banco)
        elif Razon_Para_Pagar == 'Fortuna o Arca Comunal':
            if st.button(f'Pagar {Monto_A_Pagar_Banco}', disabled = not Monto_A_Pagar_Banco > 0 or Monto_A_Pagar_Banco > Dinero_Jugador, key = 'Pagar_Fortuna'):
                Pagar_A_Banco(Nombre_Jugador,Monto_A_Pagar_Banco)