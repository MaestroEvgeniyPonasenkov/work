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
    ftypes = [('csv', '.csv'), ('excel', '.xlsx'), ('doc', '.doc'), ('pickle', '.pickle')]
    filepath = fld.asksaveasfilename(filetypes=ftypes, initialdir=path, defaultextension='csv')
    if filepath != "":
        file_format = filepath.split('.')[-1]
        if file_format == 'csv':
            table.to_csv(filepath, index=False)
            return
        if file_format == 'xlsx':
            table.to_excel(filepath, index=False)
            return
        if file_format == 'doc':
            #table.to_doc
            return
        if file_format == 'pick':
            table.to_pickle(filepath)
            return

