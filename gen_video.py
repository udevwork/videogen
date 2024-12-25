import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import moviepy.editor as mpy
from moviepy.video.fx.all import crop
import random

def crop_video(input_filename, output_filename, crop_width, crop_height):
    # Проверка существования файла
    if not os.path.exists(input_filename):
        print(f"Ошибка: Видео файл '{input_filename}' не найден.")
        return

    # Загрузка видео
    clip = mpy.VideoFileClip(input_filename)
    (w, h) = clip.size
    
    # Проверка и корректировка параметров кропа
    if crop_width > w:
        print(f"Предупреждение: Ширина кропа больше ширины видео ({w}). Устанавливается максимальная доступная ширина.")
        crop_width = w
    if crop_height > h:
        print(f"Предупреждение: Высота кропа больше высоты видео ({h}). Устанавливается максимальная доступная высота.")
        crop_height = h
    
    # Обрезка видео по заданным параметрам
    cropped_clip = crop(clip, width=crop_width, height=crop_height, x_center=w/2, y_center=h/2)
    
    # Сохранение видео с аудио
    cropped_clip = cropped_clip.set_audio(clip.audio)
    cropped_clip.write_videofile(output_filename, codec="libx264", audio_codec='aac')
    print(f"Файл успешно сохранен как '{output_filename}'")

def replace_audio(video_filename, audio_filename, output_filename):
    # Проверка существования файлов
    if not os.path.exists(video_filename):
        print(f"Ошибка: Видео файл '{video_filename}' не найден.")
        return
    
    if not os.path.exists(audio_filename):
        print(f"Ошибка: Аудио файл '{audio_filename}' не найден.")
        return
    
    # Загрузка видео и аудио
    video = VideoFileClip(video_filename)
    new_audio = AudioFileClip(audio_filename)
    
    # Длительность видео и аудио
    video_duration = video.duration
    audio_duration = new_audio.duration
    
    # Проверка, что длина видео больше длины аудио
    if video_duration <= audio_duration:
        print("Ошибка: Длина видео меньше или равна длине аудио. Невозможно выполнить операцию.")
        return
    
    # Выбор случайного начала для обрезки видео
    max_start_time = video_duration - audio_duration
    start_time = random.uniform(0, max_start_time)
    end_time = start_time + audio_duration
    
    # Обрезка видео по длине новой аудиодорожки
    video = video.subclip(start_time, end_time)
    
    # Замена аудиодорожки
    video_with_new_audio = video.set_audio(new_audio)
    
    # Экспорт видео с новой аудиодорожкой
    video_with_new_audio.write_videofile(output_filename, codec='libx264', audio_codec='aac')
    
    print(f"Файл успешно сохранен как '{output_filename}'")
    return output_filename

if __name__ == "__main__":
    # Указание файлов
    video_filename = "video.mp4"
    cropped_filename = "video_cropped.mp4"
    audio_filename = "test.wav"
    output_filename = "video_sound.mp4"

    # Параметры для кропа
    crop_width = 400  # задайте желаемую ширину
    crop_height = 800  # задайте желаемую высоту

    # Замена аудио в исходном видео
    processed_video_filename = replace_audio(video_filename, audio_filename, output_filename)
    
    # Кроп видео с замененной аудиодорожкой
    if processed_video_filename:
        crop_video(processed_video_filename, cropped_filename, crop_width, crop_height)
    
    # Удаление промежуточного файла
    if processed_video_filename and os.path.exists(processed_video_filename):
        os.remove(processed_video_filename)
        print(f"Файл '{processed_video_filename}' был удален.")
    
    # Удаление исходного видео и аудиофайла
    if os.path.exists(video_filename):
        os.remove(video_filename)
        print(f"Файл '{video_filename}' был удален.")
    
    if os.path.exists(audio_filename):
        os.remove(audio_filename)
        print(f"Файл '{audio_filename}' был удален.")
