import numpy as np
import pandas as pd


def calculate_statistics(data):
    """
    Calculate basic statistics for a given dataset.

    Parameters:
    data (list or np.ndarray or pd.Series): Input data for which to calculate
    statistics.

    Returns:
    dict: A dictionary containing mean, median, and standard deviation.
    """
    if isinstance(data, list):
        data = np.array(data)
    elif isinstance(data, pd.Series):
        data = data.values

    mean = np.mean(data)
    median = np.median(data)
    std_dev = np.std(data)

    return {"mean": mean, "median": median, "std_dev": std_dev}


def dataframe_creation(data_dict):
    """
    Create a pandas DataFrame from a dictionary.

    Parameters:
    data_dict (dict): A dictionary where keys are column names and values are lists of
    column data.

    Returns:
    pd.DataFrame: A pandas DataFrame created from the input dictionary.
    """
    df = pd.DataFrame(data_dict)
    return df


# Example usage
if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    stats = calculate_statistics(data)
    for key, value in stats.items():
        print(f"{key}: {value}")

    data_dict = {"A": [1, 2, 3], "B": [4, 5, 6]}
    df = dataframe_creation(data_dict)
    print("DataFrame:\n", df)
