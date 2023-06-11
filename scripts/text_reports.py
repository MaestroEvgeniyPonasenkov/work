import pandas as pd
import numpy as np


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
    # result.to_excel("./output/report1.xlsx", index=False)
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


def generate_frequency_table(data, attribute):
    freq_table = data[attribute].value_counts().reset_index()
    freq_table.columns = [attribute, 'Частота']
    freq_table['Процент'] = (
        freq_table['Частота'] / len(data)) * 100
    return freq_table


def generate_descriptive_stats(data, attribute):
    descriptive_stats = data[attribute].describe().reset_index()
    descriptive_stats.columns = ['Статистика', attribute]
    descriptive_stats['Статистика'] = descriptive_stats['Статистика'].replace({
        'count': 'Количество непропущенных значений',
        'mean': 'Среднее значение',
        'max': 'Максимум',
        'std': 'стандартное отклонение',
        'min': 'Минимум',
        '25%': 'первый квартиль',
        '50%': 'медиана',
        '75%': 'третий квартиль',
        'unique': 'количество уникальных значений',
        'top': 'наиболее часто встречающееся значение',
        'freq': 'количество раз, которое top значение встречается'
    })
    if np.issubdtype(data[attribute].dtype, np.number):
        sample_variance = data[attribute].var()
        descriptive_stats.loc[len(descriptive_stats)] = ['Выборочная дисперсия', sample_variance]
    return descriptive_stats


def generate_attribute_report(data, attribute1, attribute2):
    freq_table1 = generate_frequency_table(data, attribute1)
    stats_table1 = generate_descriptive_stats(data, attribute1)
    freq_table2 = generate_frequency_table(data, attribute2)
    stats_table2 = generate_descriptive_stats(data, attribute2)
    return (freq_table1, stats_table1, freq_table2, stats_table2)
