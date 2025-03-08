import requests

cedula = "0942445743"  # Reemplázalo con un número válido
api_url = f"https://prueba.onlineciber.com/app/cedula.php?id={cedula}"

try:
    response = requests.get(api_url)
    print("Código de estado:", response.status_code)  # Código HTTP (200, 404, etc.)
    print("Contenido devuelto:\n", response.text)  # Muestra el contenido de la API

    # Intentar convertir la respuesta en JSON
    try:
        data = response.json()
        print("\n✅ La API devolvió JSON válido:\n", data)
    except ValueError:
        print("\n❌ Error: La API no devolvió JSON válido.")

except requests.RequestException as e:
    print("\n🚨 Error al conectar con la API:", str(e))
