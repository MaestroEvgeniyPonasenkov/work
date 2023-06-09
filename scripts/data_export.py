import os

import pandas as pd
from tkinter import filedialog as fld


def export_to_xlsx(df, fname):
    df.to_excel(f'{fname}.xlsx', index=False)


def save_tables(GOODS: pd.DataFrame, ORDERS: pd.DataFrame, ORDERS_STRUCTURE: pd.DataFrame) -> None:
    path = path = f'{os.getcwd()[:-7]}data'
    GOODS.to_csv(f'{path}/MOCK_DATA_1.csv', index=False)
    ORDERS.to_csv(f'{path}/MOCK_DATA_2.csv', index=False)
    ORDERS_STRUCTURE.to_csv(f'{path}/MOCK_DATA_3.csv', index=False)


def save_as(table: pd.DataFrame) -> None:
    path = f'{os.getcwd()[:-7]}data'
    ftypes = [('csv файлы', '.csv'), ('Все файлы', '*')]
    filepath = fld.asksaveasfilename(filetypes=ftypes, initialdir=path, defaultextension='csv')
    print(filepath)
    if filepath != "":
        table.to_csv(filepath, index=False)
