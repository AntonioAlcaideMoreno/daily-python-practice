import numpy as np
import pandas as pd

from exercises.wsl_commit_trial import calculate_statistics, dataframe_creation


def test_calculate_statistics_with_list():
    data = [1, 2, 3, 4, 5]
    result = calculate_statistics(data)

    assert isinstance(result, dict)
    assert result["mean"] == 3.0
    assert result["median"] == 3.0
    assert round(result["std_dev"], 2) == 1.41


def test_calculate_statistics_with_numpy():
    data = np.array([1, 2, 3, 4, 5])
    result = calculate_statistics(data)

    assert isinstance(result, dict)
    assert result["mean"] == 3.0
    assert result["median"] == 3.0
    assert round(result["std_dev"], 2) == 1.41


def test_calculate_statistics_with_pandas():
    data = pd.Series([1, 2, 3, 4, 5])
    result = calculate_statistics(data)

    assert isinstance(result, dict)
    assert result["mean"] == 3.0
    assert result["median"] == 3.0
    assert round(result["std_dev"], 2) == 1.41


def test_dataframe_creation():
    test_dict = {"A": [1, 2, 3], "B": [4, 5, 6]}
    df = dataframe_creation(test_dict)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 2)
    assert list(df.columns) == ["A", "B"]
    assert (df["A"] == [1, 2, 3]).all()
    assert (df["B"] == [4, 5, 6]).all()
