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

def consulta_movimientos(limite):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    if limite:
        # Hacer un SELECT
        cursor.execute(f"SELECT accion FROM movimientos ORDER BY tiempo DESC ")
    else:
        # Hacer un SELECT
        cursor.execute(f"SELECT accion FROM movimientos ORDER BY tiempo DESC LIMIT 5")
        
    try:
        # Recuperar los resultados
        resultados = cursor.fetchall()
        
    except:
        resultados='No hay '
    # Cerrar la conexión a la base de datos
    conn.close()
    return resultados
    
def consulta_jugadores(Pasivas_Activas):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    if Pasivas_Activas:
        # Hacer un SELECT
        cursor.execute(f"SELECT nombre, dinero, pasiva, turnos_restantes FROM jugadores")
    else:
        # Hacer un SELECT
        cursor.execute(f"SELECT nombre, dinero FROM jugadores")
        
        
    try:
        # Recuperar los resultados
        resultados = cursor.fetchall()
        
    except:
        resultados='No hay '
    # Cerrar la conexión a la base de datos
    conn.close()
    return resultados

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

def main(Impuestos_Para_Parada_Libre, Acomulado_Parada_Libre, Dinero_Inicio_Personalizado, Dinero_Inicio, Bono_Salida, Pasivas_Activas, Modo_Exponencial, Jugador_Moderador, Multiplicador_Exponencial, tratos_con_propiedades_disponibles):
    with st.sidebar:
        st.title('Monopolios')
        col1_movimientos, col2_movimientos = st.columns(2)
        Ver_Tabla_completa = st.checkbox("Ver tabla completa")
        with col1_movimientos:
            st.subheader('Movimientos')
        with col2_movimientos:
            st.button('Recargar', key = 'recargar 1')
        mov=pd.DataFrame(consulta_movimientos(Ver_Tabla_completa),columns=['Accion'])
        
        st.table(mov)

        
        col1_jugadores, col2_jugadores = st.columns(2)
        with col1_jugadores:
            st.subheader('Jugadores')
        with col2_jugadores:
            st.button('Recargar', key = 'recargar 2')
        if not Pasivas_Activas:
            jugadores=pd.DataFrame(consulta_jugadores(Pasivas_Activas),columns=('Jugador','Dinero'))
            st.table(jugadores)
        else:
            jugadores=pd.DataFrame(consulta_jugadores(),columns=('Jugador','Dinero','Pasiva','CD'))
            st.table(jugadores)

        st.title("Características del juego")
        variables = ""
        if tratos_con_propiedades_disponibles:
            variables = variables + f"<li>Tratos hasta vender todas las propiedades: Si</li>"
        else:
            variables = variables + f"<li>Tratos hasta vender todas las propiedades: No</li>"
        if Impuestos_Para_Parada_Libre:
            variables = variables + f"<li>Impuestos van a parada libre: Si</li>"
            variables = variables + f"<li>Acomulado en parada libre: {Acomulado_Parada_Libre}</li>"
        else:
            variables = variables + f"<li>Impuestos van a parada libre: No</li>"
        if Dinero_Inicio_Personalizado:
            variables = variables + f"<li>Dinero de inicio personalizado: Si</li>"
            variables = variables + f"<li>Dinero de inicio: ${Dinero_Inicio}</li>"
        else:
            variables = variables + f"<li>Dinero de inicio personalizado: No</li>"
        if Bono_Salida:
            variables = variables + f"<li>Bonus de casilla salida: Si</li>"
        else:
            variables = variables + f"<li>Bonus de casilla salida: No</li>"
        if Pasivas_Activas:
            variables = variables + f"<li>Pasivas activas: Si</li>"
        else:
            variables = variables + f"<li>Pasivas activas: No</li>"
        if Modo_Exponencial:
            variables = variables + f"<li>Modo exponencial activo: Si</li>"
            variables = variables + f"<li>Jugador moderador: {Jugador_Moderador}</li>"
            variables = variables + f"<li>Multiplicador de renta: {Multiplicador_Exponencial}</li>"
        else:
            variables = variables + f"<li>Modo exponencial activo: No</li>"


        # Mostrar una lista de puntos
        st.markdown("""<ul>{}</ul>""".format(variables), unsafe_allow_html=True)
                
        with st.expander('Crear usuario'):
            jugador_nombre = st.text_input('Nombre',"",30,None,"default","Nombre que aparecera dentro del juego",None,None,None,None,placeholder="Shadow")

            jugador_contraseña = st.text_input('Conrtaseña',"",50,None,"password","Contraseña para realizar acciones dentro del juego.",placeholder="Q7z#n9$8")

            jugador_dinero = Dinero_Inicio

            if Pasivas_Activas:
                pasivas = ver_pasivas()
                jugador_pasiva = st.selectbox('Pasiva',pasivas,help='Pasiva con la que se jugará la partida')
            else:
                jugador_pasiva = None


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


                  
        from Nuevo_Juego import main as Nuevo_Juego_Main
        Nuevo_Juego_Main()