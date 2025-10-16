import pytest

from exercises.bank_account import BankAccount


@pytest.fixture
def basic_account():
    """Fixture providing a basic bank account for testing."""
    return BankAccount("Test User", 1000.0)


def test_account_initialization():
    """Test account creation with valid and invalid initial balances."""
    # Test valid initialization
    account = BankAccount("John Doe", 100.0)
    assert account.owner_name == "John Doe"
    assert account.balance == 100.0

    # Test negative initial balance
    with pytest.raises(ValueError):
        BankAccount("John Doe", -100.0)


def test_owner_name_property(basic_account):
    """Test owner name getter and setter."""
    # Test getter
    assert basic_account.owner_name == "Test User"

    # Test setter with valid name
    basic_account.owner_name = "Jane Doe"
    assert basic_account.owner_name == "Jane Doe"

    # Test setter with empty name
    original_name = basic_account.owner_name
    basic_account.owner_name = ""
    assert basic_account.owner_name == original_name  # Name should not change


def test_balance_property(basic_account):
    """Test balance getter and setter."""
    # Test getter
    assert basic_account.balance == 1000.0

    # Test setter with valid amount
    basic_account.balance = 2000.0
    assert basic_account.balance == 2000.0

    # Test setter with negative amount
    original_balance = basic_account.balance
    basic_account.balance = -500.0
    assert basic_account.balance == original_balance  # Balance should not change


def test_deposit(basic_account):
    """Test deposit functionality with valid and invalid amounts."""
    # Test valid deposit
    assert basic_account.deposit(500.0) is True
    assert basic_account.balance == 1500.0

    # Test negative deposit
    assert basic_account.deposit(-100.0) is False
    assert basic_account.balance == 1500.0  # Balance should not change


def test_withdraw(basic_account):
    """Test withdrawal functionality with various scenarios."""
    # Test valid withdrawal
    assert basic_account.withdraw(500.0) is True
    assert basic_account.balance == 500.0

    # Test negative withdrawal
    assert basic_account.withdraw(-100.0) is False
    assert basic_account.balance == 500.0

    # Test excessive withdrawal
    assert basic_account.withdraw(1000.0) is False
    assert basic_account.balance == 500.0


def test_apply_interest(basic_account):
    """Test interest calculation and application."""
    initial_balance = basic_account.balance
    expected_interest = initial_balance * BankAccount.interest_rate

    earned_interest = basic_account.apply_interest()

    assert earned_interest == pytest.approx(expected_interest)
    assert basic_account.balance == pytest.approx(initial_balance + expected_interest)


def test_display_info(basic_account, capsys):
    """Test account information display."""
    basic_account.display_info()
    captured = capsys.readouterr()

    expected_output = (
        f"Account Owner: {basic_account.owner_name}\n"
        f"Balance: ${basic_account.balance}\n"
        f"Interest Rate: {BankAccount.interest_rate*100}%\n"
    )

    assert captured.out == expected_output


def test_class_interest_rate():
    """Test class-level interest rate attribute."""
    # Test default interest rate
    assert BankAccount.interest_rate == 0.02

    # Test interest rate modification
    original_rate = BankAccount.interest_rate
    BankAccount.interest_rate = 0.03
    assert BankAccount.interest_rate == 0.03

    # Restore original rate
    BankAccount.interest_rate = original_rate
