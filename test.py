import os

def get_photos_path(photos_dir, photos_folder):
    folder_path = os.path.join(photos_dir, photos_folder)

    # Проверяем, существует ли папка
    if not os.path.exists(folder_path):
        raise Exception(f"Folder '{photos_folder}' not found in '{photos_dir}'")

    # Получаем список файлов из нужной папки с расширением .jpg
    jpg_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.jpg')]

    # Если список пустой, значит не было найдено файлов
    if not jpg_files:
        raise Exception(f"No JPG files found in folder '{folder_path}'")

    return jpg_files



