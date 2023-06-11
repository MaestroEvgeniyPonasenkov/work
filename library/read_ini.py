import os


def read_ini_file():
    """
    Функция для чтения конфигурации .ini
    Автор: Ряднов И.М.
    """
    config = {}
    current_section = None
    with open(f"{os.getcwd()}\scripts\config.ini", 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                config[current_section] = {}
            else:
                key, value = line.split('=', 1)
                config[current_section][key.strip()] = value.strip()
    return config


def write_ini_file(config):
    """
    Функция для перезаписи новой конфигурации .ini
    :param key(dict): словарь с конфигурацией
    Автор: Ряднов И.М.
    """
    with open(f"{os.getcwd()}\scripts\config.ini", 'w') as file:
        for section, values in config.items():
            file.write(f'[{section}]\n')
            for key, value in values.items():
                file.write(f'{key} = {value}\n')
            file.write('\n')


def update_ini_value(key, value):
    """
    Функция для изменения определенного параметра конфигурации .ini
    :param key(str): название конфигурации
    :param value: новое значение
    Автор: Ряднов И.М.
    """
    config = read_ini_file()
    config['Settings'][key] = value
    write_ini_file(config)
