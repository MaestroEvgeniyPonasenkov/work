import matplotlib.pyplot as plt
import pandas as pd


def histogram(data: pd.DataFrame, colomn: str) -> None:
    if colomn == 'Quantity':
        plt.hist(data[colomn], bins=30, color='blue', edgecolor='black')
        plt.title('Гистограмма распределения количества\nтоваров в заказе')
        plt.xlabel('Количество товаров в заказе')
        plt.ylabel('Количество')
    if colomn == 'Price':
        prices = [int(x[1:-3]) for x in data[colomn]]
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
