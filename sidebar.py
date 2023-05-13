import mysql.connector
import streamlit as st
import pandas as pd
import time

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

def main():
    with st.sidebar:
        st.title('Monopolios')
        col1_movimientos, col2_movimientos = st.columns(2)
        with col1_movimientos:
            st.subheader('Movimientos')
        with col2_movimientos:
            st.button('Recargar', key = 'recargar 1')
        mov=pd.DataFrame(consulta_movimientos(),columns=['Accion'])
        #st.table(mov)
        container = st.container()
        with container:
            st.write(mov.style.set_table_attributes('style="max-height: 500px; overflow-y: auto;"'))
        
        col1_jugadores, col2_jugadores = st.columns(2)
        with col1_jugadores:
            st.subheader('Jugadores')
        with col2_jugadores:
            st.button('Recargar', key = 'recargar 2')
        jugadores=pd.DataFrame(consulta_jugadores(),columns=('Jugador','Dinero','Pasiva','CD'))
        st.table(jugadores)

                
        with st.expander('Crear usuario'):
            jugador_nombre = st.text_input('Nombre',"",30,None,"default","Nombre que aparecera dentro del juego",None,None,None,None,placeholder="Shadow")

            jugador_contraseña = st.text_input('Conrtaseña',"",50,None,"password","Contraseña para realizar acciones dentro del juego.",placeholder="Q7z#n9$8")

            jugador_dinero = st.number_input('Dinero',0,999999,1500,100,help='Cantidad de dinero con la que comenzará el jugador')

            pasivas = ver_pasivas()
            jugador_pasiva = st.selectbox('Pasiva',pasivas,help='Pasiva con la que se jugará la partida')


            if jugador_nombre == None or jugador_contraseña == None:
                st.warning('Establece un nokmbre de jugador y contraseña')
            else:
                if st.button('Registrar jugador'):
                    try:
                        agregar_jugador(jugador_nombre,jugador_contraseña,jugador_dinero,jugador_pasiva)
                        #st.succes(f"El jugador {jugador_nombre} entro al juego")
                        st.success(f'{jugador_nombre} entro al juego!')
                        time.sleep(1)
                        st.experimental_rerun()
                    except:
                        st.warning('Jugador agregado!')
                        time.sleep(1)
                        st.experimental_rerun()


                    
        with st.expander('Desarrollador',expanded=False):
            t_confirmar1=st.text_input('Pass 1',key='txt_reseteo1',type='password')    
            t_confirmar2=st.text_input('Pass 2',key='txt_reseteo2',type='password')
            if st.button('Confirmar',key='btn_resteo'):
                nuevo_juego(t_confirmar1,t_confirmar2)
                st.success("La venta ha sido agregada correctamente")
                time.sleep(1)
                st.experimental_rerun() # actualiza la página