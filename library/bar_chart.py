import matplotlib.pyplot as plt
import calendar
from matplotlib.ticker import FuncFormatter


def report_day_sales(data):
    """
    Функция для отображения графика продаж по дням
    :param data(pd.DataFrame): Данные таблицы 2
    Автор: Ряднов И.М.
    """
    if data.index.name is None:
        data['Date'] = data['Date'].astype("datetime64[ns]")
        data.set_index('Date', inplace=True)
    sales_by_day = data['Sum'].resample('D').sum()
    x_labels = []
    for date in sales_by_day.index:
        if date.day % 5 == 0:
            month = calendar.month_name[date.month]
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
    :param data(pd.DataFrame): Данные таблицы 2
    Автор: Ряднов И.М.
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
    :param data(pd.DataFrame): Данные таблицы 2
    Автор: Ряднов И.М.
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
    :param data(pd.DataFrame): Данные таблицы 2
    Автор: Ряднов И.М.
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
    :param value(int): значение показателя на графике
    Автор: Ряднов И.М.
    """
    if value >= 1000000:
        value = f'{int(value / 1000000)}M'
    elif value >= 1000:
        value = f'{int(value / 1000)}K'
    return value
