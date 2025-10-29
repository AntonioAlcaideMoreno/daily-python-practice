"""
Implementation of the Singleton design pattern for database connections.

This module demonstrates the Singleton pattern which ensures a class has only one
instance and provides a global point of access to that instance. This is particularly
useful for database connections where we want to avoid multiple connections being
created.

Key concepts:
- Uses __new__ to control instance creation
- Maintains a single instance in _instance class variable
- All instance requests return the same object
"""


class DatabaseConnection:
    """
    A Singleton class that manages a single database connection instance.

    Attributes:
        _instance (DatabaseConnection): Class-level variable storing the single instance
        host (str): Database host address
        connected (bool): Flag indicating if database is currently connected

    Usage:
        db1 = DatabaseConnection()  # Creates first instance
        db2 = DatabaseConnection()  # Returns same instance as db1
        assert db1 is db2  # True - both variables reference same object
    """

    # Class variable to store the singleton instance
    _instance = None

    def __new__(cls):
        """
        Control instance creation to ensure only one instance exists.

        Returns:
            DatabaseConnection: The single instance of DatabaseConnection
        """
        if cls._instance is None:
            # Create new instance only if none exists
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the database connection properties.
        Note: This runs on every DatabaseConnection() call but only affects
        the instance on first creation due to singleton pattern.
        """
        self.host = "localhost"
        self.connected = False

    def connect(self):
        """
        Simulate establishing a database connection.
        Sets connected flag to True and prints confirmation message.
        """
        self.connected = True
        print("Connected to database at localhost")

    def disconnect(self):
        """
        Simulate closing a database connection.
        Sets connected flag to False and prints confirmation message.
        """
        self.connected = False
        print("Disconnected from database")
