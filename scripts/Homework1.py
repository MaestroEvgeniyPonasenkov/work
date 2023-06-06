import os
import pandas as pd
import numpy as np


def csv_to_npz(outputf: str) -> None:
    """
    Converts CSV files into a single compressed binary file in NPZ format.

    Parameters:
    - outputf (str): the name of the output file, without extension.

    Returns:
    - None

    Example:
    >>> csv_to_npz('my_data')
    """
    path = f'{os.getcwd()[:-7]}data'
    csv_file1 = f'{path}\MOCK_DATA_1.csv'
    csv_file2 = f'{path}\MOCK_DATA_2.csv'
    csv_file3 = f'{path}\MOCK_DATA_3.csv'
    data1 = pd.read_csv(csv_file1).to_numpy()
    data2 = pd.read_csv(csv_file2).to_numpy()
    data3 = pd.read_csv(csv_file3).to_numpy()
    bin_file = f'{path}\{outputf}.npz'
    np.savez(bin_file, data1=data1, data2=data2, data3=data3)


csv_to_npz('output')
