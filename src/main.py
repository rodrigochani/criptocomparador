from database import crear_conexion, crear_tablas,insertar_o_actualizar_criptomoneda
from api import obtener_datos_mercado
import webbrowser

# Ruta al archivo de base de datos:
RUTA_DB = "db/criptocomparador.db"

def procesar_datos_criptomonedas(conn, coin_id, datos_mercado):
    if datos_mercado is None or 'prices' not in datos_mercado or 'market_caps' not in datos_mercado or 'total_volumes' not in datos_mercado:
        print(f"No hay datos suficientes para procesar {coin_id}.")
        return

    # Calcular promedios
    precios_promedio = sum([precio for precio, _ in datos_mercado['prices']]) / len(datos_mercado['prices'])
    caps_promedio = sum([cap for cap, _ in datos_mercado['market_caps']]) / len(datos_mercado['market_caps'])

    # Manejo de volumen de 24h
    if len(datos_mercado['total_volumes']) > 0:
        volumen_24h = datos_mercado['total_volumes'][-1][1]  # El último elemento, valor del volumen
    else:
        volumen_24h = 0  # Si no hay datos disponibles, mantiene el valor provisional.

    nombre = coin_id.title()  # Asegurar que el nombre inicie con mayúsculas

    # Llamar a la función para insertar o actualizar la base de datos
    insertar_o_actualizar_criptomoneda(conn, coin_id, nombre, precios_promedio, volumen_24h, caps_promedio)

def actualizar_datos_criptomonedas(conn):
    lista_ids = [
        'bitcoin',
        'ethereum',
        'binancecoin',
        'ripple',
        'cardano',
        'solana',
        'polkadot',
        'dogecoin',
        'chainlink',
        'litecoin'
    ]
    for coin_id in lista_ids:
        print(f"Actualizando datos de mercado para {coin_id}...")
        datos_mercado = obtener_datos_mercado(coin_id)
        procesar_datos_criptomonedas(conn, coin_id, datos_mercado)

def generar_html_criptomonedas():
    conn = crear_conexion(RUTA_DB)
    if conn is not None:
        crear_tablas(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM criptomonedas")
        rows = cursor.fetchall()

        # Estructura del archivo HTML:
        html_inicio = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Listado de Criptomonedas</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Listado de Criptomonedas</h1>
    <table>
        <tr>
            <th>Nombre</th>
            <th>Precio promedio actual (USD)</th>
            <th>Volumen 24 h (USD)</th>
            <th>Capitalizacion promedio de mercado (USD)</th>
        </tr>
"""
        html_fin = """
    </table>
</body>
</html>
"""
        nombre_archivo = "criptomonedas.html"

        with open(nombre_archivo, "w") as file:
            file.write(html_inicio)
            for row in rows:
                nombre_con_mayusculas = row[1].title()
                file.write(f"""<tr>
                                <td>{nombre_con_mayusculas}</td>
                                <td>{row[2]:,.2f}</td>
                                <td>{row[3]:,.2f}</td>
                                <td>{row[4]:,.2f}</td>
                               </tr>\n""")
            file.write(html_fin)
        
        print("Archivo HTML generado exitosamente.")
        conn.close()

        # Abrir el archivo HTML en el navegador predeterminado:
        webbrowser.open(nombre_archivo)

    else:
        print("Error al crear la conexión a la base de datos.")

if __name__ == '__main__':
    conn = crear_conexion(RUTA_DB)
    crear_tablas(conn)
    actualizar_datos_criptomonedas(conn)
    generar_html_criptomonedas()