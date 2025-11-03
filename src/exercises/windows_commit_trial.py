import numpy as np
import pandas as pd


def numpy_pandas_short_exercise():
    """
    Perform basic operations using NumPy and pandas.

    Returns:
    tuple: A tuple containing a NumPy array and a pandas DataFrame.
    """
    # Create a NumPy array
    np_array = np.array([[1, 2, 3], [4, 5, 6]])

    # Create a pandas DataFrame
    data = {"Column1": [1, 2, 3], "Column2": [4, 5, 6]}
    df = pd.DataFrame(data)

    return np_array, df


# Example usage
if __name__ == "__main__":
    array, dataframe = numpy_pandas_short_exercise()
    print("NumPy Array:\n", array)
    print("Pandas DataFrame:\n", dataframe)
