import subprocess
import sys

# Список файлов, которые нужно запустить
script_files = ["download_video.py",
                "gen_text.py",
                "gen_audio.py",
                "gen_video.py", 
                "gen_subtitles.py",
                "upload_video.py"]

for script in script_files:
    try:
        print(f"\nЗапуск {script}...")
        subprocess.run([sys.executable, script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nОшибка при выполнении {script}: {e}")
    except FileNotFoundError:
        print(f"\nФайл {script} не найден, проверьте путь к файлу.")

print("\nВсе скрипты выполнены.")
