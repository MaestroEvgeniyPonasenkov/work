import pandas as pd


def merge_files(PRODUCT, ORDERS, TOTAL_ORDERS):
    merged = pd.merge(TOTAL_ORDERS, PRODUCT, on="Product ID")
    merged = pd.merge(merged, ORDERS, on="Order ID")
    return merged


def report_about_firm(merged, start_date, end_date, category):
    merged['Date'] = merged['Date'].astype("datetime64[ns]")
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
