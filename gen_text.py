from openai import OpenAI

# Создаем экземпляр клиента OpenAI с вашим API ключом
client = OpenAI(api_key="sk-...NEA")

def chat_with_gpt(prompt, role="user"):
    try:
        # Создание запроса на генерацию ответа с использованием модели
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты - маркетолог, ты пишешь провокационные рекламные тексты для YouTube shorts. Ты отвечаешь только сырым текстом, без кавычек, без темы, в ответе должен быть сразу только готовый текст. Цифры пиши буквами. Английские слова пиши русскими буквами!"},
                {"role": role, "content": prompt}
            ]
        )
        # Извлечение содержимого ответа
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None

def write_to_file(content, filename):
    # Убираем кавычки из текста перед записью в файл
    content = content.replace('"', '').replace("'", '')
    # Запись содержимого в файл
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def read_prompt_from_file(filename="promt.txt"):
    # Чтение промта из файла
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return None

if __name__ == "__main__":
    # Чтение пользовательского запроса из файла promt.txt
    user_prompt = read_prompt_from_file()
    if user_prompt:
        # Получаем ответ от GPT на первый запрос
        main_response = chat_with_gpt(user_prompt)
        
        if main_response:
            # Записываем основной ответ в файл input.txt
            write_to_file(main_response, "input.txt")
            print(f"Ответ записан в файл input.txt")
            
            # Генерация названия для видеоролика Reels на основе первого ответа
            title_prompt = f"Пожалуйста, сгенерируйте название для видеоролика Reels на основе следующего текста: \"{main_response}\". Максимум 5 слов"
            video_title = chat_with_gpt(title_prompt)
            
            if video_title:
                # Запись названия в файл uploaded_video_name.txt
                write_to_file(video_title, "uploaded_video_name.txt")
                print(f"Название записано в файл uploaded_video_name.txt")
                
                # Генерация описания для ролика с хештегами на основе первого ответа и названия
                description_prompt = f"Пожалуйста, сгенерируйте описание для этого видео: \"{video_title}\". Используйте при этом содержание ответа \"{main_response}\" и добавьте подходящие хештеги. Максимум 20 слов"
                video_description = chat_with_gpt(description_prompt)
                
                if video_description:
                    # Запись описания в файл uploaded_video_description.txt
                    write_to_file(video_description, "uploaded_video_description.txt")
                    print(f"Описание записано в файл uploaded_video_description.txt")
                else:
                    print("Не удалось получить описание для ролика.")
            else:
                print("Не удалось получить название для видео.")
        else:
            print("Не удалось получить ответ от ChatGPT")
    else:
        print("Не удалось прочитать запрос из файла promt.txt")
