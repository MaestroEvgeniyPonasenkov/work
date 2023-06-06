import os
import pandas as pd

os.chdir("c:/work")
path = f'{os.getcwd()[:-7]}data'
csv_file1 = f'{path}\MOCK_DATA_1.csv'
csv_file2 = f'{path}\MOCK_DATA_2.csv'
csv_file3 = f'{path}\MOCK_DATA_3.csv'

PRODUCT = pd.read_csv(csv_file1, delimiter=',', encoding='utf8')
ORDERS = pd.read_csv(csv_file2, delimiter=',', encoding='utf8')
TOTAL_ORDERS = pd.read_csv(csv_file3, delimiter=',', encoding='utf8')

merged = pd.merge(TOTAL_ORDERS, PRODUCT, on="Product ID")
merged = pd.merge(merged, ORDERS, on="Order ID")
merged['Date'] = merged['Date'].astype("datetime64[ns]")


def report_about_firm(start_date, end_date, category):
    """
    Текстовый отчёт о продажах фирмы за определённый период

    Parameters
    ----------
    start_date (str) : дата начала периода
    end_date (str): дата конца периода
    category (str): фирма

    Returns
    -------
    result (pandas.DataFrame): полученный отчёт

    """
    selector = (merged['Date'].between(start_date, end_date)) & (
        merged['Category'] == category)
    result = merged.loc[selector, ['Product',
                                   'Description', 'Price', 'Quantity', 'Sum']]

    result.to_excel("./output/report1.xlsx", index=False)
    return result


def report_about_firm_with_sum(start_date, end_date, category, summa):
    """
    Текстовый отчёт о чеках выше какой-то суммы определенной 
    фирмы за данный период.

    Parameters
    ----------
    start_date (str) : дата начала периода
    end_date (str): дата конца периода
    category (str): фирма
    summa (int): минимальная сумма чека
    Returns
    -------
    result (pandas.DataFrame): полученный отчёт

    """
    selector = (merged['Date'].between(start_date, end_date)) & (merged['Category'] == category) & (
        merged['Sum'] >= summa)
    result = merged.loc[selector, ['Product',
                                   'Description', 'Price', 'Quantity', 'Sum']]
    result.to_excel("./output/report2.xlsx", index=False)
    return result


def report_about_product(start_date, end_date, product, category):
    """
    Текстовый отчёт о продажах определенного препарата отдельной фирмы
    за данный период.

    Parameters
    ----------
    start_date (str) : дата начала периода
    end_date (str): дата конца периода
    product (str): препарат
    category (str): фирма

    Returns
    -------
    result (pandas.DataFrame): полученный отчёт

    """
    selector = (merged['Date'].between(start_date, end_date)) & (merged['Category'] == category) & (
        merged['Product'] == product)
    result = merged.loc[selector, ['Product',
                                   'Description', 'Price', 'Quantity', 'Sum']]
    result.to_excel("./output/report3.xlsx", index=False)
    return result


rep1 = report_about_firm('2022-09-01', '2023-01-01', 'Novartis')
rep2 = report_about_firm_with_sum('2022-09-01', '2023-04-01', 'Novartis', 3000)
rep3 = report_about_product(
    '2022-05-01', '2023-04-01', 'Alprazolam', 'Novartis')
