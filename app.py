import mysql.connector
import streamlit as st
import time
import pandas as pd

# Establecer una conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database="monopolios"
)

    
def agregar_jugador(v1, v2, v3, v4):
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
    cursor.callproc('crear_jugador', (v1, v2, int(v3), v4))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()


def ver_pasivas():
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    cursor.execute("SELECT nombre FROM pasivas")
    resultados = cursor.fetchall()

    nombres = [resultado[0] for resultado in resultados]

    # Cerrar la conexión a la base de datos
    conn.close()
    return nombres



# Redirigir a la página correspondiente según la opción seleccionada
from sidebar import main as menu_main
menu_main()

   
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
    cursor.execute(f"SELECT nombre FROM jugadores")
        
    # Recuperar los nombres de los jugadores como una lista
    nombres = [registro[0] for registro in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()

    return nombres

def consulta_dinero(vnombre):
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
    cursor.execute(f"SELECT dinero FROM jugadores where nombre='{vnombre}'")
        
    # Recuperar los nombres de los jugadores como una lista
    nombres = [registro[0] for registro in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()
    try:
        return int(nombres[0])
    except IndexError:
        return 0

def tirar_dado(v1):
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
    cursor.callproc('Tirar_Dado', (v1,))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    st.success('Tiraste los dados!')
    time.sleep(1)
    st.experimental_rerun()
    




with st.container():
    st.title('Monopolios')

    col1,col2,col3,col4=st.columns(4)
    with col1:  
        jugador = st.selectbox('Jugador',consulta_jugadores())
    with col2:
        contraseña = st.text_input('Contraseña',max_chars=50,key='contraseña_acciones',type='password',help='Contraseña para realizar acciones',placeholder="Q7z#n9$8")
    with col3:
        st.text_input('Dinero',f'Dinero: {consulta_dinero(jugador)}',disabled=True,help='Referencia a cantidad actual')
    with col4:
        st.write('')
        st.write('')
        if st.button('Tirar dados'):
            tirar_dado(jugador)


    with st.expander('Crear usuario'):
        jugador_nombre = st.text_input('Nombre',"",30,None,"default","Nombre que aparecera dentro del juego",None,None,None,None,placeholder="Shadow")

        jugador_contraseña = st.text_input('Conrtaseña',"",50,None,"password","Contraseña para realizar acciones dentro del juego.",placeholder="Q7z#n9$8")

        jugador_dinero = st.number_input('Dinero',0,999999,1500,100,help='Cantidad de dinero con la que comenzará el jugador')

        pasivas = ver_pasivas()
        jugador_pasiva = st.selectbox('Pasiva',pasivas,help='Pasiva con la que se jugará la partida')



        if st.button('Registrar jugador'):
            try:
                agregar_jugador(jugador_nombre,jugador_contraseña,jugador_dinero,jugador_pasiva)
                st.succes(f"El jugador {jugador_nombre} entro al juego")
                time.sleep(1)
                st.experimental_rerun() # actualiza la página
            except:
                #st.error("Ya existe el jugador")
                st.experimental_rerun() # actualiza la página


