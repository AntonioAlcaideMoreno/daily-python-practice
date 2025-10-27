from decimal import Decimal

import pytest

from exercises.special_methods_practice import Money


def test_init_and_quantize_with_float_and_string():
    m1 = Money(
        10.509, "USD"
    )  # float input -> quantized to 2 decimals (ROUND_HALF_EVEN)
    m2 = Money("5.252", "USD")  # string input -> quantized to 2 decimals
    assert isinstance(m1.amount, Decimal)
    assert m1.amount == Decimal("10.51")
    assert m2.amount == Decimal("5.25")


def test_add_same_currency():
    a = Money("10.50", "USD")
    b = Money("5.24", "USD")
    c = a + b
    assert isinstance(c, Money)
    assert c.currency == "USD"
    assert c.amount == Decimal("15.74")


def test_add_different_currency_raises():
    a = Money(1, "USD")
    b = Money(1, "EUR")
    with pytest.raises(ValueError):
        _ = a + b


def test_mul_by_integer_scalar():
    m = Money("2.50", "USD")
    p = m * 3  # use integer scalar (Decimal * int is supported)
    assert isinstance(p, Money)
    assert p.amount == Decimal("7.50")
    assert p.currency == "USD"


def test_equality_and_str():
    m = Money("1.234", "USD")  # quantizes to 1.23
    n = Money(1.23, "USD")
    assert m == n
    assert str(m) == "1.23 USD"


def test_setting_negative_amount_raises():
    m = Money(1, "USD")
    with pytest.raises(ValueError):
        m.amount = -5


def test_unsupported_currency_raises_and_supported_allows():
    m = Money(1, "USD")
    with pytest.raises(ValueError):
        m.currency = "ABC"  # not in example supported list
    # supported currency should be accepted
    m.currency = "EUR"
    assert m.currency == "EUR"


def test_init_with_non_numeric_raises():
    with pytest.raises(ValueError):
        Money("not-a-number", "USD")
