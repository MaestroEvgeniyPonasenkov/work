import pandas as pd
import matplotlib.pyplot as plt


def report_price_by_category(data: pd.DataFrame) -> None:
    """
    Функция для отображения графика распределения цен по категориям товаров
    :param data(pd.DataFrame): Данные таблицы 1
    Автор: Ряднов И.М.
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
