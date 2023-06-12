"""
Программа для отображения, изменения и описания данныхиз справочников с графическим интерфейсом
Бригада 7
Авторы: Ряднов И.М, Болезнов С.А.
"""
import os
import sys
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, Entry, colorchooser
from tkinter.ttk import Treeview, Spinbox

os.chdir("\\".join(os.getcwd().split("\\")[:-1]))
sys.path.append("\\".join(os.getcwd().split("\\")))
from library.read_ini import read_ini_file, update_ini_value
from library.text_reports import report_about_firm, merge_files, generate_attribute_report
from library.hist_chart import histogram
from library.bar_chart import report_day_sales, report_week_sales, report_year_sales, report_month_sales
from library.boxplot_chart import report_price_by_category
from library.scatter_chart import report_price_by_quantity
from library.data_export import save_tables, save_as


def create_pivot_table():
    """
    Создание окна с выбором параметров для сводной таблицы
    Автор Ряднов И.М.
    """
    dialog = tk.Toplevel(root)
    dialog.title("Сводная таблица")
    agg_functions = {
        "среднее значение": "mean",
        "сумма": "sum",
        "минимальное значение": "min",
        "максимальное значение": "max",
        "количество непустых значений": "count",
        "медиана": "median",
        "стандартное отклонение": "std",
        "дисперсия": "var",
        "первое значение": "first",
        "последнее значение": "last",
        "произведение": "prod"
    }

    tk.Label(dialog, text="Выберите значения (values):").grid(row=0, column=0, sticky="nesw")
    values_entry = ttk.Combobox(dialog, values=['None'] + list(MERGED.columns), state='readonly')
    values_entry.grid(row=1, column=0, sticky="nesw")

    tk.Label(dialog, text="Выберите индекс (index):").grid(row=0, column=1, sticky="nesw")
    index_entry = ttk.Combobox(dialog, values=['None'] + list(MERGED.columns), state='readonly')
    index_entry.grid(row=1, column=1, sticky="nesw")

    tk.Label(dialog, text="Выберите столбцы (columns):").grid(row=0, column=2, sticky="nesw")
    columns_entry = ttk.Combobox(dialog, values=['None'] + list(MERGED.columns), state='readonly')
    columns_entry.grid(row=1, column=2, sticky="nesw")

    tk.Label(dialog, text="Выберите функцию агрегации (aggfunc):").grid(row=0, column=3, sticky="nesw")
    aggfunc_entry = ttk.Combobox(dialog, values=list(agg_functions.keys()), state='readonly')
    aggfunc_entry.grid(row=1, column=3, sticky="nesw")

    def create_pivot_table():
        """
        Создание сводной таблицы
        Автор Ряднов И.М.
        """
        values = values_entry.get()
        index = index_entry.get()
        columns = columns_entry.get()
        aggfunc = aggfunc_entry.get()

        try:
            pivot_data = pd.pivot_table(MERGED,
                                        values=values if values != 'None' else None,
                                        index=index if index != 'None' else None,
                                        columns=columns if columns != 'None' else None,
                                        aggfunc=agg_functions.get(aggfunc))
            dialog.destroy()
            dialog2 = tk.Toplevel(root)
            dialog2.title("Сводная таблица")
            table = create_table(dialog2, pivot_data, True)
            table.pack(fill='both', expand=True)
            export_button = ttk.Button(dialog2, text='Экспорт', command=lambda: save_as(pivot_data))
            export_button.pack(fill='both', expand=True, )
            config_widgets(dialog2, 2, 1)

        except Exception as ex:
            print(f"Данные не подходят для создания сводной таблицы\nДетали: {ex}")

    tk.Button(dialog, text="Создать таблицу", command=create_pivot_table).grid(row=2, column=0, columnspan=4,
                                                                               sticky="nesw")
    config_widgets(dialog, 3, 4)


def create_statistic_report():
    """
    Создание окна с выбором атрибутов для статистического отчета
    Автор Ряднов И.М.
    """
    dialog = tk.Toplevel(root)
    dialog.title("Статистический отчет")

    tk.Label(dialog, text="Выберите первый атрибут:").grid(row=0, column=0, sticky="nesw")
    attribute_1_entry = ttk.Combobox(dialog, values=list(MERGED.columns), state='readonly')
    attribute_1_entry.grid(row=1, column=0, sticky="nesw")

    tk.Label(dialog, text="Выберите второй атрибут:").grid(row=0, column=1, sticky="nesw")
    attribute_2_entry = ttk.Combobox(dialog, values=list(MERGED.columns), state='readonly')
    attribute_2_entry.grid(row=1, column=1, sticky="nesw")

    def export():
        print(1)

    def create_stat_report():
        """
        Создание статистического отчета
        Автор Ряднов И.М., Болезнов С.А.
        """
        attribute_1 = attribute_1_entry.get()
        attribute_2 = attribute_2_entry.get()

        attribute_rep = generate_attribute_report(MERGED, attribute_1, attribute_2)

        dialog.destroy()
        dialog2 = tk.Toplevel(root)
        dialog2.title("Статистический отчёт")
        tab_controler = ttk.Notebook(dialog2)
        tab_1 = ttk.Frame(tab_controler)
        tab_2 = ttk.Frame(tab_controler)
        tab_3 = ttk.Frame(tab_controler)
        tab_4 = ttk.Frame(tab_controler)
        tab_controler.add(tab_1, text='Таблица 1')
        tab_controler.add(tab_2, text='Таблица 2')
        tab_controler.add(tab_3, text='Таблица 3')
        tab_controler.add(tab_4, text='Таблица 4')
        create_table(tab_1, attribute_rep[0])
        create_table(tab_2, attribute_rep[1])
        create_table(tab_3, attribute_rep[2])
        create_table(tab_4, attribute_rep[3])
        tab_controler.grid(row=0, column=0, columnspan=2, sticky='nsew')
        export_button_1 = ttk.Button(dialog2, text='Экспорт 1', command=lambda: save_as(attribute_rep[0]))
        export_button_1.grid(row=1, column=0, sticky='nsew')

        export_button_1 = ttk.Button(dialog2, text='Экспорт 2', command=lambda: save_as(attribute_rep[1]))
        export_button_1.grid(row=1, column=1, sticky='nsew')

        export_button_1 = ttk.Button(dialog2, text='Экспорт 3', command=lambda: save_as(attribute_rep[2]))
        export_button_1.grid(row=2, column=0, sticky='nsew')

        export_button_1 = ttk.Button(dialog2, text='Экспорт 4', command=lambda: save_as(attribute_rep[3]))
        export_button_1.grid(row=2, column=1, sticky='nsew')
        config_widgets(dialog2, 3, 2)

    tk.Button(dialog, text="Создать таблицу", command=create_stat_report).grid(row=2, column=0, columnspan=2,
                                                                               sticky="nesw")
    config_widgets(dialog, 3, 2)


def create_table(tab, data: pd.DataFrame, pivot=False) -> Treeview:
    """
    Функция для добавления таблицы в окно
    :param pivot: Является ли таблица сводной
    :param tab(tk.ttk.Frame): Название окна
    :param data(pd.DataFrame): Данные таблицы
    :return: Полученный виджет таблицы
    Автор: Болезнов С.А., Ряднов И.М.
    """
    translater = {
        'Order ID': 'Номер заказа',
        'Product ID': 'Номер товара',
        'Quantity': 'Количество',
        'Product': 'Товар',
        'Description': 'Описание',
        'Price': 'Цена',
        'Category': 'Категория',
        'Date': 'Дата',
        'Sum': 'Сумма'
    }
    table_frame = ttk.Frame(tab)
    table_frame.pack(fill='both', expand=True)

    table = ttk.Treeview(table_frame)
    table.pack(side='left', fill='both', expand=True)
    table.configure(style='Treeview')

    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=table.yview)
    scrollbar.pack(side='right', fill='y')
    table.configure(yscroll=scrollbar.set)

    if pivot:
        data = data.reset_index()
    heads = [translater.get(head, str(head)) for head in data.columns]
    table['columns'] = heads
    table['show'] = 'headings'

    for header in heads:
        table.heading(header, text=header)
        if len(heads) == 9:
            table.column(header, width=0, anchor='center')
        else:
            table.column(header, anchor='center')

    for i, row in data.iterrows():
        values = list(row)
        table.insert("", "end", text=i, values=values)
    return table


def new_save():
    """
    Функция для сохранения одной таблицы в отдельный файл
    Автор: Болезнов С.А.
    """
    index = tab_control.index(tab_control.select())
    tabs = [GOODS, ORDERS, ORDERS_STRUCTURE, MERGED]
    table = tabs[index]
    save_as(table)


def add_datas(parent) -> tuple[Spinbox, Spinbox, Spinbox, Spinbox, Spinbox, Spinbox]:
    """
    Функция для добавления в окно полей ввода даты
    Автор: Болезнов С.А.
    :param parent: Название окна
    :return: Добавленные виджеты
    """
    start_date_label = tk.Label(parent, text='Выберите начальную дату:')
    start_date_label.grid(column=0, row=0, columnspan=3, sticky="nesw")
    start_date_day = tk.Spinbox(parent, from_=1, to=31, width=2)
    start_date_day.grid(column=0, row=1, sticky="nesw")
    start_date_month = tk.Spinbox(parent, from_=1, to=12, width=2)
    start_date_month.grid(column=1, row=1, sticky="nesw")
    start_date_year = tk.Spinbox(parent, from_=2022, to=2023, width=4)
    start_date_year.grid(column=2, row=1, sticky="nesw")

    end_date_label = tk.Label(parent, text='Выберите конечную дату:')
    end_date_label.grid(column=0, row=2, columnspan=3, sticky="nesw")
    end_date_day = tk.Spinbox(parent, from_=1, to=31, width=2)
    end_date_day.grid(column=0, row=3, sticky="nesw")
    end_date_month = tk.Spinbox(parent, from_=1, to=12, width=2)
    end_date_month.grid(column=1, row=3, sticky="nesw")
    end_date_year = tk.Spinbox(parent, from_=2022, to=2023, width=4)
    end_date_year.grid(column=2, row=3, sticky="nesw")
    return start_date_day, start_date_month, start_date_year, end_date_day, end_date_month, end_date_year


def config_widgets(parent, rows: int, cols: int):
    """
    Функция для задания веса каждому элемента окна.
    Необходимо для коректного отображения окна при растяжении.
    Автор: Болезнов С.А.
    :param parent: Название окна
    :param rows: Количество рядов в сетке окна
    :param cols: Количество столбцов в сетке окна
    """
    for col in range(cols):
        parent.columnconfigure(index=col, weight=1)
    for row in range(rows):
        parent.rowconfigure(index=row, weight=1)


def report_1():
    """
    Создание нового окна для ввода необходимых параметров для текстового отчета
    Автор: Болезнов С.А.
    """
    dialog = tk.Toplevel(root)
    dialog.title("Текстовый отчёт")
    start_date_day, start_date_month, start_date_year, end_date_day, \
        end_date_month, end_date_year = add_datas(dialog)
    tk.Label(dialog, text="Выберете категорию:").grid(row=4, column=0, columnspan=3)
    categories = list(GOODS.Category.unique())
    firm_entry = ttk.Combobox(dialog, values=categories, textvariable=categories[0])
    firm_entry.grid(row=5, column=0, columnspan=3, sticky="nesw")

    config_widgets(dialog, 7, 3)

    def ok_button():
        """
        Вывод полученного отчета на экран
        Автор: Болезнов С.А.
        """
        first_date = f'{start_date_year.get()}-{start_date_month.get()}-{start_date_day.get()}'
        second_date = f'{end_date_year.get()}-{end_date_month.get()}-{end_date_day.get()}'
        category = firm_entry.get()

        report = report_about_firm(MERGED, first_date, second_date, category)
        dialog.destroy()
        dialog2 = tk.Toplevel(root)
        dialog2.title(f"Текстовый отчёт о продажах {category}")
        table = create_table(dialog2, report)
        table.pack(fill='both', expand=True)
        export_button = ttk.Button(dialog2, text='Экспорт', command=lambda: save_as(report))
        export_button.pack(fill='both', expand=True, )
        config_widgets(dialog2, 2, 1)

    tk.Button(dialog, text="Создать", command=ok_button).grid(row=6, column=0, columnspan=2, sticky="nesw")
    tk.Button(dialog, text='Отменить', command=dialog.destroy).grid(row=6, column=2, sticky='nsew')


def create_hist():
    """
    Создание нового окна с выбором гистограмм
    Автор: Болезнов С.А.
    """
    dialog = tk.Toplevel(root)
    dialog.title("Создание гистограммы")
    tk.Button(dialog, text="Гистограмма распределения\nколичества товаров\nв заказе",
              command=lambda: histogram(MERGED, 'Quantity')).grid(row=0, column=0, sticky="nesw")
    tk.Button(dialog, text='Гистограмма распределения\nцены на товары',
              command=lambda: histogram(MERGED, 'Price')).grid(row=0, column=1, sticky='nsew')
    tk.Button(dialog, text="Гистограмма распределения\nсуммы заказов",
              command=lambda: histogram(MERGED, 'Sum')).grid(row=1, column=0, sticky="nesw")
    tk.Button(dialog, text='Отменить', command=dialog.destroy).grid(row=1, column=1, sticky='nsew')
    config_widgets(dialog, 2, 2)


def create_bar():
    """
    Создание нового окна для выбора столбчатых диаграмм
    Автор: Болезнов С.А.
    """
    dialog = tk.Toplevel(root)
    dialog.title("Создание столбчатой диаграммы")
    tk.Button(dialog, text="Продажи по дням",
              command=lambda: report_day_sales(ORDERS)).grid(row=0, column=0, sticky="nesw")
    tk.Button(dialog, text='Продажи по неделям',
              command=lambda: report_week_sales(ORDERS)).grid(row=0, column=1, sticky='nsew')
    tk.Button(dialog, text="Продажи по месяцам",
              command=lambda: report_month_sales(ORDERS)).grid(row=1, column=0, sticky="nesw")
    tk.Button(dialog, text="Продажи по годам",
              command=lambda: report_year_sales(ORDERS)).grid(row=1, column=1, sticky="nesw")
    tk.Button(dialog, text='Отменить', command=dialog.destroy).grid(row=2, column=0, columnspan=2, sticky='nsew')
    config_widgets(dialog, 3, 2)


def create_scatter():
    """
    Функция для подготовки данных и отображения таблицы рассеивания
    Автор: Ряднов И.М.
    """
    data = pd.merge(ORDERS_STRUCTURE, GOODS, on="Product ID")
    data['Price'] = data['Price'].astype(float)
    report_price_by_quantity(data)


def del_line():
    """
    Функция для удаления строк таблицы.
    Автор: Болезнов С.А.
    """
    index = tab_control.index(tab_control.select())
    if index == 0:
        selected_item = goods_table.selection()[0]
        selected_line = goods_table.item(selected_item)['values']
        global GOODS
        GOODS = GOODS.drop(GOODS.loc[GOODS['Product ID'] == selected_line[0]].index)
        goods_table.delete(selected_item)
    if index == 1:
        selected_item = orders_table.selection()[0]
        selected_line = orders_table.item(selected_item)['values']
        global ORDERS
        ORDERS = ORDERS.drop(ORDERS.loc[ORDERS['Order ID'] == selected_line[0]].index)
        orders_table.delete(selected_item)
    if index == 2:
        selected_item = orders_structure_table.selection()[0]
        selected_line = orders_structure_table.item(selected_item)['values']
        global ORDERS_STRUCTURE
        ORDERS_STRUCTURE = ORDERS_STRUCTURE.drop(
            ORDERS_STRUCTURE.loc[ORDERS_STRUCTURE['Order ID'] == selected_line[0]].index)
        orders_structure_table.delete(selected_item)
    if index == 3:
        selected_item = merged_table.selection()[0]
        selected_line = merged_table.item(selected_item)['values']
        global MERGED
        MERGED = MERGED.drop(MERGED.loc[MERGED['Order ID'] == selected_line[0]].index)
        merged_table.delete(selected_item)


def edit_line():
    """
    Внесение изменений в строку таблицы.
    Автор: Болезнов С.А.
    """
    index = tab_control.index(tab_control.select())
    if index == 0:
        selected_item = goods_table.selection()[0]
        selected_line = goods_table.item(selected_item)['values']
        name_entry, description_entry, price_entry, category_entry = goods_dialog(selected_item,
                                                                                  selected_line)
        name_entry.insert(0, selected_line[1])
        description_entry.insert(0, selected_line[2])
        price_entry.set(selected_line[3])
        category_entry.insert(0, selected_line[4])
    if index == 1:
        selected_item = orders_table.selection()[0]
        selected_line = orders_table.item(selected_item)['values']
        date_day, date_month, date_year, sum_entry = orders_dialog(selected_item, selected_line)
        month, day, year = selected_line[1].split('/')
        date_day.set(day)
        date_month.set(month)
        date_year.set(year)
        sum_entry.set(selected_line[2])
    if index == 2:
        selected_item = orders_structure_table.selection()[0]
        selected_line = orders_structure_table.item(selected_item)['values']
        good_entry, quantity_entry = orders_structure_dialog(selected_item, selected_line)
        good_entry.set(selected_line[1])
        quantity_entry.set(selected_line[2])
    if index == 3:
        print('Данная операция невозможна. Данные можно изменять только в отдельных справочниках')


def goods_dialog(selected_item, selected_line) -> tuple[Entry, Entry, Spinbox, Entry]:
    """
    Создание нового окна с вводом новых/измененных значений для таблицы товары
    Автор: Болезнов С.А.
    :param selected_item: Выбранный объект в таблице
    :param selected_line: Список выбранных значений
    :return: Виджеты ввода значений
    """
    dialog = tk.Toplevel(root)
    dialog.title('Изменение товара')
    tk.Label(dialog, text="Название").grid(row=0, column=0, sticky="nesw", columnspan=2)
    name_entry = tk.Entry(dialog)
    name_entry.grid(row=1, column=0, sticky="nesw", columnspan=2)

    tk.Label(dialog, text="Описание").grid(row=2, column=0, sticky="nesw", columnspan=2)
    description_entry = tk.Entry(dialog)
    description_entry.grid(row=3, column=0, sticky="nesw", columnspan=2)

    tk.Label(dialog, text="Ценв").grid(row=4, column=0, sticky="nesw", columnspan=2)
    price_entry = ttk.Spinbox(dialog, increment=0.01, from_=0, to=1000)
    price_entry.grid(row=5, column=0, sticky="nesw", columnspan=2)

    tk.Label(dialog, text="Категория").grid(row=6, column=0, sticky="nesw", columnspan=2)
    category_entry = tk.Entry(dialog)
    category_entry.grid(row=7, column=0, sticky="nesw", columnspan=2)

    def save():
        """
        Функция для сохранения полученных значений
        Автор: Болезнов С.А.
        """
        name = name_entry.get()
        description = description_entry.get()
        price = price_entry.get()
        category = category_entry.get()
        values = [selected_line[0], name, description, price, category]
        goods_table.item(selected_item, values=values)
        dialog.destroy()
        global GOODS
        GOODS = replace_row_values(GOODS, selected_line, values)
        create_new_merge()

    save_button = ttk.Button(dialog, text='Сохранить', command=save)
    cancel_button = ttk.Button(dialog, text='Отмена', command=dialog.destroy)
    save_button.grid(row=8, column=0, sticky="nesw")
    cancel_button.grid(row=8, column=1, sticky="nesw")
    config_widgets(dialog, 9, 2)
    return name_entry, description_entry, price_entry, category_entry


def replace_row_values(df: pd.DataFrame, old_values: list, new_values: list) -> pd.DataFrame:
    """
    Функция для замены одной строки датафрейма на новую
    Автор: Болезнов С.А.
    :param df(pd.DataFrame): Исходный датафрейм
    :param old_values: Список значений, которые будут изсменены
    :param new_values: Список новых значений
    :return: Изменененный датафрейм
    """
    if 'Quantity' in df.columns:
        row_idx = (df['Order ID'] == old_values[0])
    elif 'Product ID' in df.columns:
        row_idx = (df['Product ID'] == old_values[0])
    elif 'Order ID' in df.columns:
        row_idx = (df['Order ID'] == old_values[0])
    df.loc[row_idx] = new_values
    return df


def orders_dialog(selected_item, selected_line):
    """
    Функция для создания нового окна с вводом новых/измененных значений для таблицы заказы
    Автор: Болезнов С.А.
    :param selected_item: Выбранный объект в таблице
    :param selected_line: Список выбранных значений
    :return: Виджеты ввода значений
    """
    dialog = tk.Toplevel(root)
    dialog.title('Изменение заказ')
    tk.Label(dialog, text='Дата').grid(column=0, row=0, columnspan=3, sticky="nesw")
    date_day = ttk.Spinbox(dialog, from_=1, to=31, width=2)
    date_day.grid(column=0, row=1, sticky="nesw")
    date_month = ttk.Spinbox(dialog, from_=1, to=12, width=2)
    date_month.grid(column=1, row=1, sticky="nesw")
    date_year = ttk.Spinbox(dialog, from_=2022, to=2023, width=4)
    date_year.grid(column=2, row=1, sticky="nesw")

    tk.Label(dialog, text="Сумма").grid(row=2, column=0, sticky="nesw", columnspan=3)
    sum_entry = ttk.Spinbox(dialog, increment=1, from_=0, to=100000)
    sum_entry.grid(row=3, column=0, sticky="nesw", columnspan=3)

    def save():
        """
        Функция для сохранения полученных значений
        Автор: Болезнов С.А.
        """
        date = f'{date_month.get()}/{date_day.get()}/{date_year.get()}'
        sum = sum_entry.get()
        values = [selected_line[0], date, sum]
        orders_table.item(selected_item, values=values)
        dialog.destroy()
        global ORDERS
        ORDERS = replace_row_values(ORDERS, selected_line, values)
        create_new_merge()

    save_button = ttk.Button(dialog, text='Сохранить', command=save)
    cancel_button = ttk.Button(dialog, text='Отмена', command=dialog.destroy)
    save_button.grid(row=8, column=0, sticky="nesw", columnspan=2)
    cancel_button.grid(row=8, column=2, sticky="nesw")
    config_widgets(dialog, 4, 3)
    return date_day, date_month, date_year, sum_entry


def create_new_merge():
    """
    Функция для обновления общей таблицы после внесения изменений в справочники
    Автор: Болезнов С.А.
    """
    global MERGED
    widgets_list = tab4.pack_slaves()
    for element in widgets_list:
        element.destroy()
    MERGED = merge_files(GOODS, ORDERS, ORDERS_STRUCTURE)
    create_table(tab4, MERGED)


def orders_structure_dialog(selected_item, selected_line):
    """
    Функция для создания нового окна с вводом новых/измененных значений для таблицы состав заказов
    Автор: Болезнов С.А.
    :param selected_item: Выбранный объект в таблице
    :param selected_line: Список выбранных значений
    :return: Виджеты ввода значений
    """
    dialog = tk.Toplevel(root)
    dialog.title('Изменение состава заказа')
    tk.Label(dialog, text='Товар').grid(column=0, row=0, sticky="nesw", columnspan=2)
    ids = list(GOODS['Product ID'])
    good_entry = ttk.Combobox(dialog, values=ids)
    good_entry.grid(column=0, row=1, sticky="nesw", columnspan=2)
    tk.Label(dialog, text="Количество").grid(row=2, column=0, sticky="nesw", columnspan=2)
    quantity_entry = ttk.Spinbox(dialog, increment=1, from_=0, to=100)
    quantity_entry.grid(row=3, column=0, sticky="nesw", columnspan=2)

    def save():
        """
        Функция для сохранения полученных значений
        Автор: Болезнов С.А.
        """
        good_id = int(good_entry.get())
        quantity = quantity_entry.get()
        values = [selected_line[0], good_id, quantity]
        orders_structure_table.item(selected_item, values=values)
        dialog.destroy()
        global ORDERS_STRUCTURE
        ORDERS_STRUCTURE = replace_row_values(ORDERS_STRUCTURE, selected_line, values)
        create_new_merge()

    save_button = ttk.Button(dialog, text='Сохранить', command=save)
    cancel_button = ttk.Button(dialog, text='Отмена', command=dialog.destroy)
    save_button.grid(row=4, column=0, sticky="nesw")
    cancel_button.grid(row=4, column=1, sticky="nesw")
    config_widgets(dialog, 5, 2)
    return good_entry, quantity_entry


def generate_id(index) -> int:
    """
    Функция для создания нового айди для справочников
    Автор: Болезнов С.А.
    """
    if index == 0:
        ids = [int(x) for x in GOODS['Product ID']]
        for i in range(1, max(ids) + 1):
            if i not in ids:
                return i
        return max(ids) + 1
    if index == 1:
        ids = [x for x in ORDERS['Order ID']]
        new_id = ids[0]
        while new_id in ids:
            first_part = np.random.randint(1, 100)
            second_part = np.random.randint(1, 1000)
            third_part = np.random.randint(1, 10000)
            new_id = f'{first_part}-{second_part}-{third_part}'
        return new_id


def add_order():
    """
    Функция для добавления заказа
    Автор: Болезнов С.А.
    """
    dialog = tk.Toplevel(root)
    dialog.title('Создание нового заказа')
    tk.Label(dialog, text='Дата').grid(column=0, row=0, columnspan=3, sticky="nesw")
    date_day = ttk.Spinbox(dialog, from_=1, to=31, width=2)
    date_day.grid(column=0, row=1, sticky="nesw")
    date_day.set(1)
    date_month = ttk.Spinbox(dialog, from_=1, to=12, width=2)
    date_month.grid(column=1, row=1, sticky="nesw")
    date_month.set(1)
    date_year = ttk.Spinbox(dialog, from_=2022, to=2023, width=4)
    date_year.grid(column=2, row=1, sticky="nesw")
    date_year.set(2022)

    tk.Label(dialog, text="Сумма").grid(row=2, column=0, sticky="nesw", columnspan=3)
    sum_entry = ttk.Spinbox(dialog, increment=1, from_=0, to=100000)
    sum_entry.set(1000)
    sum_entry.grid(row=3, column=0, sticky="nesw", columnspan=3)

    tk.Label(dialog, text='Товар').grid(column=0, row=4, sticky="nesw", columnspan=3)
    ids = list(GOODS['Product ID'])
    products = list(GOODS['Product'])
    good_entry = ttk.Combobox(dialog, values=products)
    good_entry.set(products[0])
    good_entry.grid(column=0, row=5, sticky="nesw", columnspan=3)
    tk.Label(dialog, text="Количество").grid(row=6, column=0, sticky="nesw", columnspan=3)
    quantity_entry = ttk.Spinbox(dialog, increment=1, from_=0, to=100)
    quantity_entry.set(5)
    quantity_entry.grid(row=7, column=0, sticky="nesw", columnspan=3)

    def save():
        """
        Функция для сохранения полученных данных
        Автор: Болезнов С.А.
        """
        date = f'{date_month.get()}/{date_day.get()}/{date_year.get()}'
        sum = sum_entry.get()
        quantity = quantity_entry.get()
        product = ids[products.index(good_entry.get())]
        order_id = generate_id(1)
        order_values = [order_id, date, sum]
        struct_values = [order_id, product, quantity]
        global ORDERS, ORDERS_STRUCTURE
        ORDERS = pd.concat([pd.DataFrame([order_values], columns=ORDERS.columns), ORDERS], ignore_index=True)
        ORDERS_STRUCTURE = pd.concat(
            [pd.DataFrame([struct_values], columns=ORDERS_STRUCTURE.columns), ORDERS_STRUCTURE],
            ignore_index=True)
        dialog.destroy()
        widgets_list = tab2.pack_slaves()
        for element in widgets_list:
            element.destroy()
        global orders_table, orders_structure_table
        orders_table = create_table(tab2, ORDERS)
        widgets_list = tab3.pack_slaves()
        for element in widgets_list:
            element.destroy()
        orders_structure_table = create_table(tab3, ORDERS_STRUCTURE)

    save_button = ttk.Button(dialog, text='Создать', command=save)
    cancel_button = ttk.Button(dialog, text='Отмена', command=dialog.destroy)
    save_button.grid(row=8, column=0, sticky="nesw", columnspan=2)
    cancel_button.grid(row=8, column=2, sticky="nesw")
    config_widgets(dialog, 9, 3)


def add_product():
    """
    Функция для добавления товара
    Автор: Болезнов С.А.
    """
    dialog = tk.Toplevel(root)
    dialog.title('Создание нового товара')
    tk.Label(dialog, text="Название").grid(row=0, column=0, sticky="nesw", columnspan=2)
    product_entry = tk.Entry(dialog)
    product_entry.grid(row=1, column=0, sticky="nesw", columnspan=2)

    tk.Label(dialog, text="Описание").grid(row=2, column=0, sticky="nesw", columnspan=2)
    description_entry = tk.Entry(dialog)
    description_entry.grid(row=3, column=0, sticky="nesw", columnspan=2)

    tk.Label(dialog, text="Цена").grid(row=4, column=0, sticky="nesw")
    sum_entry = ttk.Spinbox(dialog, increment=1, from_=0, to=100000)
    sum_entry.set(1000)
    sum_entry.grid(row=5, column=0, sticky="nesw", columnspan=2)

    tk.Label(dialog, text="Категория").grid(row=6, column=0, sticky="nesw")
    category_entry = tk.Entry(dialog)
    category_entry.grid(row=7, column=0, sticky="nesw", columnspan=2)

    def save():
        """
        Функция для сохранения полученных данных
        Автор: Болезнов С.А.
        """
        product = product_entry.get()
        description = description_entry.get()
        sum = sum_entry.get()
        category = category_entry.get()

        product_id = generate_id(0)
        product_values = [product_id, product, description, sum, category]
        global GOODS
        GOODS = pd.concat([pd.DataFrame([product_values], columns=GOODS.columns), GOODS], ignore_index=True)
        dialog.destroy()
        widgets_list = tab1.pack_slaves()
        for element in widgets_list:
            element.destroy()
        global goods_table
        goods_table = create_table(tab1, GOODS)

    save_button = ttk.Button(dialog, text='Создать', command=save)
    cancel_button = ttk.Button(dialog, text='Отмена', command=dialog.destroy)
    save_button.grid(row=8, column=0, sticky="nesw")
    cancel_button.grid(row=8, column=1, sticky="nesw")
    config_widgets(dialog, 9, 2)


def config_color():
    """
    Открытие палитры и изменение цвета
    Автор Ряднов И.М.
    """
    style = ttk.Style()
    color = colorchooser.askcolor(title="Выберите цвет фона")
    if color[1] is not None:
        style.configure("Treeview", background=color[1])
    update_ini_value('BackgroundColor', color[1])


def get_settings():
    """
    Чтение ini файла и применение полученных значений к приложению
    Автор Ряднов И.М.
    """
    config = read_ini_file().get('Settings')
    height = config.get('Height')
    width = config.get('Width')
    resize_h = config.get('ResizableHeight')
    resize_w = config.get('ResizableWidth')
    background_color = config.get('BackgroundColor')
    font_size = config.get('FontSize')
    font_family = config.get('FontFamily')
    font_style = config.get('FontStyle')
    cfg = [height,
           width,
           bool(resize_h),
           bool(resize_w),
           background_color,
           int(font_size),
           font_family,
           font_style]
    return cfg


settings = get_settings()

root = tk.Tk()
root.title("Редактор справочников")

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)

ttk.Style().configure("Treeview", background=settings[4],
                      foreground="black", fieldbackground="white", font=(settings[6], settings[5], settings[7]))

tab_control.add(tab1, text='Товары')
tab_control.add(tab2, text='Заказы')
tab_control.add(tab3, text='Состав заказов')
tab_control.add(tab4, text='Полная таблица')
tab_control.grid(column=0, row=0, rowspan=6, columnspan=2, sticky='nswe')

path = f'{os.getcwd()}\\data'
GOODS = pd.read_csv(f"{path}\MOCK_DATA_1.csv")
goods_table = create_table(tab1, GOODS)
ORDERS = pd.read_csv(f"{path}\MOCK_DATA_2.csv")
orders_table = create_table(tab2, ORDERS)
ORDERS_STRUCTURE = pd.read_csv(f"{path}\MOCK_DATA_3.csv")
orders_structure_table = create_table(tab3, ORDERS_STRUCTURE)
MERGED = merge_files(GOODS, ORDERS, ORDERS_STRUCTURE)
merged_table = create_table(tab4, MERGED)

ttk.Button(root, text='Текстовый отчёт', command=report_1).grid(column=2, row=0, sticky="nesw")
ttk.Button(root, text='Статистический отчёт', command=create_statistic_report).grid(column=2, row=1, sticky="nesw")
ttk.Button(root, text='Сводная таблица', command=create_pivot_table).grid(column=2, row=2, sticky="nesw")
ttk.Button(root, text='Гистограмма', command=create_hist).grid(column=2, row=3, sticky="nesw")
ttk.Button(root, text='Стобчатая диаграмма', command=create_bar).grid(column=2, row=4, sticky="nesw")
ttk.Button(root, text='Блочная диаграмма', command=lambda: report_price_by_category(GOODS)) \
    .grid(column=2, row=5, sticky="nesw")
ttk.Button(root, text='Диаграмма рассеяния', command=create_scatter).grid(column=2, row=6, sticky="nesw")
ttk.Button(root, text='Добавить заказ', command=add_order).grid(column=0, row=6, sticky='nesw')
ttk.Button(root, text='Добавить товар', command=add_product).grid(column=1, row=6, sticky='nesw')

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Сохранить", command=lambda: save_tables(GOODS, ORDERS, ORDERS_STRUCTURE))
file_menu.add_command(label="Сохранить как", command=new_save)
edit_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Изменить", menu=edit_menu)
edit_menu.add_command(label="Удалить запись", command=del_line)
edit_menu.add_command(label="Изменить запись", command=edit_line)
menu_bar.add_command(label='Изменить цвет', command=config_color)
config_widgets(root, 7, 3)
root.geometry(
    f"{settings[0]}x{settings[1]}".format(root.winfo_screenwidth() // 2 - 400, root.winfo_screenheight() // 2 - 300))
root.resizable(settings[2], settings[3])
root.mainloop()
