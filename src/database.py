import sqlite3
from sqlite3 import Error

def crear_conexion(db_file):
    """Crear una conexión a la base de datos SQLite especificada por db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Conexión establecida.")
    except Error as e:
        print(e)
    return conn

def crear_tablas(conn):
    """Crear las tablas necesarias en la base de datos."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS criptomonedas (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                precio_actual REAL,
                volumen_24h REAL,
                cap_mercado REAL
            );
        """)
        print("Tablas creadas correctamente.")
    except Error as e:
        print(e)

def insertar_o_actualizar_criptomoneda(conn, id_cripto, nombre, precio_actual, volumen_24h, cap_mercado):
    """
    Inserta o actualiza una criptomoneda en la base de datos.
    """
    sql = '''INSERT INTO criptomonedas(id, nombre, precio_actual, volumen_24h, cap_mercado)
             VALUES(?,?,?,?,?)
             ON CONFLICT(id) DO UPDATE SET
             nombre=excluded.nombre,
             precio_actual=excluded.precio_actual,
             volumen_24h=excluded.volumen_24h,
             cap_mercado=excluded.cap_mercado;'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (id_cripto, nombre, precio_actual, volumen_24h, cap_mercado))
        conn.commit()
        print(f"Dato de '{nombre}' insertado/actualizado correctamente.")
    except Error as e:
        print(e)

# Inicializar base de datos y crear tablas:
if __name__ == "__main__":
    database = "ruta/a/tu/base_de_datos.db" # Ruta al archivo de la base de datos.

    # Conexión a la base de datos:
    conn = crear_conexion(database)
    if conn is not None:
        # Crear tablas:
        crear_tablas(conn)
        conn.close()
