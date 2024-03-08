import requests
import time

def obtener_datos_mercado(coin_id):
    max_reintentos = 5  # Número máximo de intentos.
    espera = 1  # Tiempo inicial de espera en segundos.
    
    for intento in range(max_reintentos):
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': '30',
                'interval': 'daily'
            }
            respuesta = requests.get(url, params=params)
            respuesta.raise_for_status()  # Excepción para los códigos de estado.
            return respuesta.json()  # Retorna los datos si la solicitud fue exitosa.
        except requests.exceptions.HTTPError as e:
            if respuesta.status_code == 429:
                print(f"Límite de solicitudes alcanzado, reintentando en {espera} segundos...")
                time.sleep(espera)
                espera *= 2  # Incrementa el tiempo de espera exponencialmente.
            else:
                print(f"Error HTTP al obtener datos para {coin_id}: {e}")
                break  # Rompe el bucle para errores diferentes a 429.
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud para {coin_id}: {e}")
            break  # Rompe el bucle para otros errores de solicitud.
    return None  # Retorna None si se alcanza el máximo de reintentos sin éxito.
