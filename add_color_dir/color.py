from PyInstaller.utils.hooks import collect_data_files

# Добавляем зависимости colorlog
datas = collect_data_files('colorlog')
