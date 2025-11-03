class CoffeeShop:
    """
    A class that manages coffee orders and inventory.
    """

    def __init__(self):
        # ALL: Initialize an empty list to store orders
        # ALL: This list will hold beverage objects (both plain and decorated)
        self.orders = []

    def add_order(self, beverage):
        # ALL: Add the beverage to the orders list
        # ALL: Return the total number of orders after adding this one
        # ALL: Use len() to get the count after appending
        self.orders.append(beverage)
        return len(self.orders)

    def get_total_cost(self):
        # ALL: Calculate and return the total cost of all orders
        # ALL: Use sum() with a generator expression
        # ALL: Call the cost() method on each beverage in self.orders
        return sum(lambda x: x.cost() for x in self.orders)

    def print_orders(self):
        # ALL: Create a formatted string showing all orders
        # ALL: Initialize an empty result list
        # ALL: Loop through orders with enumerate() starting at 1
        # ALL: For each order, format as "Order #X: description - $cost"
        # ALL: Use beverage.get_description() and beverage.cost()
        # ALL: Format cost to 2 decimal places using :.2f
        # ALL: Join all order strings with newlines and return
        result = []
        for i in enumerate(self.orders, start=1):
            result.append(
                f"""Order #{i}: {self.beverage.get_description()}
                - ${self.beverage.cost():.2f}"""
            )
        return "\n".join(result)

    def clear_orders(self):
        # ALL: Remove all orders from the orders list
        # ALL: Reset self.orders to an empty list
        self.orders = []

    def get_order_count(self):
        # ALL: Return the number of orders currently in the shop
        # ALL: Use len() on the orders list
        return len(self.orders)
