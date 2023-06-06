import matplotlib.pyplot as plt
import numpy as np
def boxplot():
    # Создаем случайные данные
    data = np.random.normal(size=(3, 5))
    print(data)
    # Создаем ящик с усами с помощью функции boxplot
    plt.boxplot(data)
    # Добавляем заголовок
    plt.title('Boxplot')
    # Показываем график
    plt.show()

boxplot()