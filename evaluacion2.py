import openrouteservice
from openrouteservice import convert

# Clave de API
api_key = '5b3ce3597851110001cf62481079697709684885bce6d417295f374a'
client = openrouteservice.Client(key=api_key)

# Coordenadas de ciudades conocidas
coordenadas_ciudades = {
    "santiago": (-70.6483, -33.4569),
    "ovalle": (-71.1985, -30.6016),
    # Puedes agregar más ciudades aquí
}

def obtener_coordenadas(ciudad):
    ciudad = ciudad.lower()
    if ciudad in coordenadas_ciudades:
        return coordenadas_ciudades[ciudad]
    else:
        print(f"No se encuentran coordenadas para {ciudad}.")
        return None

def calcular_ruta(origen, destino):
    coords = [origen, destino]
    try:
        ruta = client.directions(
            coordinates=coords,
            profile='driving-car',
            format='geojson',
            language='es'
        )
        return ruta
    except Exception as e:
        print("Error al consultar la API:", e)
        return None

def mostrar_resultados(ruta):
    features = ruta['features'][0]
    summary = features['properties']['summary']
    distance_m = summary['distance']
    duration_s = summary['duration']

    distancia_km = distance_m / 1000
    consumo_por_km = 0.07  # 7 litros cada 100km => 0.07 l/km
    consumo_litros = distancia_km * consumo_por_km
    horas = int(duration_s // 3600)
    minutos = int((duration_s % 3600) // 60)
    segundos = int(duration_s % 60)

    print(f"\nDistancia total: {distancia_km:.2f} km")
    print(f"Duración estimada del viaje: {horas} horas, {minutos} minutos, {segundos} segundos")
    print(f"Combustible estimado necesario: {consumo_litros:.2f} litros")

    instrucciones = features['properties']['segments'][0]['steps']
    print("\nNarrativa del viaje:")
    for paso in instrucciones:
        print(f"- {paso['instruction']}")

# --- Script automatizado (sin input) ---

origen_nombre = "santiago"
destino_nombre = "ovalle"

origen_coords = obtener_coordenadas(origen_nombre)
destino_coords = obtener_coordenadas(destino_nombre)

if origen_coords and destino_coords:
    ruta = calcular_ruta(origen_coords, destino_coords)
    if ruta:
        mostrar_resultados(ruta)
