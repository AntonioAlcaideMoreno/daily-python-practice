class BankAccount:
    """
    A class representing a bank account with basic banking operations.

    Attributes:
        interest_rate (float): Class-level interest rate applied
        to all accounts (2% default)
    """

    interest_rate = 0.02

    def __init__(self, owner_name: str, initial_balance: float):
        """
        Initialize a new bank account.

        Args:
            owner_name (str): Name of the account owner
            initial_balance (float): Initial deposit amount

        Raises:
            ValueError: If initial_balance is negative
        """
        self.__owner_name = owner_name
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.__balance = initial_balance

    @property
    def owner_name(self) -> str:
        """Get the account owner's name."""
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, value: str) -> None:
        """
        Set the account owner's name.

        Args:
            value (str): New owner name

        Note:
            Returns None silently on invalid input -
            consider raising an exception instead
        """
        if not value:
            print("Owner name cannot be empty")
            return None
        self.__owner_name = value

    @property
    def balance(self) -> float:
        """Get the current account balance."""
        return self.__balance

    @balance.setter
    def balance(self, value: float) -> None:
        """
        Set the account balance directly (with validation).

        Args:
            value (float): New balance value

        Note:
            Returns None silently on invalid input -
            consider raising an exception instead
        """
        if value < 0:
            print("Balance cannot be negative")
            return None
        self.__balance = value

    def deposit(self, amount: float) -> bool:
        """
        Deposit money into the account.

        Args:
            amount (float): Amount to deposit

        Returns:
            bool: True if deposit was successful, False otherwise
        """
        if amount < 0:
            print("Deposit amount must be positive")
            return False
        self.__balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from the account.

        Args:
            amount (float): Amount to withdraw

        Returns:
            bool: True if withdrawal was successful, False otherwise
        """
        if amount < 0:
            print("Withdrawal amount must be positive")
            return False
        elif amount > self.__balance:
            print("Insufficient funds")
            return False
        self.__balance -= amount
        return True

    def apply_interest(self) -> float:
        """
        Apply the current interest rate to the balance.

        Returns:
            float: The amount of interest earned
        """
        interest = self.__balance * self.interest_rate
        self.__balance += interest
        return interest

    def display_info(self) -> None:
        """Print account information including owner,
        balance, and interest rate."""
        print(
            f"Account Owner: {self.__owner_name}\nBalance: ${self.__balance}\n"
            f"Interest Rate: {self.interest_rate*100}%"
        )
