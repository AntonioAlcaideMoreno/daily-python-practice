from abc import abstractmethod

from beverage import Beverage


class CondimentDecorator(Beverage):
    """
    Abstract decorator class for all condiments.
    """

    @abstractmethod
    def get_description(self):
        # TODO: Abstract method that must be implemented by concrete decorators
        # TODO: Should return the description of the beverage with the condiment added
        pass


class Milk(CondimentDecorator):
    """
    Concrete decorator for adding milk to a beverage.
    """

    def __init__(self, beverage):
        # TODO: Store the beverage object as self.beverage
        # TODO: This beverage will be decorated with milk
        self.beverage = beverage

    def get_description(self):
        # TODO: Return the beverage's description plus " + Milk"
        # TODO: Use self.beverage.get_description() to get the base description
        return self.beverage.get_description() + " + Milk"

    def cost(self):
        # TODO: Return the beverage's cost plus 0.10 for milk
        # TODO: Use self.beverage.cost() to get the base cost
        return self.beverage.cost() + 0.1


class Mocha(CondimentDecorator):
    """
    Concrete decorator for adding mocha to a beverage.
    """

    def __init__(self, beverage):
        # TODO: Store the beverage object as self.beverage
        # TODO: This beverage will be decorated with mocha
        self.beverage = beverage

    def get_description(self):
        # TODO: Return the beverage's description plus " + Mocha"
        # TODO: Use self.beverage.get_description() to get the base description
        return self.beverage.get_description() + " + Mocha"

    def cost(self):
        # TODO: Return the beverage's cost plus 0.20 for mocha
        # TODO: Use self.beverage.cost() to get the base cost
        return self.beverage.cost() + 0.2


class Soy(CondimentDecorator):
    """
    Concrete decorator for adding soy to a beverage.
    """

    def __init__(self, beverage):
        # TODO: Store the beverage object as self.beverage
        # TODO: This beverage will be decorated with soy
        self.beverage = beverage

    def get_description(self):
        # TODO: Return the beverage's description plus " + Soy"
        # TODO: Use self.beverage.get_description() to get the base description
        return self.beverage.get_description() + " + Soy"

    def cost(self):
        # TODO: Return the beverage's cost plus 0.15 for soy
        # TODO: Use self.beverage.cost() to get the base cost
        return self.beverage.cost() + 0.15


class Whip(CondimentDecorator):
    """
    Concrete decorator for adding whipped cream to a beverage.
    """

    def __init__(self, beverage):
        # TODO: Store the beverage object as self.beverage
        # TODO: This beverage will be decorated with whipped cream
        self.beverage = beverage

    def get_description(self):
        # TODO: Return the beverage's description plus " + Whip"
        # TODO: Use self.beverage.get_description() to get the base description
        return self.beverage.get_description() + " + Whip"

    def cost(self):
        # TODO: Return the beverage's cost plus 0.10 for whipped cream
        # TODO: Use self.beverage.cost() to get the base cost
        return self.beverage.cost() + 0.1
