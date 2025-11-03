from abc import ABC, abstractmethod


class Beverage(ABC):
    """
    Abstract base class for all beverages.
    """

    def __init__(self):
        # TODO: Initialize description attribute with "Unknown Beverage"
        self.description = "Unknown Beverage"

    def get_description(self):
        # TODO: Return the description attribute
        return self.description

    @abstractmethod
    def cost(self):
        # TODO: Abstract method that must be implemented by concrete beverage classes
        # TODO: Should return the cost of the beverage as a float
        pass


class Espresso(Beverage):
    """
    A concrete beverage implementation - Espresso.
    """

    def __init__(self):
        # TODO: Call parent constructor using super()
        # TODO: Set description to "Espresso"
        super().__init__()
        self.description = "Espresso"

    def cost(self):
        # TODO: Return the cost of Espresso (1.99)
        return 1.99


class HouseBlend(Beverage):
    """
    A concrete beverage implementation - House Blend Coffee.
    """

    def __init__(self):
        # TODO: Call parent constructor using super()
        # TODO: Set description to "House Blend Coffee"
        super().__init__()
        self.description = "House Blend Coffee"

    def cost(self):
        # TODO: Return the cost of House Blend Coffee (0.89)
        return 0.89


class DarkRoast(Beverage):
    """
    A concrete beverage implementation - Dark Roast Coffee.
    """

    def __init__(self):
        # TODO: Call parent constructor using super()
        # TODO: Set description to "Dark Roast Coffee"
        super().__init__()
        self.description = "Dark Roast Coffee"

    def cost(self):
        # TODO: Return the cost of Dark Roast Coffee (0.99)
        return 0.99


class Decaf(Beverage):
    """
    A concrete beverage implementation - Decaf Coffee.
    """

    def __init__(self):
        # TODO: Call parent constructor using super()
        # TODO: Set description to "Decaf Coffee"
        super().__init__()
        self.description = "Decaf Coffee"

    def cost(self):
        # TODO: Return the cost of Decaf Coffee (1.05)
        return 1.05
