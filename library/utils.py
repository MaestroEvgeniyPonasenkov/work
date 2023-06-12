import os
import pandas as pd
from tkinter import filedialog as fld


def save_tables(GOODS: pd.DataFrame, ORDERS: pd.DataFrame, ORDERS_STRUCTURE: pd.DataFrame):
    """
    Сохранение всех таблиц
    Автор: Болезнов С.А.
    :param GOODS: Датафрейм товаров
    :param ORDERS: Датафрейм заказов
    :param ORDERS_STRUCTURE: Датафрейм содержания заказов
    """
    path = f'{os.getcwd()}\\data'
    GOODS.to_csv(f'{path}/MOCK_DATA_1.csv', index=False)
    ORDERS.to_csv(f'{path}/MOCK_DATA_2.csv', index=False)
    ORDERS_STRUCTURE.to_csv(f'{path}/MOCK_DATA_3.csv', index=False)


def save_as(table: pd.DataFrame):
    """
    Сохранение отдельной таблицы
    Автор: Болезнов С.А.
    :param table: таблица
    """
    path = f'{os.getcwd()}\\output'
    ftypes = [('csv', '.csv'), ('excel', '.xlsx'), ('pickle', '.pickle')]
    filepath = fld.asksaveasfilename(filetypes=ftypes, initialdir=path, defaultextension='csv')
    if filepath != "":
        file_format = filepath.split('.')[-1]
        if file_format == 'csv':
            table.to_csv(filepath, index=False)
            return
        if file_format == 'xlsx':
            table.to_excel(filepath, index=False)
            return
        if file_format == 'pick':
            table.to_pickle(filepath)
            return


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
