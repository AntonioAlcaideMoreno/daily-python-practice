"""Simple banking system models: Transaction, Account hierarchy and Bank.

This module contains small, well-documented classes suitable for exercises
and demonstrations. It intentionally keeps the behavior straightforward
(e.g., no persistence, no concurrency safeguards) while providing clear
APIs for deposits, withdrawals, interest application, and transfers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple


class Transaction:
    """Represents a single account transaction.

    Attributes:
        transaction_type (str): e.g. 'deposit', 'withdrawal', 'interest'
        amount (float): Monetary amount involved in the transaction
        account (Account): Reference to the account where it occurred
    """

    def __init__(self, transaction_type: str, amount: float, account: "Account"):
        # Store basic immutable attributes describing the transaction
        self.transaction_type = transaction_type
        self.amount = amount
        self.account = account

    def __str__(self) -> str:
        # Human-readable form used in logs and debugging
        return f"{self.transaction_type.title()} - ${self.amount:.2f}"


class Account(ABC):
    """Abstract base class for bank accounts.

    Subclasses must implement `withdraw`. Common functionality such as
    `deposit` and transaction history tracking is provided here.
    """

    def __init__(self, account_number: str, owner_name: str, balance: float = 0.0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance
        # Keep a simple chronological list of Transaction instances
        self.transaction_history: List[Transaction] = []

    def deposit(self, amount: float) -> Tuple[bool, str]:
        """Deposit `amount` into the account.

        Validates the input, updates the balance and records a Transaction.
        Returns a (success, message) tuple to keep the interface simple.
        """
        if amount <= 0:
            return (False, "Deposit amount must be positive")
        self.balance += amount
        transaction = Transaction("deposit", amount, self)
        self.transaction_history.append(transaction)
        return (True, f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")

    @abstractmethod
    def withdraw(self, amount: float) -> Tuple[bool, str]:
        """Withdraw `amount` from the account.

        Concrete implementations must implement account-specific rules
        (e.g., minimum balance, overdraft). Return (success, message).
        """
        pass

    def get_balance(self) -> float:
        """Return current account balance."""
        return self.balance

    def get_transaction_history(self) -> List[Transaction]:
        """Return the list of recorded transactions for this account."""
        return self.transaction_history


class SavingsAccount(Account):
    """Savings account implementation enforcing a minimum balance and interest."""

    def __init__(
        self,
        account_number: str,
        owner_name: str,
        balance: float = 0.0,
        interest_rate: float = 0.01,
        min_balance: float = 100.0,
    ):
        super().__init__(account_number, owner_name, balance)
        self.interest_rate = interest_rate
        self.min_balance = min_balance

    def withdraw(self, amount: float) -> Tuple[bool, str]:
        """Withdraw with a constraint that the balance cannot fall below min_balance."""
        if amount <= 0:
            return (False, "Withdrawal amount must be positive")
        if (self.balance - amount) < self.min_balance:
            return (
                False,
                f"Cannot withdraw below minimum balance of ${self.min_balance:.2f}",
            )
        self.balance -= amount
        transaction = Transaction("withdrawal", amount, self)
        self.transaction_history.append(transaction)
        return (True, f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")

    def apply_interest(self) -> Tuple[bool, str]:
        """Apply interest to the current balance and record the transaction."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        transaction = Transaction("interest", interest, self)
        self.transaction_history.append(transaction)
        return (
            True,
            f"Applied interest: ${interest:.2f}. New balance: ${self.balance:.2f}",
        )


class CheckingAccount(Account):
    """Checking account implementation with an overdraft limit."""

    def __init__(
        self,
        account_number: str,
        owner_name: str,
        balance: float = 0.0,
        overdraft_limit: float = 100.0,
    ):
        super().__init__(account_number, owner_name, balance)
        # overdraft_limit is a positive number representing how far negative the
        # balance may go
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> Tuple[bool, str]:
        """Withdraw allowing balance to go negative up to -overdraft_limit."""
        if amount <= 0:
            return (False, "Withdrawal amount must be positive")
        # After withdrawal, balance must not be less than -overdraft_limit
        if (self.balance - amount) < -self.overdraft_limit:
            return (
                False,
                f"Cannot exceed overdraft limit of ${self.overdraft_limit:.2f}",
            )
        self.balance -= amount
        transaction = Transaction("withdrawal", amount, self)
        self.transaction_history.append(transaction)
        if self.balance < 0:
            return (
                True,
                f"Withdrew ${amount:.2f}. \
                        New balance: ${self.balance:.2f} (Overdraft)",
            )
        return (True, f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")


class Bank:
    """Simple container for multiple accounts facilitating account
    creation and transfers."""

    def __init__(self, name: str):
        self.name = name
        # Map account_number -> Account instance
        self.accounts: Dict[str, Account] = {}

    def create_account(
        self,
        account_type: str,
        account_number: str,
        owner_name: str,
        initial_balance: float = 0.0,
        **kwargs,
    ) -> Tuple[bool, str]:
        """Create and register a new account of the requested type.

        Returns a (success, message) tuple. `account_type` is case-insensitive.
        Additional keyword arguments are forwarded to the account constructor.
        """
        if account_number in self.accounts:
            return (False, "Account number already exists")

        account_type_lower = account_type.lower()
        account: Account

        if account_type_lower == "savings":
            account = SavingsAccount(
                account_number, owner_name, initial_balance, **kwargs
            )
        elif account_type_lower == "checking":
            account = CheckingAccount(
                account_number, owner_name, initial_balance, **kwargs
            )
        else:
            return (False, "Invalid account type")
        self.accounts[account_number] = account
        return (True, f"{account_type.title()} account created successfully")

    def get_account(self, account_number: str) -> Optional[Account]:
        """Return the account by `account_number` or None if not found."""
        return self.accounts.get(account_number)

    def transfer(
        self, from_account_number: str, to_account_number: str, amount: float
    ) -> Tuple[bool, str]:
        """Transfer `amount` from one account to another.

        The method will attempt to withdraw from the source account and, on
        success, deposit into the destination account. It returns a
        (success, message) tuple describing the result.
        """
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)
        if (not from_account) or (not to_account):
            return (False, "One or both accounts not found")
        withdraw_result = from_account.withdraw(amount)
        if not withdraw_result[0]:
            return (False, f"Transfer failed: {withdraw_result[1]}")
        to_account.deposit(amount)
        return (
            True,
            f"Transferred ${amount:.2f} from {from_account_number} "
            "to {to_account_number}",
        )
