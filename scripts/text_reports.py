import os
import pandas as pd


def merge_files():
    path = f'{os.getcwd()}/data'
    csv_file1 = f'{path}\MOCK_DATA_1.csv'
    csv_file2 = f'{path}\MOCK_DATA_2.csv'
    csv_file3 = f'{path}\MOCK_DATA_3.csv'
    PRODUCT = pd.read_csv(csv_file1, delimiter=',', encoding='utf8')
    ORDERS = pd.read_csv(csv_file2, delimiter=',', encoding='utf8')
    TOTAL_ORDERS = pd.read_csv(csv_file3, delimiter=',', encoding='utf8')
    merged = pd.merge(TOTAL_ORDERS, PRODUCT, on="Product ID")
    merged = pd.merge(merged, ORDERS, on="Order ID")
    merged['Date'] = merged['Date'].astype("datetime64[ns]")
    return merged


def report_about_firm(merged, start_date, end_date, category):
    selector = (merged['Date'].between(start_date, end_date)) & (
        merged['Category'] == category)
    result = merged.loc[selector, ['Product',
                                   'Description', 'Price', 'Quantity', 'Sum']]
    #result.to_excel("./output/report1.xlsx", index=False)
    return result


def report_about_firm_with_sum(merged, start_date, end_date, category, summa):
    selector = (merged['Date'].between(start_date, end_date)) & (merged['Category'] == category) & (
        merged['Sum'] >= summa)
    result = merged.loc[selector, ['Product',
                                   'Description', 'Price', 'Quantity', 'Sum']]
    result.to_excel("./output/report2.xlsx", index=False)
    return result


def report_about_product(merged, start_date, end_date, product, category):
    selector = (merged['Date'].between(start_date, end_date)) & (merged['Category'] == category) & (
        merged['Product'] == product)
    result = merged.loc[selector, ['Product',
                                   'Description', 'Price', 'Quantity', 'Sum']]
    result.to_excel("./output/report3.xlsx", index=False)
    return result
