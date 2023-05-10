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

def validar_jugador(nombre, contraseña):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT para buscar al jugador en la tabla de jugadores
    cursor.execute(f"SELECT * FROM jugadores WHERE nombre = '{nombre}' AND contraseña = '{contraseña}'")
        
    # Recuperar el resultado de la consulta
    resultado = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    conn.close()

    # Si la consulta devuelve un resultado, entonces el jugador existe
    if resultado:
        return True
    else:
        return False

   
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
    cursor.execute(f"SELECT nombre,dinero,pasiva,turnos_restantes FROM jugadores")
        
    # # Recuperar los nombres de los jugadores como una lista
    # nombres = [registro[0] for registro in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()

    return cursor.fetchall()

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
    
def consultar_datos_jugador(v1):
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
    cursor.execute(f"SELECT * FROM jugadores where nombre = '{v1}'")
        
    return cursor.fetchall()

def usar_pasiva(v1,v2):
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
    cursor.callproc('Usar_Pasiva', (v1,))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    st.success(f'Usaste {v2}!')
    time.sleep(1)
    st.experimental_rerun()

def Comprar_Propiedad(v1,v2):
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
    cursor.callproc('Comprar_Propiedad', (v1,v2))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()


with st.container():
    st.title('Monopolios')

    if st.button('Actualizar'):
        st.experimental_rerun()

    datos_jugador = consulta_jugadores()
    nombres_jugador = [jugador[0] for jugador in datos_jugador]
    jugador = st.selectbox('Jugador', nombres_jugador)
    try:
        datos_jugador = consultar_datos_jugador(jugador)[0]
    except:
        datos_jugador = ['','',0,'',''] 

    contraseña = st.text_input('Contraseña', max_chars=50, key='contraseña_acciones', type='password', value='', help='Contraseña para realizar acciones', placeholder="Q7z#n9$8")

    
    st.text(f'Dinero: {datos_jugador[2]}')
    
    st.text(f'Pasiva: {datos_jugador[3]}')

    restante = False
    if datos_jugador[4] != 0:
        st.text(f'Turnos_restantes: {datos_jugador[4]}')
        restante = False
    else:
        st.success(f'Lista para usar!')
        restante = True
        
    if validar_jugador(jugador,contraseña):
        monto_disponible = False

        if not jugador==None:
            if st.button('Usar pasiva', disabled = not restante):
                usar_pasiva(jugador,datos_jugador[3])
            if st.button('Tirar dados', disabled = restante):
                tirar_dado(jugador)
            col1_propiedad,col2_propiedad = st.columns(2)

            with col1_propiedad:
                valor_propiedad = st.number_input(label = 'Costo de propiedad',min_value = 0,  max_value = 999999, value = 0, step = 1, help = 'Total de costo de propiedad')
                if valor_propiedad <= datos_jugador[2]:
                    monto_disponible = True
                else:
                    monto_disponible = False
            with col2_propiedad:
                if st.button(label = 'Pagar', help = 'Comprar propiedad', disabled = not monto_disponible):
                    Comprar_Propiedad()







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


