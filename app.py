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
    cursor.execute(f"SELECT * FROM jugadores WHERE nombre = '{nombre}' AND contraseña = '{contraseña}' AND activo = 1")
        
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






with st.container():
    st.title('Monopolios')

    with st.expander('Pasivas'):
            df = pd.read_csv('pasivas.csv')
            #cambiar indice
            df = df.set_index('nombre')
            # Cambiar el nombre de las columnas
            df = df.rename(columns={'nombre': 'Pasiva', 'descripcion': 'Descripcion', 'enfriamiento': 'Enfriamiento', 'extras': 'Extras'})

            st.table(df)

    # recarga=False
    # if st.button('Actualizar'):
    #     recargar=True
    #     #st.experimental_rerun()

    jugador,contraseña = '',''
    #ocultar_jugadores = st.checkbox('Ocultar otros jugadores',False,'Ocultar_jugadores','Limpiar pantalla ocultando otros jugadores')
    with st.expander('Logueo',False):
        st.header(body = 'Seleccion de jugador', help = 'Seleccion de jugador')
        datos_jugador = consulta_jugadores()
        nombres_jugador = [jugador[0] for jugador in datos_jugador]
        jugador = st.selectbox('Jugador', nombres_jugador)
        try:
            datos_jugador = consultar_datos_jugador(jugador)[0]
        except:
            datos_jugador = ['','',0,'',''] 
        Nombre_Jugador = datos_jugador[0]
        Dinero_Jugador = datos_jugador[2]
        Nombre_Pasiva_Jugador = datos_jugador[3]
        Enfriamiento_Pasiva_Jugador = datos_jugador[4]

        contraseña = st.text_input('Contraseña', max_chars=50, key='contraseña_acciones', type='password', value='', help='Contraseña para realizar acciones', placeholder="Q7z#n9$8")
        Credenciales_Validas = validar_jugador(jugador,contraseña)
        if not Credenciales_Validas:
            st.warning('Escribe credenciales validas')
        else:
            st.success('Ya puedes cerrar esta pestaña')

    if Credenciales_Validas:
        st.title(body = f'Estas jugando como {jugador}')
        col1_cuerpo, col2_cuerpo = st.columns(2)
        with col1_cuerpo:
            st.header('Datos del jugador', help = 'Datos generales del jugador')
            st.write(f'Dinero: {Dinero_Jugador}')       
            st.write(f'Pasiva: {Nombre_Pasiva_Jugador}')

            restante = False
            if Enfriamiento_Pasiva_Jugador != 0:
                st.write(f'Turnos_restantes: {Enfriamiento_Pasiva_Jugador}')
                restante = False
            else:
                st.success(f'Lista para usar!')
                restante = True
        with col2_cuerpo:
            st.header(body = 'Pasiva')
            monto_disponible = False
            col1_pasiva, col2_pasiva, col3_pasiva = st.columns(3)
            with col1_pasiva:
                if st.button('Usar pasiva', disabled = not restante):
                    usar_pasiva(jugador,Nombre_Pasiva_Jugador)
            with col2_pasiva:
                if st.button('Tirar dados', disabled = restante):
                    tirar_dado(jugador)
            with col3_pasiva:
                if Enfriamiento_Pasiva_Jugador != 0:
                    st.warning(f'Disponible en {Enfriamiento_Pasiva_Jugador} turnos')

        st.header('Gastos')
        st.subheader('Propiedades')
        from Comprar_Propiedad import main as comprar_propiedad_main
        comprar_propiedad_main(jugador, Dinero_Jugador)

        st.subheader('Pagos a jugadores')
        from Pagos_A_Jugadores import main as Pagos_A_Jugadores_main
        Pagos_A_Jugadores_main(Nombre_Jugador, Dinero_Jugador)

        st.subheader('Pagos al banco')
        from Pagos_A_Banco import main as Pagos_A_banco_main
        Pagos_A_banco_main(Nombre_Jugador, Dinero_Jugador)
        
        st.header('Cobros')
        st.subheader('Banco')
        from Cobros_A_Banco import main as Cobros_A_banco_main
        Cobros_A_banco_main(Nombre_Jugador)

        # st.header('Propiedades')
        # from Propiedades_Propias import main as Propiedades_main
        # Propiedades_main(Nombre_Jugador)

        st.header('Abandono o derrota')
        from Abandono_Derrota import main as Abandono_Derrota_main
        Abandono_Derrota_main(Nombre_Jugador)






    


