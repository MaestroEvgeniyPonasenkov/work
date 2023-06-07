import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def report_price_by_quantity(data):
    plt.scatter(data['Price'], data['Quantity'])
    plt.xlabel('Цена')
    plt.ylabel('Количество')
    plt.title('Распределение количества заказанных товаров по их цене')
    x_labels = np.arange(int(data['Price'].min()), int(data['Price'].max())+100, 25)
    plt.xticks(x_labels, rotation=90, ha='right')
    plt.yticks(list(range(int(data['Quantity'].min()), int(data['Quantity'].max())+1)))
    plt.show()
    
    
path = f'{os.getcwd()}\data'
data_1 = pd.read_csv(f"{path}\MOCK_DATA_1.csv",
                      delimiter=',', encoding='utf8')
data_2 = pd.read_csv(
    f"{path}\MOCK_DATA_3.csv", delimiter=',', encoding='utf8')
data = pd.merge(data_2, data_1, on="Product ID")
data['Price'] = data['Price'].replace('[\$,]', '', regex=True).astype(float)
report_price_by_quantity(data)


