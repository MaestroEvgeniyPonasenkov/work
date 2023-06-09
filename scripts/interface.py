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


def add_color_change(root):
    # Создаем кнопку для изменения цвета
    color_label = ttk.Label(root, text='Цвет фона (RGB):')
    color_label.pack()
    color_entry = ttk.Entry(root)
    color_entry.pack()

    def change_color():
        color = color_entry.get()
        root.configure(background=color)
        ttk.Style().configure("Treeview", background=color, fieldbackground=color,
                              foreground="black")

    color_button = ttk.Button(root, text='Изменить цвет', command=change_color)
    color_button.pack()



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

tab_control.pack(expand=1, fill='both')
# Создаем таблицы для каждой вкладки
path = f'{os.getcwd()[:-7]}data'
create_table(tab1, f"{path}\MOCK_DATA_1.csv")
create_table(tab2, f"{path}\MOCK_DATA_2.csv")
create_table(tab3, f"{path}\MOCK_DATA_3.csv")
#add_color_change(root)

root.mainloop()


