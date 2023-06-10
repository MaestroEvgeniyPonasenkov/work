import pandas as pd
import matplotlib.pyplot as plt
import os


def report_price_by_category(data: pd.DataFrame) -> None:
    data['Price'] = data['Price'].replace('[\$,]', '', regex=True).astype(float)
    categories = data.groupby('Category')
    prices_by_category = [category[1]['Price'].tolist() for category in categories]
    plt.boxplot(prices_by_category)
    print([category[0] for category in categories])
    plt.xticks(range(1, len(categories) + 1), [category[0] for category in categories], rotation=60, ha='right')
    plt.title('Распределение цен по категориям товаров')
    plt.xlabel('Категория товара')
    plt.ylabel('Цена')
    plt.show()


if __name__ == '__main__':
    path = f'{os.getcwd()}\data'
    data = pd.read_csv(f"{path}\MOCK_DATA_1.csv")
    report_price_by_category(data)
