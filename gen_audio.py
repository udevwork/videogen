import torch
import ssl
import soundfile as sf
import numpy as np
import random

# Отключение проверки SSL (если требуется)
ssl._create_default_https_context = ssl._create_unverified_context

# Загрузка модели v4
device = torch.device('cpu')  # Используем CPU
model_path = 'v4_ru.pt'
model = torch.package.PackageImporter(model_path).load_pickle("tts_models", "model")
model.to(device)

# Загрузка текста для синтеза из txt файла
input_file = "input.txt"
with open(input_file, "r", encoding="utf-8") as file:
    text = file.read()

# Удаляем лишние переносы строк
text = text.replace("\n", " ").strip()

# Список доступных голосов в модели v4
speakers = ['eugene']

# Выбор случайного голоса
random_speaker = random.choice(speakers)
print(f"Выбранный голос: {random_speaker}")

# Генерация аудиоданных
sample_rate = 48000
audio = model.apply_tts(text=text, speaker=random_speaker, sample_rate=sample_rate)

# Преобразование аудиоданных в двухмерный массив
if len(audio.shape) == 1:  # Если массив одномерный (моно)
    audio = np.expand_dims(audio, axis=1)

# Сохранение аудио в файл
output_file = "test.wav"
sf.write(output_file, audio, sample_rate)
print(f"Аудиофайл сохранён как: {output_file}")
