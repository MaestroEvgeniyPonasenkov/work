import matplotlib.pyplot as plt
import numpy as np


def report_price_by_quantity(data):
    """
    Функция для отображения графика распределения количества заказанных товаров по их цене
    :param data(pd.DataFrame): Данные таблицы 3
    Автор: Ряднов И.М.
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
