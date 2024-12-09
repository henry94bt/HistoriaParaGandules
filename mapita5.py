import folium
import pandas as pd
import requests
import os

# Crear carpeta para almacenar las imágenes
if not os.path.exists("imagenes"):
    os.makedirs("imagenes")

# Cargar el archivo Excel
df = pd.read_excel('excel_info_1.xlsx')

# Función para obtener coordenadas
def obtener_coordenadas(localizacion):
    try:
        lat, lon = map(float, localizacion.split(','))
        return lat, lon
    except Exception as e:
        print(f"Error al procesar la ubicación: {localizacion} - {e}")
        return None, None

# Descargar imágenes y almacenarlas localmente
def descargar_imagen(url, index):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            ruta_imagen = f"imagenes/imagen_{index}.jpg"
            with open(ruta_imagen, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return ruta_imagen
        else:
            print(f"No se pudo descargar la imagen: {url}")
            return None
    except Exception as e:
        print(f"Error al descargar la imagen: {url} - {e}")
        return None

# Crear el mapa
m = folium.Map(location=[28.0, -15.0], zoom_start=6)

# Iterar sobre el DataFrame
for index, row in df.iterrows():
    lat, lon = obtener_coordenadas(row['Localización'])
    if lat is not None and lon is not None:
        ruta_imagen = descargar_imagen(row['URL de imagen'], index)
        if ruta_imagen:
            popup_content = f"""
            <div>
                <h4>{row['Texto del reel'].split(' ')[0]}</h4>
                <img src="{ruta_imagen}" alt="Imagen del Reel" style="width:200px;height:auto;">
                <a href="{row['URL del Post']}">Ver publicación</a>
            </div>
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(m)

# Guardar el mapa como archivo HTML
m.save("mapa_ubicaciones_reels_with_thumbnails.html")
print("Mapa generado con imágenes y enlaces: 'mapa_ubicaciones_reels_with_thumbnails.html'")
