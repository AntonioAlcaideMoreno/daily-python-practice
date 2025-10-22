"""
Utilities for a simple Money value object.

This module provides the Money class which models a monetary amount with a
currency and implements common "special" methods so Money instances can be
added, multiplied by a scalar, compared for equality, and rendered as a string.

Design notes / best practices:
- Operations require matching currencies when combining values.
- __mul__ expects a numeric scalar; no strict type checking is enforced here.
"""

from decimal import ROUND_HALF_EVEN, Decimal


class Money:
    """Represents an amount of money in a given currency.

    Attributes:
        amount (decimal): Numeric value representing the monetary amount.
        currency (str): Currency code / symbol associated with the amount.
    """

    _CENT = Decimal("0.01")

    def __init__(self, amount, currency):
        """Initialize a Money instance.

        Converts the provided amount to decimal and currency to str to normalize
        internal representation.
        """
        self.__amount = self._to_decimal(amount)
        self.__currency = str(currency)

    """ METHODS DEFINITIONS BELOW """

    def _to_decimal(self, amount):
        """Convert value to Decimal and quantize to 2 decimal places."""
        if not isinstance(amount, (int, float, Decimal)):
            raise ValueError("Amount should be a numeric value")
        # Convert via str to avoid float imprecision when value is a float
        dec = Decimal(str(amount)) if not isinstance(amount, Decimal) else amount
        return dec.quantize(self._CENT, rounding=ROUND_HALF_EVEN)

    def __add__(self, other):
        """Add two Money instances with the same currency.

        Returns:
            Money: New Money instance with the summed amount and same currency.

        Raises:
            ValueError: If currencies differ (cannot add different currencies).
        """
        # Ensure currencies match before adding to avoid mixing units
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        money = Money(self.amount + other.amount, self.currency)
        return money

    def __mul__(self, scalar):
        """Multiply the Money amount by a scalar.

        Returns:
            Money: New Money instance with the scaled amount and same currency.

        Note:
            This method does not enforce the scalar type strictly; it's assumed
            to be a numeric type (int/float). For production, consider checking
            types and raising TypeError for invalid inputs.
        """
        money = Money(self.amount * scalar, self.currency)
        return money

    def __eq__(self, other):
        """Compare two Money objects for equality.

        Two Money instances are equal when both amount and currency match.
        Floating point equality is used here; consider rounding or Decimal for
        financial applications to avoid precision issues.
        """
        if self.amount == other.amount and self.currency == other.currency:
            return True
        return False

    def __str__(self):
        """Return a human-readable string representation of the money.

        Example output: '12.34 USD'
        """
        return f"{self.amount:.2f} {self.currency}"

    """ END OF METHODS DEFINITIONS"""

    """GETTERS, SETTERS AND PROPERTIES BELOW"""

    @property
    def amount(self):
        """Get the monetary amount as a Decimal (already quantized to 2 decimals)."""
        return self.__amount

    @amount.setter
    def amount(self, value):
        """Set the monetary amount.

        Args:
            value (decimal): New amount value

        Note:
            Returns None silently on invalid input -
            consider raising an exception instead
        """
        if value < 0:
            raise ValueError("Amount cannot be negative")
        self.__amount = self._to_decimal(value)

    @property
    def currency(self):
        """Get the currency code/symbol."""
        return self.__currency

    @currency.setter
    def currency(self, value):
        """Set the currency code/symbol.

        Args:
            value (str): New currency code/symbol
        """
        currencies_list = ["USD", "EUR", "GBP", "JPY", "CNY"]  # Example list
        if str(value) not in currencies_list:
            raise ValueError(
                "Unsupported currency. Supported currencies are: "
                + ", ".join(currencies_list)
            )
        self.__currency = str(value)

    """END OF GETTERS, SETTERS AND PROPERTIES"""


if __name__ == "__main__":
    # Example usage
    money1 = Money(10.509, "USD")
    money2 = Money(5.252, "USD")
    money3 = money1 + money2
    money4 = money1 * 2
    print(money3)  # Output: 15.76 USD
    print(money4)  # Output: 21.02 USD
