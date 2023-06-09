import tkinter as tk
from tkinter import ttk
import csv
import os


def load_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data


def create_table(tab, file_path):
    table_frame = ttk.Frame(tab)
    table_frame.pack(fill='both', expand=True)

    table = ttk.Treeview(table_frame)
    table.pack(side='left', fill='both', expand=True)
    table.configure(style='Treeview')

    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=table.yview)
    scrollbar.pack(side='right', fill='y')
    table.configure(yscroll=scrollbar.set)

    data = load_csv(file_path)
    heads = data[0]
    table['columns'] = heads
    table['show'] = 'headings'

    for header in heads:
        table.heading(header, text=header)
        table.column(header)

    for row in data[1:]:
        table.insert('', 'end', values=row)


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
    btn_1.grid(column=1, row=0, sticky="w")
    btn_2 = ttk.Button(root, text='Текстовый отчёт 2')
    btn_2.grid(column=1, row=1, sticky="w")
    btn_3 = ttk.Button(root, text='Текстовый отчёт 3')
    btn_3.grid(column=1, row=2, sticky="w")
    btn_4 = ttk.Button(root, text='Гистограмма')
    btn_4.grid(column=1, row=3, sticky="w")
    btn_5 = ttk.Button(root, text='Стобчатая диаграмма')
    btn_5.grid(column=1, row=4, sticky="w")
    btn_6 = ttk.Button(root, text='Boxplot')
    btn_6.grid(column=1, row=5, sticky="w")
    btn_7 = ttk.Button(root, text='Scatter')
    btn_7.grid(column=1, row=6, sticky="w")

root = tk.Tk()
root.title("CSV Viewer")

# Создаем вкладки
tab_control = ttk.Notebook(root)
# tab_control.configure(style='Treeview')
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
create_table(tab1, f"{path}\MOCK_DATA_1.csv")
create_table(tab2, f"{path}\MOCK_DATA_2.csv")
create_table(tab3, f"{path}\MOCK_DATA_3.csv")
add_reports()

mainmenu = tk.Menu(root, tearoff=0)
mainmenu.add_command(label="Загрузить данные", command=add_color_change)


#mainmenu.add_command(label="Составить отчёт", command = doc)
mainmenu.add_command(label="Выход", command = root.destroy)

root.config(menu=mainmenu)

root.mainloop()
