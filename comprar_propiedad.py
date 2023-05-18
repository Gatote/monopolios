import streamlit as st
import mysql.connector

# Diccionario que asocia cada nombre de color con el emoji correspondiente
colores_emoji = {
    "Marron": "🟤",
    "Celeste": "🔵",
    "Morado": "🟣",
    "Naranja": "🟠",
    "Rojo": "🔴",
    "Amarillo": "🟡",
    "Verde": "🟢",
    "Azul": "🔵",
    "Negro": "⚫",
    "Servicio": "🔧"
}

def Consultar_Propiedades_Disponibles():
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )   
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT que incluya la columna 'color'
    cursor.execute("SELECT nombre, color FROM propiedades WHERE dueño IS NULL")

    # Recuperar los nombres y los emojis de los colores de las propiedades disponibles como una lista de tuplas
    propiedades_disponibles = []
    for nombre, color in cursor.fetchall():
        emoji_color = colores_emoji[color]
        propiedades_disponibles.append((nombre, emoji_color))

    # Cerrar la conexión a la base de datos
    conn.close()

    return propiedades_disponibles

def Consultar_Propiedades_Color(Nombre_Jugador):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )   
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT que incluya la columna 'color'
    cursor.execute(f"SELECT nombre, color FROM propiedades WHERE color <> 'negro' and color <> 'servicio' and dueño = '{Nombre_Jugador}' and nivel_renta = 1")

    # Recuperar los nombres y los emojis de los colores de las propiedades disponibles como una lista de tuplas
    propiedades_disponibles = []
    for nombre, color in cursor.fetchall():
        emoji_color = colores_emoji[color]
        propiedades_disponibles.append((nombre, emoji_color))

    # Cerrar la conexión a la base de datos
    conn.close()
    if propiedades_disponibles:
        return propiedades_disponibles
    else:
        return []

def Consultar_Precio_Propiedad_Disponible(Nombre_Propiedad):
    # Establecer una conexión a la base de datos
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="monopolios"
    )   
    # Crear un cursor para ejecutar comandos en la base de datos
    cursor = conn.cursor()

    # Hacer un SELECT que incluya la columna 'color'
    cursor.execute(f"SELECT precio FROM propiedades WHERE nombre = '{Nombre_Propiedad}'")

    precio = cursor.fetchall()[0][0]
    # Cerrar la conexión a la base de datos
    conn.close()

    return precio

def Comprar_Propiedad(Nombre_Jugador, Dinero_Jugador, Nombre_Propiedad, Precio_Propiedad):
    import time
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
    cursor.callproc('Comprar_Propiedad', (Nombre_Jugador, Dinero_Jugador, Nombre_Propiedad, Precio_Propiedad))
    conn.commit()
    
    # Cerrar la conexión a la base de datos
    conn.close()
    st.success(f"Compraste {Nombre_Propiedad}!")
    time.sleep(1)
    st.experimental_rerun()

def Montar_Grupo_Color(Nombre_Propiedad):
    import time
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
    cursor.callproc('Montar_Grupo_Color', (Nombre_Propiedad,))
    
    conn.commit()
    # Cerrar la conexión a la base de datos
    conn.close()


    #st.success(f"{}")
    time.sleep(1)
    st.experimental_rerun()


def main(Nombre_Jugador,Dinero_Jugador):
    propiedades_disponibles = Consultar_Propiedades_Disponibles()
    if not propiedades_disponibles:
        st.success('Tratos con jugadores disponibles!')
    else:
        col1_comprar_propiedad,col2_comprar_propiedad = st.columns(2)
        opciones = [f"{nombre} {emoji}" for nombre, emoji in propiedades_disponibles]
        with col1_comprar_propiedad:
            Propiedad_Seleccionada_A_Comprar = st.selectbox('Propiedad', opciones)

        with col2_comprar_propiedad:
            emojis = list(colores_emoji.values())
            for i in emojis:
                Propiedad_Seleccionada_A_Comprar = Propiedad_Seleccionada_A_Comprar.replace(f" {i}","")
            
            Precio_Propiedad = Consultar_Precio_Propiedad_Disponible(Propiedad_Seleccionada_A_Comprar)
            Nombre_Propiedad = Propiedad_Seleccionada_A_Comprar
            if st.button(f'Pagar ${Precio_Propiedad}', disabled = Dinero_Jugador < Precio_Propiedad ):
                Comprar_Propiedad(Nombre_Jugador, Dinero_Jugador, Nombre_Propiedad, Precio_Propiedad)

                
    propiedades_disponibles = Consultar_Propiedades_Color(Nombre_Jugador)

    st.subheader('Montar grupo de color')
    col1_comprar_propiedad,col2_comprar_propiedad = st.columns(2)
    opciones = [f"{nombre} {emoji}" for nombre, emoji in propiedades_disponibles]
    with col1_comprar_propiedad:
        Propiedad_Seleccionada_A_Comprar = st.selectbox('Selecciona una propiedad del grupo a montar', opciones)

    with col2_comprar_propiedad:
        emojis = list(colores_emoji.values())
        for i in emojis:
            Propiedad_Seleccionada_A_Comprar = Propiedad_Seleccionada_A_Comprar.replace(f" {i}","")
        
        Precio_Propiedad = Consultar_Precio_Propiedad_Disponible(Propiedad_Seleccionada_A_Comprar)
        Nombre_Propiedad = Propiedad_Seleccionada_A_Comprar
        if st.button(f'Montar grupo de color', disabled = False):
            Montar_Grupo_Color(Nombre_Propiedad)
