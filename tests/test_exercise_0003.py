# Tests for handle_shopping_cart.py file

from exercises.handle_shopping_cart import handle_shopping_cart


def test_handle_shopping_cart_basic():
    orders = ["apple:2", "banana:3", "apple:1"]
    expected_cart = {"apple": 3, "banana": 3}
    assert handle_shopping_cart(orders) == expected_cart


def test_handle_shopping_cart_invalid_format(capfd):
    orders = ["apple-2", "banana:3"]
    expected_cart = {"banana": 3}
    assert handle_shopping_cart(orders) == expected_cart
    captured = capfd.readouterr()
    assert "Invalid format: apple-2" in captured.out


def test_handle_shopping_cart_negative_quantity(capfd):
    orders = ["apple:-2", "banana:3"]
    expected_cart = {"banana": 3}
    assert handle_shopping_cart(orders) == expected_cart
    captured = capfd.readouterr()
    assert "Negative quantity not allowed: apple:-2" in captured.out


def test_handle_shopping_cart_non_numeric_quantity(capfd):
    orders = ["apple:two", "banana:3"]
    expected_cart = {"banana": 3}
    assert handle_shopping_cart(orders) == expected_cart
    captured = capfd.readouterr()
    assert "Invalid quantity: apple:two" in captured.out


def test_handle_shopping_cart_empty_list():
    orders = []
    expected_cart = {}
    assert handle_shopping_cart(orders) == expected_cart


def test_handle_shopping_cart_multiple_errors(capfd):
    orders = ["apple:-2", "banana:three", "orange-1", "grape:2"]
    expected_cart = {"grape": 2}
    assert handle_shopping_cart(orders) == expected_cart
    captured = capfd.readouterr()
    assert all(
        msg in captured.out
        for msg in [
            "Negative quantity not allowed: apple:-2",
            "Invalid quantity: banana:three",
            "Invalid format: orange-1",
        ]
    )


def test_handle_shopping_cart_zero_quantity(capfd):
    orders = ["apple:0", "banana:3"]
    expected_cart = {"apple": 0, "banana": 3}
    assert handle_shopping_cart(orders) == expected_cart


def test_handle_shopping_cart_accumulation():
    orders = ["apple:2", "banana:3", "apple:3", "banana:2", "apple:1"]
    expected_cart = {"apple": 6, "banana": 5}
    assert handle_shopping_cart(orders) == expected_cart
