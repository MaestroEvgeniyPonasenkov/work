import tkinter as tk
from tkinter import ttk, Spinbox
from tkinter.ttk import Treeview, Scrollbar
from typing import Tuple

from text_reports import report_about_firm, merge_files
from hist_chart import histogram
from bar_chart import report_day_sales, report_week_sales, report_year_sales, report_month_sales
from boxplot_chart import report_price_by_category
from scatter_chart import report_price_by_quantity
from data_export import save_tables, save_as
import os
import pandas as pd
import numpy as np


def create_pivot_table():
    dialog = tk.Toplevel(root)
    dialog.title("Сводная таблица")

    tk.Label(dialog, text="Выберите значения (values):").grid(row=0, column=0, sticky="nesw")
    values_entry = ttk.Combobox(dialog, values=['None'] + list(MERGED.columns), state='readonly')
    values_entry.grid(row=1, column=0, sticky="nesw")

    tk.Label(dialog, text="Выберите индекс (index):").grid(row=0, column=1, sticky="nesw")
    index_entry = ttk.Combobox(dialog, values=['None'] + list(MERGED.columns), state='readonly')
    index_entry.grid(row=1, column=1, sticky="nesw")

    tk.Label(dialog, text="Выберите столбцы (columns):").grid(row=0, column=2, sticky="nesw")
    columns_entry = ttk.Combobox(dialog, values=['None'] + list(MERGED.columns), state='readonly')
    columns_entry.grid(row=1, column=2, sticky="nesw")

    def create_pivot_table():
        values = values_entry.get()
        index = index_entry.get()
        columns = columns_entry.get()

        try:
            pivot_data = pd.pivot_table(MERGED,
                                        values=values if values != 'None' else None,
                                        index=index if index != 'None' else None,
                                        columns=columns if columns != 'None' else None,
                                        aggfunc=np.sum)
            dialog2 = tk.Toplevel(root)
            dialog2.title("Сводная таблица")
            create_table(dialog2, pivot_data, True)
        except Exception:
            print("Данные не подходят для создания сводной таблицы")

    tk.Button(dialog, text="Создать таблицу", command=create_pivot_table).grid(row=2, column=0, columnspan=3,
                                                                               sticky="nesw")
    config_widgets(dialog, 3, 3)


def create_table(tab, data: pd.DataFrame, pivot=False) -> tuple[Treeview, Scrollbar]:
    """
    Функция для добавления таблицы в окно
    :param tab: Название окна
    :param data(pd.DataFrame): Данные таблицы
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
    heads = [translater[x] for x in data.columns]
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
    return table, scrollbar


def add_color_change():
    """
    Хуйня из-под коня, надо переделать
    """
    # Создаем кнопку для изменения цвета
    color_label = ttk.Label(root, text='Цвет фона (RGB):')
    color_label.grid(column=1, row=0, sticky='nswe')
    color_entry = ttk.Entry(root)
    color_entry.grid(column=1, row=1, sticky='nswe')

    def change_color():
        color = color_entry.get()
        root.configure(background=color)
        ttk.Style().configure("Treeview", background=color, fieldbackground=color,
                              foreground="black")

    color_button = ttk.Button(root, text='Изменить цвет', command=change_color)
    color_button.grid(column=1, row=2, sticky='nswe')


def new_save():
    """
    Функция для сохранения одной таблицы
    :return:
    """
    index = tab_control.index(tab_control.select())
    tabs = [GOODS, ORDERS, ORDERS_STRUCTURE, MERGED]
    table = tabs[index]
    save_as(table)


def get_current_table_name():
    index = tab_control.index(tab_control.select())
    tabs = [GOODS, ORDERS, ORDERS_STRUCTURE, MERGED]
    table = tabs[index]


def add_datas(parent) -> tuple[Spinbox, Spinbox, Spinbox, Spinbox, Spinbox, Spinbox]:
    """
    Функция для добавления в окно полей ввода даты
    :param parent: Название окна
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
    Создание нового окна для ввода необходимых параметров
    """
    dialog = tk.Toplevel(root)
    dialog.title("Текстовый отчёт 1")
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
        """
        first_date = f'{start_date_year.get()}-{start_date_month.get()}-{start_date_day.get()}'
        second_date = f'{end_date_year.get()}-{end_date_month.get()}-{end_date_day.get()}'
        category = firm_entry.get()

        report = report_about_firm(MERGED, first_date, second_date, category)
        dialog.destroy()
        dialog2 = tk.Toplevel(root)
        dialog2.title(f"Текстовый отчёт о продажах {category}")
        tab_control = ttk.Notebook(root)
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Товары')
        dialog2.columnconfigure(index=0, weight=1)
        dialog2.rowconfigure(index=0, weight=1)
        create_table(dialog2, report)

    tk.Button(dialog, text="Создать", command=ok_button).grid(row=6, column=0, columnspan=2, sticky="nesw")
    tk.Button(dialog, text='Отменить', command=dialog.destroy).grid(row=6, column=2, sticky='nsew')


def report_2():
    pass


def create_hist():
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


def create_boxplot():
    report_price_by_category(GOODS)


def create_scatter():
    data = pd.merge(ORDERS_STRUCTURE, GOODS, on="Product ID")
    data['Price'] = data['Price'].astype(float)
    report_price_by_quantity(data)


def del_line():
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
    index = tab_control.index(tab_control.select())
    if index == 0:
        selected_item = goods_table.selection()[0]
        selected_line = goods_table.item(selected_item)['values']
        name_entry, description_entry, price_entry, category_entry = goods_dialog(selected_item, selected_line[0])
        name_entry.insert(0, selected_line[1])
        description_entry.insert(0, selected_line[2])
        price_entry.set(selected_line[3])
        category_entry.insert(0, selected_line[4])
    if index == 1:
        selected_item = orders_table.selection()[0]
        selected_line = orders_table.item(selected_item)['values']
        date_day, date_month, date_year, sum_entry = orders_dialog(selected_item, selected_line[0])
        month, day, year = selected_line[1].split('/')
        date_day.set(day)
        date_month.set(month)
        date_year.set(year)
        sum_entry.set(selected_line[2])

    if index == 2:
        selected_item = orders_structure_table.selection()[0]
        selected_line = orders_structure_table.item(selected_item)['values']
        good_entry, quantity_entry = orders_structure_dialog(selected_item, selected_line[0])
        good_entry.set(selected_line[1])
        quantity_entry.set(selected_line[2])
    if index == 3:
        print('Так нельзя')


def goods_dialog(selected_item, id):
    dialog = tk.Toplevel(root)
    dialog.title('Товар')
    tk.Label(dialog, text="Название").grid(row=0, column=0, sticky="nesw", columnspan=2)
    name_entry = tk.Entry(dialog)
    name_entry.grid(row=1, column=0, sticky="nesw", columnspan=2)

    tk.Label(dialog, text="Описание").grid(row=2, column=0, sticky="nesw", columnspan=2)
    description_entry = tk.Entry(dialog)
    description_entry.grid(row=3, column=0, sticky="nesw", columnspan=2)

    tk.Label(dialog, text="Название").grid(row=4, column=0, sticky="nesw", columnspan=2)
    price_entry = ttk.Spinbox(dialog, increment=0.01, from_=0, to=1000)
    price_entry.grid(row=5, column=0, sticky="nesw", columnspan=2)

    tk.Label(dialog, text="Категория").grid(row=6, column=0, sticky="nesw", columnspan=2)
    category_entry = tk.Entry(dialog)
    category_entry.grid(row=7, column=0, sticky="nesw", columnspan=2)

    def save():
        name = name_entry.get()
        description = description_entry.get()
        price = price_entry.get()
        category = category_entry.get()
        values = [id, name, description, price, category]
        goods_table.item(selected_item, values=values)
        dialog.destroy()
        global MERGED, merged_table
        MERGED = merge_files(GOODS, ORDERS, ORDERS_STRUCTURE)
        merged_table = create_table(tab4, MERGED)

    save_button = ttk.Button(dialog, text='Сохранить', command=save)
    cancel_button = ttk.Button(dialog, text='Отмена', command=dialog.destroy)
    save_button.grid(row=8, column=0, sticky="nesw")
    cancel_button.grid(row=8, column=1, sticky="nesw")
    config_widgets(dialog, 9, 2)
    return name_entry, description_entry, price_entry, category_entry


def orders_dialog(selected_item, id):
    dialog = tk.Toplevel(root)
    dialog.title('Заказ')
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
        date = f'{date_month.get()}/{date_day.get()}/{date_year.get()}'
        sum = sum_entry.get()
        values = [id, date, sum]
        orders_table.item(selected_item, values=values)
        dialog.destroy()
        global MERGED, merged_table
        MERGED = merge_files(GOODS, ORDERS, ORDERS_STRUCTURE)
        merged_table = create_table(tab4, MERGED)

    save_button = ttk.Button(dialog, text='Сохранить', command=save)
    cancel_button = ttk.Button(dialog, text='Отмена', command=dialog.destroy)
    save_button.grid(row=8, column=0, sticky="nesw", columnspan=2)
    cancel_button.grid(row=8, column=2, sticky="nesw")
    config_widgets(dialog, 4, 3)
    return date_day, date_month, date_year, sum_entry


def orders_structure_dialog(selected_item, id):
    dialog = tk.Toplevel(root)
    dialog.title('Состав заказа')
    tk.Label(dialog, text='Товар').grid(column=0, row=0, sticky="nesw", columnspan=2)
    ids = list(GOODS['Product ID'])
    good_entry = ttk.Combobox(dialog, values=ids)
    good_entry.grid(column=0, row=1, sticky="nesw", columnspan=2)
    tk.Label(dialog, text="Количество").grid(row=2, column=0, sticky="nesw", columnspan=2)
    quantity_entry = ttk.Spinbox(dialog, increment=1, from_=0, to=100)
    quantity_entry.grid(row=3, column=0, sticky="nesw", columnspan=2)

    def save():
        good = good_entry.get()
        quantity = quantity_entry.get()
        values = [id, good, quantity]
        orders_structure_table.item(selected_item, values=values)
        dialog.destroy()
        global MERGED, merged_table
        merged_table.pack_forget()
        merged_scroll.pack_forget()
        MERGED = merge_files(GOODS, ORDERS, ORDERS_STRUCTURE)
        merged_table = create_table(tab4, MERGED)

    save_button = ttk.Button(dialog, text='Сохранить', command=save)
    cancel_button = ttk.Button(dialog, text='Отмена', command=dialog.destroy)
    save_button.grid(row=4, column=0, sticky="nesw")
    cancel_button.grid(row=4, column=1, sticky="nesw")
    config_widgets(dialog, 5, 2)
    return good_entry, quantity_entry


def add_line():
    pass


def config_color():
    pass


root = tk.Tk()
root.title("Редактор справочников")

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)

ttk.Style().configure("Treeview", background="white",
                      foreground="black", fieldbackground="white")

tab_control.add(tab1, text='Товары')
tab_control.add(tab2, text='Заказы')
tab_control.add(tab3, text='Состав заказов')
tab_control.add(tab4, text='Полная таблица')
tab_control.grid(column=0, row=0, rowspan=7, sticky='nswe')

path = f'{os.getcwd()}\\data'
GOODS = pd.read_csv(f"{path}\MOCK_DATA_1.csv")
goods_table, goods_scroll = create_table(tab1, GOODS)
ORDERS = pd.read_csv(f"{path}\MOCK_DATA_2.csv")
orders_table, order_scroll = create_table(tab2, ORDERS)
ORDERS_STRUCTURE = pd.read_csv(f"{path}\MOCK_DATA_3.csv")
orders_structure_table, orders_structure_scroll = create_table(tab3, ORDERS_STRUCTURE)
MERGED = merge_files(GOODS, ORDERS, ORDERS_STRUCTURE)
merged_table, merged_scroll = create_table(tab4, MERGED)

btn_1 = ttk.Button(root, text='Текстовый отчёт', command=report_1)
btn_1.grid(column=1, row=0, sticky="nesw")
btn_2 = ttk.Button(root, text='Статистический отчёт', command=report_2)
btn_2.grid(column=1, row=1, sticky="nesw")
btn_3 = ttk.Button(root, text='Сводная таблица', command=create_pivot_table)
btn_3.grid(column=1, row=2, sticky="nesw")
btn_4 = ttk.Button(root, text='Гистограмма', command=create_hist)
btn_4.grid(column=1, row=3, sticky="nesw")
btn_5 = ttk.Button(root, text='Стобчатая диаграмма', command=create_bar)
btn_5.grid(column=1, row=4, sticky="nesw")
btn_6 = ttk.Button(root, text='Boxplot', command=create_boxplot)
btn_6.grid(column=1, row=5, sticky="nesw")
btn_7 = ttk.Button(root, text='Scatter', command=create_scatter)
btn_7.grid(column=1, row=6, sticky="nesw")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Сохранить", command=lambda: save_tables(GOODS, ORDERS, ORDERS_STRUCTURE))
file_menu.add_command(label="Сохранить как", command=new_save)
edit_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Изменить", menu=edit_menu)
edit_menu.add_command(label="Удалить запись", command=del_line)
edit_menu.add_command(label="Добавить запись", command=add_line)
edit_menu.add_command(label="Изменить запись", command=edit_line)
menu_bar.add_command(label='Изменить цвет', command=config_color)
config_widgets(root, 7, 2)
root.mainloop()
