"""Tests for `src/exercises/banking_system`.

Covers Transaction formatting, Account.deposit behavior, SavingsAccount and
CheckingAccount withdrawal rules, interest application, and Bank account
management (creation, retrieval, transfers).
"""

import sys
from pathlib import Path

# Ensure src/ is importable in various environments
repo_root = Path(__file__).resolve().parent.parent
src_dir = repo_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from exercises.banking_system import (
    Bank,
    CheckingAccount,
    SavingsAccount,
)


def test_transaction_str_and_history_order():
    acc = SavingsAccount("A1", "Alice", balance=0)
    # perform a deposit
    acc.deposit(50)
    assert len(acc.get_transaction_history()) == 1
    tx = acc.get_transaction_history()[0]
    assert str(tx) == "Deposit - $50.00"


def test_deposit_validation_and_balance_update():
    acc = SavingsAccount("S1", "Bob", balance=10)
    ok, msg = acc.deposit(40)
    assert ok is True
    assert "Deposited $40.00" in msg
    assert acc.get_balance() == 50

    ok2, msg2 = acc.deposit(-5)
    assert ok2 is False
    assert "Deposit amount must be positive" in msg2


def test_savings_withdraw_min_balance_enforced():
    acc = SavingsAccount("S2", "Carol", balance=200, min_balance=100)
    # valid withdrawal that keeps balance >= min_balance
    ok, msg = acc.withdraw(50)
    assert ok is True
    assert acc.get_balance() == 150

    # withdrawal that would go below min_balance should fail
    ok2, msg2 = acc.withdraw(60)  # would leave 90 < 100
    assert ok2 is False
    assert "Cannot withdraw below minimum balance" in msg2

    # negative withdrawal invalid
    ok3, msg3 = acc.withdraw(-10)
    assert ok3 is False
    assert "Withdrawal amount must be positive" in msg3


def test_apply_interest_records_transaction_and_updates_balance():
    acc = SavingsAccount("S3", "Dora", balance=100, interest_rate=0.05)
    ok, msg = acc.apply_interest()
    assert ok is True
    assert "Applied interest" in msg
    # 100 * 0.05 = 5
    assert acc.get_balance() == 105
    # last transaction should be interest of 5.00
    last_tx = acc.get_transaction_history()[-1]
    assert str(last_tx) == "Interest - $5.00"


def test_checking_withdraw_allows_overdraft_up_to_limit():
    acc = CheckingAccount("C1", "Eve", balance=50, overdraft_limit=100)
    # withdraw within overdraft (should succeed and indicate overdraft in message)
    ok, msg = acc.withdraw(140)  # leaves -90
    assert ok is True
    assert "(Overdraft)" in msg
    assert acc.get_balance() == -90

    # withdraw that would exceed overdraft should fail
    acc2 = CheckingAccount("C2", "Frank", balance=0, overdraft_limit=100)
    ok2, msg2 = acc2.withdraw(150)  # would leave -150 beyond -100 limit
    assert ok2 is False
    assert "Cannot exceed overdraft limit" in msg2


def test_bank_create_account_get_and_duplicate_and_invalid():
    bank = Bank("LocalBank")
    ok, msg = bank.create_account("savings", "100", "Gina", initial_balance=500)
    assert ok is True
    assert "Savings account created successfully" in msg
    acc = bank.get_account("100")
    assert isinstance(acc, SavingsAccount)

    # duplicate account number not allowed
    ok2, msg2 = bank.create_account("checking", "100", "Henry")
    assert ok2 is False
    assert "Account number already exists" in msg2

    # invalid account type
    ok3, msg3 = bank.create_account("investment", "200", "Ivy")
    assert ok3 is False
    assert "Invalid account type" in msg3


def test_transfer_success_and_failure_cases():
    bank = Bank("XBank")
    bank.create_account("checking", "A", "Alice", initial_balance=200)
    bank.create_account("savings", "B", "Bob", initial_balance=50)

    # successful transfer
    ok, msg = bank.transfer("A", "B", 100)
    assert ok is True
    assert "Transferred $100.00" in msg
    a = bank.get_account("A")
    b = bank.get_account("B")
    assert a.get_balance() == 100
    assert b.get_balance() == 150

    # transfer fails when source cannot withdraw (e.g., savings min_balance)
    bank.create_account("savings", "C", "Cara", initial_balance=120, min_balance=100)
    ok2, msg2 = bank.transfer("C", "B", 30)  # would leave 90 < min_balance
    assert ok2 is False
    assert "Transfer failed" in msg2

    # transfer fails when account doesn't exist
    ok3, msg3 = bank.transfer("X", "B", 10)
    assert ok3 is False
    assert "One or both accounts not found" in msg3
