import os


def get_latest_log_file(log_directory='logs'):
    """
    Возвращает путь к самому последнему (по времени изменения) файлу в директории logs.
    """
    try:
        files = os.listdir(log_directory)
        if not files:
            return None

        files = [os.path.join(log_directory, f) for f in files]  # Получаем полный путь к файлам
        latest_file = max(files, key=os.path.getmtime)  # Самый последний файл
        return latest_file

    except Exception as e:
        print(f"Ошибка при получении последнего файла лога: {e}")
        return None
