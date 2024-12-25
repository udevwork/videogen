import moviepy.editor as mp
import os
import whisper
import urllib.request
import ssl
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import TextClip, CompositeVideoClip

# Извлечение аудио и транскрибация

def extract_audio(video_file, audio_file="temp_audio.wav"):
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file, codec='pcm_s16le')
    return audio_file

def transcribe_audio(audio_file):
    # Игнорирование SSL-сертификатов
    ssl._create_default_https_context = ssl._create_unverified_context

    # Загрузка модели Whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, word_timestamps=True)
    return result['segments']

# Разделение текста на фрагменты для титров

def create_subtitles(segments):
    subtitles = []
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text'].strip()
        subtitles.append(((start_time, end_time), text))
    return subtitles

def render_subtitles(video_file, subtitles):
    def generator(txt):
        video = mp.VideoFileClip(video_file)
        video_width = video.size[0] - 20  # Учитываем отступы по 10 пикселей с каждой стороны
        # Динамически подстраиваем высоту фона под количество строк текста
        text_clip = TextClip(txt, font='Arial', fontsize=24, color='white', size=(video_width, None), method='caption')
        text_height = text_clip.h + 20  # Добавляем отступы сверху и снизу
        return text_clip.on_color(size=(video_width, text_height), color=(0, 0, 0), pos='center', col_opacity=0.6)

    video = mp.VideoFileClip(video_file)
    subtitles_clip = SubtitlesClip(subtitles, generator)
    result = CompositeVideoClip([video, subtitles_clip.set_position(('center', 'center'))])
    return result

# Основной скрипт

def main():
    video_file = "video_cropped.mp4"
    audio_file = extract_audio(video_file)
    segments = transcribe_audio(audio_file)

    if segments:
        subtitles = create_subtitles(segments)
        final_video = render_subtitles(video_file, subtitles)
        final_video.write_videofile("Final.mp4", codec='libx264', fps=24, audio_codec='aac')
    
    # Удалить временный аудиофайл
    if os.path.exists(audio_file):
        os.remove(audio_file)
        
    # Удаление исходного видео и аудиофайла
    if os.path.exists(video_file):
        os.remove(video_file)
        print(f"Файл '{video_file}' был удален.")

if __name__ == "__main__":
    main()
