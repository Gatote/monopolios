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

    


def Consultar_Propiedades():
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
    cursor.execute("SELECT COUNT(*) FROM propiedades WHERE dueño IS NULL")
    # Cerrar la conexión a la base de datos
    conn.close()
    if cursor.fetchall()[0][0] != 0:
        propiedades_disponibles = True
    else:
        propiedades_disponibles = False
    return propiedades_disponibles
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


def Consultar_Dinero_Neto(Nombre_Jugador):

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
    cursor.execute(f"SELECT FLOOR((SELECT dinero FROM jugadores WHERE nombre = '{Nombre_Jugador}') + (IFNULL((SELECT SUM(hipoteca) FROM propiedades WHERE dueño = '{Nombre_Jugador}' AND hipotecado = 0), 0)) + (SELECT SUM((nivel_renta - 1) * (costo_casa / 2)) FROM propiedades WHERE dueño = '{Nombre_Jugador}' ))")
        
    return cursor.fetchall()[0][0]

def Consular_Variables():

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
    cursor.execute(f"SELECT * FROM variables")
        
    return cursor.fetchall()[0]



with st.container():
    Variables_Juego = Consular_Variables()
    Impuestos_Para_Parada_Libre = bool(Variables_Juego[0])
    Acomulado_Parada_Libre = int(Variables_Juego[1])
    Dinero_Inicio_Personalizado = int(Variables_Juego[2])
    Dinero_Inicio = int(Variables_Juego[3])
    Bono_Salida = bool(Variables_Juego[4])
    Pasivas_Activas = bool(Variables_Juego[5])
    Modo_Exponencial = bool(Variables_Juego[6])
    Jugador_Moderador = str(Variables_Juego[7])
    Multiplicador_Exponencial = int(Variables_Juego[8])
    tratos_con_propiedades_disponibles	 = bool(Variables_Juego[9])
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
    
    datos_jugador = consulta_jugadores()
    if datos_jugador != []:
        with st.expander('Logueo',False):
            st.header(body = 'Seleccion de jugador', help = 'Seleccion de jugador')
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
            if not Credenciales_Validas or contraseña == None or jugador == None:
                st.warning('Escribe credenciales validas')
            else:
                st.success('Ya puedes cerrar esta pestaña')
    else:
        st.warning("No hay jugadores registrados en el juego")
        Credenciales_Validas = False

    if Credenciales_Validas:
        st.title(body = f'Estas jugando como {jugador}')
        col1_cuerpo, col2_cuerpo = st.columns(2)
        with col1_cuerpo:
            st.header('Datos del jugador', help = 'Datos generales del jugador')
            st.write(f'Dinero: ${Dinero_Jugador}')   
            Dinero_Jugador_Neto = Consultar_Dinero_Neto(jugador)
            if Dinero_Jugador_Neto == None:
                Dinero_Jugador_Neto = Dinero_Jugador
            st.write(f'Dinero neto: ${Dinero_Jugador_Neto}')  
            if Pasivas_Activas:
                st.write(f'Pasiva: {Nombre_Pasiva_Jugador}')
                restante = False
                if Enfriamiento_Pasiva_Jugador != 0:
                    st.write(f'Turnos_restantes: {Enfriamiento_Pasiva_Jugador}')
                    restante = False
                else:
                    st.success(f'Lista para usar!')
                    restante = True

        if Pasivas_Activas:      
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
        Pagos_A_Jugadores_main(Nombre_Jugador, Dinero_Jugador, Multiplicador_Exponencial)

        st.subheader('Pagos al banco')
        from Pagos_A_Banco import main as Pagos_A_banco_main
        Pagos_A_banco_main(Nombre_Jugador, Dinero_Jugador, Impuestos_Para_Parada_Libre)
        
        st.header('Cobros')
        st.subheader('Banco')
        from Cobros_A_Banco import main as Cobros_A_banco_main
        Cobros_A_banco_main(Nombre_Jugador, Bono_Salida, Impuestos_Para_Parada_Libre, Acomulado_Parada_Libre)

        st.header('Tratos con jugadores')
        if tratos_con_propiedades_disponibles == False or Consultar_Propiedades() == False:
            from Tratos_Con_Jugadores import main as Tratos_Con_Jugadores_main
            Tratos_Con_Jugadores_main(Nombre_Jugador, Dinero_Jugador)
        elif Consultar_Propiedades():
           st.warning("Todavia hay propiedades disponibles en venta")

        st.header('Abandono o derrota')
        from Abandono_Derrota import main as Abandono_Derrota_main
        Abandono_Derrota_main(Nombre_Jugador)



    # st.write(f"Impuestos van a parada libre: {Impuestos_Para_Parada_Libre}")
    # st.write(f"Acomulado en parada libre: {Acomulado_Parada_Libre}")
    # st.write(f"Dinero de inicio personalizado: {Dinero_Inicio_Personalizado}")
    # st.write(f"Dinero de inicio: {Dinero_Inicio}")
    # st.write(f"Bonus de casilla salida: {Bono_Salida}")
    # st.write(f"Pasivas activas: {Pasivas_Activas}")
    # st.write(f"Modo exponencial activo: {Modo_Exponencial}")
    # st.write(f"Jugador moderador: {Jugador_Moderador}")
    # st.write(f"Multiplicador de renta: {Multiplicador_Exponencial}")
    # st.write(f"Tratos hasta vender todas las propiedades: {tratos_con_propiedades_disponibles	}")
from sidebar import main as menu_main
menu_main(Impuestos_Para_Parada_Libre, Acomulado_Parada_Libre, Dinero_Inicio_Personalizado, Dinero_Inicio, Bono_Salida, Pasivas_Activas, Modo_Exponencial, Jugador_Moderador, Multiplicador_Exponencial, tratos_con_propiedades_disponibles)



    


