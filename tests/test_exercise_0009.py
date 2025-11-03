import numpy as np
import pandas as pd

from exercises.windows_commit_trial import numpy_pandas_short_exercise


def test_numpy_pandas_return_types():
    """Test that the function returns correct types for both array and dataframe."""
    array, dataframe = numpy_pandas_short_exercise()
    assert isinstance(array, np.ndarray)
    assert isinstance(dataframe, pd.DataFrame)


def test_numpy_array_shape_and_values():
    """Test the NumPy array has correct shape and values."""
    array, _ = numpy_pandas_short_exercise()
    expected_shape = (2, 3)
    expected_array = np.array([[1, 2, 3], [4, 5, 6]])

    assert array.shape == expected_shape
    np.testing.assert_array_equal(array, expected_array)


def test_pandas_dataframe_structure():
    """Test the pandas DataFrame has correct structure and values."""
    _, dataframe = numpy_pandas_short_exercise()

    # Test DataFrame shape
    assert dataframe.shape == (3, 2)

    # Test column names
    expected_columns = ["Column1", "Column2"]
    assert all(col in dataframe.columns for col in expected_columns)

    # Test values in columns
    expected_col1 = [1, 2, 3]
    expected_col2 = [4, 5, 6]
    pd.testing.assert_series_equal(
        dataframe["Column1"], pd.Series(expected_col1, name="Column1")
    )
    pd.testing.assert_series_equal(
        dataframe["Column2"], pd.Series(expected_col2, name="Column2")
    )


def test_function_consistency():
    """Test that multiple calls return consistent results."""
    array1, df1 = numpy_pandas_short_exercise()
    array2, df2 = numpy_pandas_short_exercise()

    np.testing.assert_array_equal(array1, array2)
    pd.testing.assert_frame_equal(df1, df2)
