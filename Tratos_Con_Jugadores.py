import mysql.connector
import streamlit as st
import time

def Otros_Jugadores(Nombre_Jugador):
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
    cursor.execute(f"SELECT nombre FROM jugadores where nombre <> '{Nombre_Jugador}' AND activo = 1")
        
    # Obtener todas las filas y agregarlas a una lista
    resultados = []
    for fila in cursor.fetchall():
        resultados.append(fila[0])

    # Cerrar la conexión a la base de datos
    conn.close()

    # Devolver la lista de resultados
    return resultados

def Pagar_Trato(Nombre_Jugador, Cantidad_Dinero, Nombre_Jugador_Receptor):
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
    cursor.callproc("Pagar_Trato", (Nombre_Jugador, Cantidad_Dinero, Nombre_Jugador_Receptor))
        
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

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

def Consultar_Propiedades_Propias(Nombre_Jugador):
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
    cursor.execute(f"SELECT nombre, color FROM propiedades where dueño = '{Nombre_Jugador}' and nivel_renta = 1")
        
    # Recuperar los nombres y los emojis de los colores de las propiedades disponibles como una lista de tuplas
    propiedades_disponibles = []
    for nombre, color in cursor.fetchall():
        emoji_color = colores_emoji[color]
        propiedades_disponibles.append((nombre, emoji_color))

    # Cerrar la conexión a la base de datos
    conn.close()

    return propiedades_disponibles

def Dar_Propiedad_Trato(Nombre_Propiedad, Nombre_Jugador_Receptor):
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
    cursor.callproc("Dar_Propiedad_Trato", (Nombre_Propiedad, Nombre_Jugador_Receptor))
        
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()


def main(Nombre_Jugador, Dinero_Jugador):
    Otro_Jugador = Otros_Jugadores(Nombre_Jugador)
    if Otro_Jugador == []:
        st.warning("No hay otros jugadores en el juego")
    else:
        Nombre_Jugador_Trato = st.selectbox("Jugador con el que será el trato", Otro_Jugador)
        Razon_Trato = st.selectbox("Razón", ["Pago", "Dar propiedad"])

        if Razon_Trato == "Pago":
            Cantidad_Pago = st.number_input("Cantidad dinero", 0, 9999, 0,50, None, "Cantidad_Dinero_Trato")
            if st.button(label = f"Pagar ${Cantidad_Pago} a {Nombre_Jugador_Trato}", key = "btn_pagar_trato", disabled = Cantidad_Pago == 0 or Cantidad_Pago > Dinero_Jugador):
                Pagar_Trato(Nombre_Jugador, Cantidad_Pago, Nombre_Jugador_Trato)
                st.success(f"Pagaste ${Cantidad_Pago}!")
                time.sleep(0.5)
                st.experimental_rerun()
        elif Razon_Trato == "Dar propiedad":
            propiedades_propias = Consultar_Propiedades_Propias(Nombre_Jugador)
            if propiedades_propias != []:
                opciones = [f"{nombre} {emoji}" for nombre, emoji in propiedades_propias]
                Propiedad_Seleccionada = st.selectbox('Propiedad', opciones)
                emojis = list(colores_emoji.values())
                for i in emojis:
                    Propiedad_Seleccionada = Propiedad_Seleccionada.replace(f" {i}","")
                if Propiedad_Seleccionada != None:
                    if st.button(label = f"Dar {Propiedad_Seleccionada} a {Nombre_Jugador_Trato}", key = "btn_dar_propiedad_trato"):
                        Dar_Propiedad_Trato(Propiedad_Seleccionada, Nombre_Jugador_Trato)
            else:
                st.error("No tienes propiedades")