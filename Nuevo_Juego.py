import mysql.connector
import streamlit as st
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

def Crear_Jugador(Nombre_Jugador, Contraseña_Jugador, Dinero, Pasiva):
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
    cursor.callproc('crear_jugador', (Nombre_Jugador, Contraseña_Jugador, Dinero, Pasiva))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

def nuevo_juego(v_impuestos_para_parada_libre, v_dinero_inicio_personalizado, v_dinero_inicio_personalizado_cantidad, v_bono_salida, v_pasivas_activas, v_modo_exponencial, v_jugador_moderador, v_tratos_con_propiedades_disponibles):
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
    cursor.callproc('Nuevo_Juego', (v_impuestos_para_parada_libre, v_dinero_inicio_personalizado, v_dinero_inicio_personalizado_cantidad, v_bono_salida, v_pasivas_activas, v_modo_exponencial, v_jugador_moderador, v_tratos_con_propiedades_disponibles))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()

def main():
    #with st.expander('Nuevo juego',expanded=False):
    with st.expander('Nuevo juego',expanded=True):
        st.title('Reglas del juego')
        Input_Impuestos_Para_Parada_Libre = st.checkbox('Impuestos se van a parada libre', False, None, "Los pagos de las casillas de 'impuesto sobre la renta' y 'impuesto de lujo' se dirigira a la casilla de parada libre")
        Input_Personalizar_Dinero_Inicio = st.checkbox('Personalizar dinero de inicio')
        if Input_Personalizar_Dinero_Inicio:
            Input_Personalizar_Dinero_Inicio_Cantidad = st.number_input("Dinero de inicio", 0, 9999, 1500, 100)
        else:
            Input_Personalizar_Dinero_Inicio_Cantidad = 1500
        # if Input_Impuestos_Para_Parada_Libre:
        #     st.write("Los pagos de las casillas de 'impuesto sobre la renta' y 'impuesto de lujo' se dirigira a la casilla de parada libre ")
        Input_Pasivas_Activas = st.checkbox('Habilitar pasivas')
        Input_Modo_Exponencial = st.checkbox('Habilitar modo exponencial')
        if Input_Modo_Exponencial:
            Input_Jugador_Moderador = st.text_input('Jugador principal', "", 30, help = "Jugador que va a estar aumentando el multiplicador")
            #Input_Jugador_Moderador_contraseña = st.text_input('Contraseña', "", 50, type = "password")
            # if Input_Pasivas_Activas:
            #     pasivas = ver_pasivas()
            #     Jugador_Pasiva = st.selectbox('Pasiva', pasivas, help='Pasiva con la que se jugará la partida', key = "Jugador_Moderador_Exponencial")
            # else:
            #     Jugador_Pasiva = None
        else:
            Input_Jugador_Moderador = None
        Input_Bono_Salida  = st.checkbox('Bonus de salida casilla salida', value = Input_Modo_Exponencial, disabled = Input_Modo_Exponencial)
        tratos_con_propiedades_disponibles = st.checkbox('Tratos con jugadores hasta vender todas las propiedades', value = True)
        
        
        
        t_confirmar1=st.text_input('Clave',key='txt_reseteo1',type='password')
        if st.button('Confirmar', key='btn_resteo', disabled = t_confirmar1 != 'bruno'):
            nuevo_juego(Input_Impuestos_Para_Parada_Libre, Input_Personalizar_Dinero_Inicio, Input_Personalizar_Dinero_Inicio_Cantidad, Input_Bono_Salida, Input_Pasivas_Activas, Input_Modo_Exponencial, Input_Jugador_Moderador, tratos_con_propiedades_disponibles)
            # if Input_Modo_Exponencial:
            #     Crear_Jugador(Input_Jugador_Moderador, Input_Jugador_Moderador_contraseña, Input_Personalizar_Dinero_Inicio_Cantidad, Jugador_Pasiva)
            st.success("Comienza el juego!")
            time.sleep(1)
            st.experimental_rerun() # actualiza la página