import os
import pandas as pd
import matplotlib.pyplot as plt

path = f'{os.getcwd()}\data'
PRODUCT = pd.read_csv(f"{path}\MOCK_DATA_1.csv",
                      delimiter=',', encoding='utf8')
TOTAL_ORDERS = pd.read_csv(
    f"{path}\MOCK_DATA_3.csv", delimiter=',', encoding='utf8')
df = pd.merge(TOTAL_ORDERS, PRODUCT, on="Product ID")

plt.scatter(df['Price'], df['Quantity'])

labels_x = []
for x in df['Price']:
    labels_x.append(float(x[1:]))
    
plt.figure(figsize=(300, 300))
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot')
plt.xticks(labels_x, rotation=90, ha='right')
plt.yticks(df['Quantity'])
plt.show()