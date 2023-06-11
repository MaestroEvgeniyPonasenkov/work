import pandas as pd
import numpy as np


def merge_files(PRODUCT, ORDERS, TOTAL_ORDERS):
    """
    Мердж данных
    :param PRODUCT(pd.DataFrame): датафрейм с товарами
    :param ORDERS(pd.DataFrame): датафрейм с заказами
    :param TOTAL_ORDERS(pd.DataFrame): датафрейм со всеми заказами
    Автор: Ряднов И.М.
    """
    merged = pd.merge(TOTAL_ORDERS, PRODUCT, on="Product ID")
    merged = pd.merge(merged, ORDERS, on="Order ID")
    return merged


def report_about_firm(merged, start_date, end_date, category):
    """
    отчет о продажах товаров выбранной компании за выбранный временной промежуток
    :param merged(pd.DataFrame): датафрейм со всеми данными
    :param start_date(str): начальная дата
    :param end_date(str): конечная дата
    :param category(str): категория
    Автор: Ряднов И.М.
    """
    merged['Date'] = merged['Date'].astype("datetime64[ns]")
    selector = (merged['Date'].between(start_date, end_date)) & (
        merged['Category'] == category)
    result = merged.loc[selector, ['Product',
                                   'Description', 'Price', 'Quantity', 'Sum']]
    return result


def generate_frequency_table(data, attribute):
    """
    отчет о частоте встречаемости атрибута
    :param data(pd.DataFrame): датафрейм со всеми данными
    :param attribute(str): имя атрибута
    Автор: Ряднов И.М.
    """
    freq_table = data[attribute].value_counts().reset_index()
    freq_table.columns = [attribute, 'Частота']
    freq_table['Процент'] = (
        freq_table['Частота'] / len(data)) * 100
    return freq_table


def generate_descriptive_stats(data, attribute):
    """
    отчет-описание атрибутов
    :param data(pd.DataFrame): датафрейм со всеми данными
    :param attribute(str): имя атрибута
    Автор: Ряднов И.М.
    """
    descriptive_stats = data[attribute].describe().reset_index()
    descriptive_stats.columns = ['Статистика', attribute]
    descriptive_stats['Статистика'] = descriptive_stats['Статистика'].replace({
        'count': 'Количество непропущенных значений',
        'mean': 'Среднее значение',
        'max': 'Максимум',
        'std': 'Стандартное отклонение',
        'min': 'Минимум',
        '25%': 'Первый квартиль',
        '50%': 'Медиана',
        '75%': 'Третий квартиль',
        'unique': 'Количество уникальных значений',
        'top': 'Наиболее часто встречающееся значение',
        'freq': 'Количество раз, которое top значение встречается'
    })
    if np.issubdtype(data[attribute].dtype, np.number):
        sample_variance = data[attribute].var()
        descriptive_stats.loc[len(descriptive_stats)] = ['Выборочная дисперсия', sample_variance]
    return descriptive_stats


def generate_attribute_report(data, attribute1, attribute2):
    """
    генерация отчётов о паре атрибутов
    :param data(pd.DataFrame): датафрейм со всеми данными
    :param attribute1(str): имя первого атрибута
    :param attribute2(str): имя второго атрибута
    Автор: Ряднов И.М.
    """
    freq_table1 = generate_frequency_table(data, attribute1)
    stats_table1 = generate_descriptive_stats(data, attribute1)
    freq_table2 = generate_frequency_table(data, attribute2)
    stats_table2 = generate_descriptive_stats(data, attribute2)
    return (freq_table1, stats_table1, freq_table2, stats_table2)
