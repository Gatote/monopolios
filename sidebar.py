import mysql.connector
import streamlit as st
import pandas as pd
import time

def consulta_movimientos():
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
    cursor.execute(f"SELECT accion FROM movimientos ORDER BY tiempo DESC")
        
        
    try:
        # Recuperar los resultados
        resultados = cursor.fetchall()
        
    except:
        resultados='No hay '
    # Cerrar la conexión a la base de datos
    conn.close()
    return resultados
    
def consulta_jugadores():
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
    cursor.execute(f"SELECT nombre, dinero, pasiva, turnos_restantes FROM jugadores")
        
        
    try:
        # Recuperar los resultados
        resultados = cursor.fetchall()
        
    except:
        resultados='No hay '
    # Cerrar la conexión a la base de datos
    conn.close()
    return resultados
    
def nuevo_juego(confirmar1, confirmar2):
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
    cursor.callproc('Nuevo_Juego', (confirmar1, confirmar2))
    conn.commit()
    
    #st.write(f"CALL Nuevo_Juego('{confirmar1}','{confirmar2}')")
    # Cerrar la conexión a la base de datos
    conn.close()


def main():
    with st.sidebar:
        st.title('Gato')
        st.subheader('Movimientos')
        mov=pd.DataFrame(consulta_movimientos(),columns=['Accion'])
        st.table(mov)
        
        st.subheader('Jugadores')
        jugadores=pd.DataFrame(consulta_jugadores(),columns=('Jugador','Dinero','Pasiva','CD'))
        st.table(jugadores)

        with st.expander('Reseteo',expanded=False):
            t_confirmar1=st.text_input('Pass 1',key='txt_reseteo1')    
            t_confirmar2=st.text_input('Pass 2',key='txt_reseteo2')
            if st.button('Confirmar',key='btn_resteo'):
                nuevo_juego(t_confirmar1,t_confirmar2)
                st.success("La venta ha sido agregada correctamente")
                time.sleep(1)
                st.experimental_rerun() # actualiza la página