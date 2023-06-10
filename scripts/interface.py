import tkinter as tk
from tkinter import ttk, Spinbox
from text_reports import report_about_firm

from data_export import save_tables, save_as
import os
import pandas as pd


def create_table(tab, data: pd.DataFrame) -> None:
    """
    Функция для добавления таблицы в окно
    :param tab: Название окна
    :param data(pd.DataFrame): Данные таблицы
    """
    table_frame = ttk.Frame(tab)
    table_frame.pack(fill='both', expand=True)

    table = ttk.Treeview(table_frame)
    table.pack(side='left', fill='both', expand=True)
    table.configure(style='Treeview')

    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=table.yview)
    scrollbar.pack(side='right', fill='y')
    table.configure(yscroll=scrollbar.set)

    heads = list(data.columns)
    table['columns'] = heads
    table['show'] = 'headings'

    for header in heads:
        table.heading(header, text=header)
        table.column(header)

    for i, row in data.iterrows():
        values = list(row)
        table.insert("", "end", text=i, values=values)


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
    tabs = [GOODS, ORDERS, ORDERS_STRUCTURE]
    table = tabs[index]
    save_as(table)


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
    start_date_year = tk.Spinbox(parent, from_=2000, to=2022, width=4)
    start_date_year.grid(column=2, row=1, sticky="nesw")

    end_date_label = tk.Label(parent, text='Выберите конечную дату:')
    end_date_label.grid(column=0, row=2, columnspan=3, sticky="nesw")
    end_date_day = tk.Spinbox(parent, from_=1, to=31, width=2)
    end_date_day.grid(column=0, row=3, sticky="nesw")
    end_date_month = tk.Spinbox(parent, from_=1, to=12, width=2)
    end_date_month.grid(column=1, row=3, sticky="nesw")
    end_date_year = tk.Spinbox(parent, from_=2000, to=2022, width=4)
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

        report = report_about_firm(first_date, second_date, category)
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


def report_3():
    pass


def create_hist():
    pass


def create_bar():
    pass


def create_boxplot():
    pass


def create_scatter():
    pass


def del_line():
    pass


def edit_line():
    pass


def add_line():
    pass


def config_color():
    pass


root = tk.Tk()
root.title("CSV Viewer")

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

ttk.Style().configure("Treeview", background="white",
                      foreground="black", fieldbackground="white")

tab_control.add(tab1, text='Товары')
tab_control.add(tab2, text='Заказы')
tab_control.add(tab3, text='Состав заказов')

tab_control.grid(column=0, row=0, rowspan=7, sticky='nswe')
root.columnconfigure(index=0, weight=1)
root.rowconfigure(index=0, weight=1)

path = f'{os.getcwd()}\\data'
GOODS = pd.read_csv(f"{path}\MOCK_DATA_1.csv")
create_table(tab1, GOODS)
ORDERS = pd.read_csv(f"{path}\MOCK_DATA_2.csv")
create_table(tab2, ORDERS)
ORDERS_STRUCTURE = pd.read_csv(f"{path}\MOCK_DATA_3.csv")
create_table(tab3, ORDERS_STRUCTURE)

btn_1 = ttk.Button(root, text='Текстовый отчёт 1', command=report_1)
btn_1.grid(column=1, row=0, sticky="nesw")
btn_2 = ttk.Button(root, text='Текстовый отчёт 2', command=report_2)
btn_2.grid(column=1, row=1, sticky="nesw")
btn_3 = ttk.Button(root, text='Текстовый отчёт 3', command=report_3)
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
config_widgets(root, 2, 8)

root.mainloop()
