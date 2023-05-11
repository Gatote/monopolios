import mysql.connector
import streamlit as st
import time
import pandas as pd

st.set_page_config(
    page_title = 'Monopolios app',
    page_icon = 'src/monopoly_logo.jpg',
    layout = 'wide',
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Establecer una conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database="monopolios"
)

    





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

def Recibir_Dinero_Banco_Vuelta(v1):
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
    cursor.callproc('Recibir_Dinero_Banco_Vuelta', (v1,))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    time.sleep(1)
    st.experimental_rerun()


with st.container():
    st.title('Monopolios')

    recarga=False
    if st.button('Actualizar'):
        recargar=True
        #st.experimental_rerun()


    st.header(body = 'Seleccion de jugador', help = 'Seleccion de jugador')
    datos_jugador = consulta_jugadores()
    nombres_jugador = [jugador[0] for jugador in datos_jugador]
    jugador = st.selectbox('Jugador', nombres_jugador)
    try:
        datos_jugador = consultar_datos_jugador(jugador)[0]
    except:
        datos_jugador = ['','',0,'',''] 

    contraseña = st.text_input('Contraseña', max_chars=50, key='contraseña_acciones', type='password', value='', help='Contraseña para realizar acciones', placeholder="Q7z#n9$8")

    st.header('Datos del jugador', help = 'Datos generales del jugador')
    st.write(f'Dinero: {datos_jugador[2]}')
    
    st.write(f'Pasiva: {datos_jugador[3]}')

    restante = False
    if datos_jugador[4] != 0:
        st.write(f'Turnos_restantes: {datos_jugador[4]}')
        restante = False
    else:
        st.success(f'Lista para usar!')
        restante = True
        
    if validar_jugador(jugador,contraseña):
        st.title(body = f'Estas jugando como {jugador} ✔')
        st.header(body = 'Pasiva')
        monto_disponible = False

        if st.button('Usar pasiva', disabled = not restante):
            usar_pasiva(jugador,datos_jugador[3])
        if st.button('Tirar dados', disabled = restante):
            tirar_dado(jugador)

        st.header('Gastos')
        st.subheader('Propiedades')
        col1_propiedad,col2_propiedad = st.columns(2)
        with col1_propiedad:
            valor_propiedad = st.number_input(label = 'Costo de propiedad',min_value = 10,  max_value = 999999, value = 10, step = 10, help = 'Total de costo de propiedad', key = 'valorpropiedad')
            if valor_propiedad <= datos_jugador[2]:
                monto_disponible = True
            else:
                monto_disponible = False
        with col2_propiedad:
            if not monto_disponible:
                st.error('No tienes suficiente dinero')
            elif st.button(label = 'Comprar', help = 'Comprar propiedad', disabled = not monto_disponible):
                Comprar_Propiedad(jugador,valor_propiedad)

        st.subheader('Pagos a jugadores')
        col1_pago,col2_pago,col3_pago = st.columns(3)
        with col1_pago:
            valor_pago = st.number_input(label = 'Valor de pago',min_value = 1,  max_value = 999999, value = 1, step = 1, help = 'Total de pago a jugador',key='valorpago')
            if valor_pago <= datos_jugador[2]:
                monto_disponible = True
            else:
                monto_disponible = False
        with col2_pago:
            jugador2 = st.selectbox('Jugador a pagar', nombres_jugador)
        with col3_pago:
            if not monto_disponible:
                st.error('No tienes suficiente dinero')
            elif jugador == jugador2:
                st.warning('No te puedes pagar a ti mismo')
            elif st.button(label = 'Pagar', help = 'Pagar a jugador', disabled = not monto_disponible):
                
                Pagar_A_Jugador(jugador,jugador2,valor_pago)

        st.header('Cobros')
        st.subheader('Banco')
        razon_cobrar = st.selectbox('Razon', ['Vuelta', 'Impuestos'], 0, help = 'Motivo para cobrar del banco')
        #%d %e %f %g %i %u
        if razon_cobrar == 'Vuelta':
            if st.button('Cobrar'):
                Recibir_Dinero_Banco_Vuelta(jugador)
                
        else:
            cantidad_a_recibir_banco = st.number_input('Cantidad recibida',1,999999,5,5)
            if st.button('Cobrar'):
                Recibir_Dinero_Banco(jugador, cantidad_a_recibir_banco, razon_cobrar)
        







    


