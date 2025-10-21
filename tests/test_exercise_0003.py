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
