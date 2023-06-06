import matplotlib.pyplot as plt
import numpy as np

def hist():
    # Создание массива данных
    data = np.random.normal(0, 1, 1000)
    # Построение гистограммы
    plt.hist(data, bins=30, color='blue', edgecolor='black')
    # Добавление заголовка и меток осей
    plt.title('Гистограмма нормального распределения')
    plt.xlabel('Значения')
    plt.ylabel('Количество')
    # Отображение графика
    plt.show()

hist()