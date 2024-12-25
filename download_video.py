import random
import ssl
import yt_dlp
import moviepy.editor as mp
import os

ssl._create_default_https_context = ssl._create_unverified_context

# Имя файла с URL-ами видео
VIDEO_URLS_FILE = 'video_urls_to_download.txt'

# Функция для чтения ссылок из файла и добавления их в массив
def read_video_urls(file_path):
    video_urls = []
    try:
        with open(file_path, 'r') as file:
            # Читаем строки из файла и убираем пробелы и символы новой строки
            video_urls = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден. Пожалуйста, создайте его и добавьте ссылки на видео.")
    return video_urls

# Функция для скачивания случайного видео из массива ссылок
def download_random_video(video_urls):
    if not video_urls:
        print("Нет доступных ссылок для скачивания.")
        return
    
    # Выбираем случайную ссылку из массива
    random_video_url = random.choice(video_urls)
    print(f"Скачиваем видео по ссылке: {random_video_url}")
    
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',  # Скачиваем лучшее доступное качество до 720p
        'outtmpl': 'video.%(ext)s',  # Название скачанного файла
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([random_video_url])
        print(f"Видео по ссылке {random_video_url} было успешно скачано!")
        convert_to_mp4('video.webm', 'video.mp4')
    except Exception as e:
        print(f"Произошла ошибка при скачивании видео: {e}")

# Функция для конвертации видео в mp4 формат
def convert_to_mp4(input_filename, output_filename):
    if os.path.exists(input_filename):
        try:
            video_clip = mp.VideoFileClip(input_filename)
            video_clip.write_videofile(output_filename, codec='libx264', audio_codec='aac')
            print(f"Видео успешно конвертировано в формат MP4 и сохранено как '{output_filename}'")
            os.remove(input_filename)
            print(f"Файл '{input_filename}' был удален.")
        except Exception as e:
            print(f"Ошибка при конвертации видео: {e}")
    else:
        print(f"Файл '{input_filename}' не найден для конвертации.")

# Главная часть скрипта
def main():
    # Читаем ссылки на видео из файла
    video_urls = read_video_urls(VIDEO_URLS_FILE)
    
    # Скачиваем случайное видео из списка
    download_random_video(video_urls)

if __name__ == "__main__":
    main()
