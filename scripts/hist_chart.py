import matplotlib.pyplot as plt
import pandas as pd
import os


def histogram(data):
    plt.hist(data, bins=20, color='blue', edgecolor='black')
    plt.title('Гистограмма распределения количества\nтоваров в заказе')
    plt.xlabel('Количество товаров в заказе')
    plt.ylabel('Количество')
    plt.show()


path = f'{os.getcwd()}/data'
print(path)
data = pd.read_csv(f"{path}\MOCK_DATA_3.csv",
                   delimiter=',', encoding='utf8')
histogram(data['Quantity'])
