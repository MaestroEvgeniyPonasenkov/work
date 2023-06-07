import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from text_reports import merge_files


def histogram():
    data = np.random.normal(0, 1, 1000)
    plt.hist(data, bins=20, color='blue', edgecolor='black')
    plt.title('Гистограмма распределения категорий')
    plt.xlabel('Категория')
    plt.ylabel('Количество')
    plt.show()


def prepare_data(start_date: str, end_date: str) -> pd.DataFrame:
    merged = merge_files()
    selector = merged['Date'].between(start_date, end_date)
    result = merged.loc[selector, ['Category', 'Quantity']]
    new = result.groupby('Category').sum().reset_index()
    print(new)
    return new


data = prepare_data('2022-09-01', '2023-04-01')

plt.hist(data['Quantity'], bins=20)
plt.xlabel('Категория')
plt.ylabel('Количество заказов')
plt.title('Гистограмма количества заказов по категориям')
plt.figure(figsize=(300, 300))
# data.set_index('Category', inplace=True)
# plt.xticks(data.index, rotation=90, ha='right')
plt.show()
