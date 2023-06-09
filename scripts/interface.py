import tkinter as tk
from tkinter import ttk
from data_export import save_tables, save_as
import os
import pandas as pd


def create_table(tab, file_path):
    table_frame = ttk.Frame(tab)
    table_frame.pack(fill='both', expand=True)

    table = ttk.Treeview(table_frame)
    table.pack(side='left', fill='both', expand=True)
    table.configure(style='Treeview')

    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=table.yview)
    scrollbar.pack(side='right', fill='y')
    table.configure(yscroll=scrollbar.set)

    data = pd.read_csv(file_path)
    heads = list(data.columns)
    table['columns'] = heads
    table['show'] = 'headings'

    for header in heads:
        table.heading(header, text=header)
        table.column(header)

    for i, row in data.iterrows():
        values = list(row)
        table.insert("", "end", text=i, values=values)
    return data


def add_color_change():
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


def add_reports():
    btn_1 = ttk.Button(root, text='Текстовый отчёт 1')
    btn_1.grid(column=1, row=0, sticky="nesw")
    btn_2 = ttk.Button(root, text='Текстовый отчёт 2')
    btn_2.grid(column=1, row=1, sticky="nesw")
    btn_3 = ttk.Button(root, text='Текстовый отчёт 3')
    btn_3.grid(column=1, row=2, sticky="nesw")
    btn_4 = ttk.Button(root, text='Гистограмма')
    btn_4.grid(column=1, row=3, sticky="nesw")
    btn_5 = ttk.Button(root, text='Стобчатая диаграмма')
    btn_5.grid(column=1, row=4, sticky="nesw")
    btn_6 = ttk.Button(root, text='Boxplot')
    btn_6.grid(column=1, row=5, sticky="nesw")
    btn_7 = ttk.Button(root, text='Scatter')
    btn_7.grid(column=1, row=6, sticky="nesw")


def save2():
    index = tab_control.index(tab_control.select())
    table = tabs[index]
    save_as(table)


root = tk.Tk()
root.title("CSV Viewer")

# Создаем вкладки
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

# Создаем таблицы для каждой вкладкиэ
path = f'{os.getcwd()[:-7]}data'
GOODS = create_table(tab1, f"{path}\MOCK_DATA_1.csv")
ORDERS = create_table(tab2, f"{path}\MOCK_DATA_2.csv")
ORDERS_STRUCTURE = create_table(tab3, f"{path}\MOCK_DATA_3.csv")
tabs = [GOODS, ORDERS, ORDERS_STRUCTURE]
add_reports()

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Сохранить", command=lambda x=tabs[0], y=tabs[1], z=tabs[2]: save_tables(x, y, z))
file_menu.add_command(label="Сохранить как", command=save2)

edit_menu = tk.Menu(menu_bar)
menu_bar.add_cascade(label="Изменить", menu=edit_menu)

edit_menu.add_command(label="Удалить запись")
edit_menu.add_command(label="Добавить запись")
edit_menu.add_command(label="Изменить запись")

for c in range(1):
    root.columnconfigure(index=c, weight=1)
for r in range(7):
    root.rowconfigure(index=r, weight=1)

root.mainloop()
