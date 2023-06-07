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

    scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=table.yview)
    scrollbar.pack(side='right', fill='y')

    table.configure(yscroll=scrollbar.set)

    data = load_csv(file_path)
    table['columns'] = range(len(data[0]))
    table['show'] = 'headings'

    for i in range(len(data[0])):
        table.heading(i, text=data[0][i])
        table.column(i, width=100, anchor='center')

    for row in data[1:]:
        table.insert('', 'end', values=row)


def change_color():
    color = color_entry.get()
    root.configure(background=color)

root = tk.Tk()
root.title("CSV Viewer")

# Создаем вкладки
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Таблица 1')
tab_control.add(tab2, text='Таблица 2')
tab_control.add(tab3, text='Таблица 3')

tab_control.pack(expand=1, fill='both')

# Создаем кнопку для изменения цвета
color_label = ttk.Label(root, text='Цвет фона (RGB):')
color_label.pack()
color_entry = ttk.Entry(root)
color_entry.pack()
color_button = ttk.Button(root, text='Изменить цвет', command=change_color)
color_button.pack()

# Создаем таблицы для каждой вкладки
create_table(tab1, f"{os.getcwd()}\data\MOCK_DATA_1.csv")
create_table(tab2, f"{os.getcwd()}\data\MOCK_DATA_2.csv")
create_table(tab3, f"{os.getcwd()}\data\MOCK_DATA_3.csv")

root.mainloop()