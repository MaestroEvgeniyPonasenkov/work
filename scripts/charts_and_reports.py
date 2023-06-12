import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def merge_files(PRODUCT, ORDERS, TOTAL_ORDERS):
    """
    Мердж данных
    Автор: Ряднов И.М.
    :param PRODUCT(pd.DataFrame): датафрейм с товарами
    :param ORDERS(pd.DataFrame): датафрейм с заказами
    :param TOTAL_ORDERS(pd.DataFrame): датафрейм со всеми заказами
    :return merged(pd.DataFrame): объединенный датафрейм
    """
    merged = pd.merge(TOTAL_ORDERS, PRODUCT, on="Product ID")
    merged = pd.merge(merged, ORDERS, on="Order ID")
    return merged


def report_about_firm(merged, start_date, end_date, category):
    """
    Отчет о продажах товаров выбранной компании за выбранный временной промежуток
    Автор: Болезнов С.А.
    :param merged(pd.DataFrame): датафрейм со всеми данными
    :param start_date(str): начальная дата
    :param end_date(str): конечная дата
    :param category(str): категория
    :return result(pd.DataFrame): полученный отчет
    """
    merged['Date'] = merged['Date'].astype("datetime64[ns]")
    selector = (merged['Date'].between(start_date, end_date)) & (
            merged['Category'] == category)
    result = merged.loc[selector, ['Product',
                                   'Description', 'Price', 'Quantity', 'Sum']]
    return result


def generate_frequency_table(data, attribute):
    """
    Отчет о частоте встречаемости атрибута
    Автор: Ряднов И.М.
    :param data(pd.DataFrame): датафрейм со всеми данными
    :param attribute(str): имя атрибута
    :return freq_table():
    """
    freq_table = data[attribute].value_counts().reset_index()
    freq_table.columns = [attribute, 'Частота']
    freq_table['Процент'] = (freq_table['Частота'] / len(data)) * 100
    return freq_table


def generate_descriptive_stats(data, attribute):
    """
    Отчет-описание атрибутов
    Автор: Ряднов И.М.
    :param data(pd.DataFrame): датафрейм со всеми данными
    :param attribute(str): имя атрибута
    :return descriptive_stats():
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
    Генерация отчётов о паре атрибутов
    Автор: Ряднов И.М.
    :param data(pd.DataFrame): датафрейм со всеми данными
    :param attribute1(str): имя первого атрибута
    :param attribute2(str): имя второго атрибута
    :return freq_table1():
    :return stats_table1():
    :return freq_table2():
    :return stats_table2():
    """
    freq_table1 = generate_frequency_table(data, attribute1)
    stats_table1 = generate_descriptive_stats(data, attribute1)
    freq_table2 = generate_frequency_table(data, attribute2)
    stats_table2 = generate_descriptive_stats(data, attribute2)
    return (freq_table1, stats_table1, freq_table2, stats_table2)


def report_day_sales(data):
    """
    Функция для отображения графика продаж по дням
    Автор: Ряднов И.М.
    :param data(pd.DataFrame): Данные таблицы 2
    :return: None
    """
    months = {
        1: "Январь",
        2: "Февраль",
        3: "Март",
        4: "Апрель",
        5: "Май",
        6: "Июнь",
        7: "Июль",
        8: "Август",
        9: "Сентябрь",
        10: "Октябрь",
        11: "Ноябрь",
        12: "Декабрь"
    }
    if data.index.name is None:
        data['Date'] = data['Date'].astype("datetime64[ns]")
        data.set_index('Date', inplace=True)
    sales_by_day = data['Sum'].resample('D').sum()
    x_labels = []
    for date in sales_by_day.index:
        if date.day % 5 == 0:
            month = months.get(date.month)
            day = str(date.day)
            x_labels.append(f'{month} {day}')
        else:
            x_labels.append('')
    plt.bar(sales_by_day.index, sales_by_day, width=0.7)
    plt.xlabel('Дата')
    plt.ylabel('Продажи')
    plt.title('Продажи по дням')
    plt.xticks(sales_by_day.index, x_labels, rotation=60, ha='right')
    formatter = FuncFormatter(format_func)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.show()


def report_week_sales(data):
    """
    Функция для отображения графика продаж по неделям
    Автор: Ряднов И.М.
    :param data(pd.DataFrame): Данные таблицы 2
    :return: None
    """
    if data.index.name is None:
        data['Date'] = data['Date'].astype("datetime64[ns]")
        data.set_index('Date', inplace=True)
    sales_by_week = data['Sum'].resample('W').sum()
    plt.bar(sales_by_week.index, sales_by_week, width=3)
    plt.xlabel('Дата')
    plt.ylabel('Продажи')
    plt.title('Продажи по неделям')
    plt.xticks(sales_by_week.index, rotation=60, ha='right')
    formatter = FuncFormatter(format_func)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.show()


def report_month_sales(data):
    """
    Функция для отображения графика продаж по месяцам
    Автор: Ряднов И.М.
    :param data(pd.DataFrame): Данные таблицы 2
    :return: None
    """
    if data.index.name is None:
        data['Date'] = data['Date'].astype("datetime64[ns]")
        data.set_index('Date', inplace=True)
    sales_by_month = data['Sum'].resample('M').sum()
    plt.bar(sales_by_month.index, sales_by_month, width=10)
    plt.xlabel('Дата')
    plt.ylabel('Продажи')
    plt.title('Продажи по месяцам')
    plt.xticks(sales_by_month.index, rotation=60, ha='right')
    for i, value in enumerate(sales_by_month):
        plt.text(sales_by_month.index[i], value + 100, f"{str(value)}$", ha='center', va='bottom')
    formatter = FuncFormatter(format_func)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.show()


def report_year_sales(data):
    """
    Функция для отображения графика продаж по годам
    Автор: Ряднов И.М.
    :param data(pd.DataFrame): Данные таблицы 2
    :return: None
    """
    if data.index.name is None:
        data['Date'] = data['Date'].astype("datetime64[ns]")
        data.set_index('Date', inplace=True)
    sales_by_year = data['Sum'].resample('Y').sum()
    plt.bar(sales_by_year.index, sales_by_year, width=10)
    plt.xlabel('Дата')
    plt.ylabel('Продажи')
    plt.title('Продажи по годам')
    plt.xticks(sales_by_year.index, rotation=60, ha='right')
    for i, value in enumerate(sales_by_year):
        plt.text(sales_by_year.index[i], value + 100, f"{str(value)}$", ha='center', va='bottom')
    formatter = FuncFormatter(format_func)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.show()


def format_func(value, tick_number):
    """
    Функция для изменения отображения больших значений на осях графиков
    Автор: Ряднов И.М.
    :param value(int): значение показателя на графике
    :param tick_number(int): количество tick
    :return value():
    """
    if value >= 1000000:
        value = f'{int(value / 1000000)}M'
    elif value >= 1000:
        value = f'{int(value / 1000)}K'
    return value


def report_price_by_category(data: pd.DataFrame) -> None:
    """
    Функция для отображения графика распределения цен по категориям товаров
    Автор: Ряднов И.М.
    :param data(pd.DataFrame): Данные таблицы 1
    :return: None
    """
    data['Price'] = data['Price'].replace(
        '[\$,]', '', regex=True).astype(float)
    categories = data.groupby('Category')
    prices_by_category = [category[1]['Price'].tolist()
                          for category in categories]
    plt.boxplot(prices_by_category)
    plt.xticks(range(1, len(categories) + 1),
               [category[0] for category in categories], rotation=60, ha='right')
    plt.title(
        'Распределение цен по категориям товаров')
    plt.xlabel('Категория товара')
    plt.ylabel('Цена')
    plt.show()


def histogram(data: pd.DataFrame, colomn: str):
    """
    Создание гистограммы
    Автор: Болезнов С.А.
    :param data: Датафрейм с данными
    :param colomn: Тип гистограммы
    :return: None
    """
    if colomn == 'Quantity':
        plt.hist(data[colomn], bins=20, color='blue', edgecolor='black')
        plt.title('Гистограмма распределения количества\nтоваров в заказе')
        plt.xlabel('Количество товаров в заказе')
        plt.ylabel('Количество')
    if colomn == 'Price':
        prices = [int(str(x)[:-3]) for x in data[colomn]]
        plt.hist(prices, bins=30, color='blue', edgecolor='black')
        plt.title('Гистограмма распределения цены на товары')
        plt.xlabel('Цена товара')
        plt.ylabel('Количество')
    if colomn == 'Sum':
        plt.hist(data[colomn], bins=30, color='blue', edgecolor='black')
        plt.title('Гистограмма распределения суммы заказов')
        plt.xlabel('Сумма заказа')
        plt.ylabel('Количество')
    plt.show()


def report_price_by_quantity(data):
    """
    Функция для отображения графика распределения количества заказанных товаров по их цене
    Автор: Ряднов И.М.
    :param data(pd.DataFrame): Данные таблицы 3
    :return: None
    """
    plt.scatter(data['Price'], data['Quantity'])
    plt.xlabel('Цена')
    plt.ylabel('Количество')
    plt.title('Распределение количества заказанных товаров по их цене')
    x_labels = np.arange(int(data['Price'].min()),
                         int(data['Price'].max()) + 100, 25)
    plt.xticks(x_labels, rotation=90, ha='right')
    plt.yticks(
        list(range(int(data['Quantity'].min()), int(data['Quantity'].max()) + 1)))
    plt.show()
