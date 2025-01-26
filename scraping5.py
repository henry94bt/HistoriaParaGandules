import instaloader
import csv

# Crear una instancia de Instaloader
L = instaloader.Instaloader()

# Nombre del perfil de Instagram
profile_name = "historiaparagandules"

# Obtener el perfil
profile = instaloader.Profile.from_username(L.context, profile_name)

# Crear o abrir el archivo CSV
with open("informacion_reels_simple.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Escribir los encabezados en el archivo CSV
    writer.writerow(["Fecha", "Texto del reel", "Likes", "Comentarios", "URL del video", 
                     "Visualizaciones", "Duración del video (s)", "URL del Post"])

    # Iterar sobre los reels del perfil y escribir los resultados en el archivo CSV
    for post in profile.get_posts():  # Usa get_posts() si get_reels() no funciona
        if post.is_video:  # Filtra solo los videos
            fecha = post.date.strftime('%Y-%m-%d %H:%M:%S')
            texto = post.caption or "Sin texto"
            likes = post.likes or 0
            comentarios = post.comments or 0
            url_video = post.video_url or "Sin URL"
            visualizaciones = post.video_view_count or "No disponible"
            duracion_video = post.video_duration or "No disponible"
            url_post = f"https://www.instagram.com/p/{post.shortcode}/"

            writer.writerow([fecha, texto, likes, comentarios, url_video, 
                             visualizaciones, duracion_video, url_post])
            print(f"Scrapeando post del {fecha}")

print("Información guardada en 'informacion_reels_simple.csv'")
