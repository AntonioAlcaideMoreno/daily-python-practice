"""Tests for `src/exercises/library_management.py`.

Covers basic behaviors of Book, User and Library classes:
- defaults and string representations
- adding books and users
- borrowing flow (success and error cases)
- statistics aggregation
"""

import sys
from pathlib import Path

# Ensure `src/` is importable (consistent across environments)
repo_root = Path(__file__).resolve().parent.parent
src_dir = repo_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from exercises.library_management import Book, Library, User


def test_book_and_user_defaults_and_str():
    b = Book("1984", "George Orwell", "ISBN-1234")
    assert b.title == "1984"
    assert b.author == "George Orwell"
    assert b.isbn == "ISBN-1234"
    assert b.available is True
    assert b.borrower is None
    s = str(b)
    assert "1984 by George Orwell" in s
    assert "ISBN-1234" in s
    assert "Available" in s

    u = User("u1", "Alice")
    assert u.user_id == "u1"
    assert u.name == "Alice"
    assert isinstance(u.books_borrowed, list)
    assert len(u.books_borrowed) == 0
    assert "User: Alice" in str(u)


def test_borrow_book_success_and_availability():
    lib = Library("Central")
    book = Book("Dune", "Frank Herbert", "ISBN-0001")
    user = User("u2", "Bob")

    lib.add_book(book)
    lib.add_user(user)

    # Successful borrow
    res = lib.borrow_book("ISBN-0001", "u2")
    assert res == "Book borrowed successfully"
    assert book.available is False
    assert book.borrower is user
    assert book in user.books_borrowed

    # Try borrowing again -> not available
    res2 = lib.borrow_book("ISBN-0001", "u2")
    assert res2 == "Book is not available"


def test_borrow_book_error_conditions():
    lib = Library("Small")
    # no books or users
    res = lib.borrow_book("NO-ISBN", "nouser")
    assert res == "Book not found"

    # add a book but no user
    b = Book("Sapiens", "Yuval Harari", "ISBN-42")
    lib.add_book(b)
    res = lib.borrow_book("ISBN-42", "nonexistent")
    assert res == "User not found"


def test_get_statistics_and_library_str():
    lib = Library("Branch")
    b1 = Book("A", "Author A", "a1")
    b2 = Book("B", "Author B", "b1")
    b3 = Book("C", "Author C", "c1")

    u1 = User("u10", "Carol")
    u2 = User("u11", "Dave")

    lib.add_book(b1)
    lib.add_book(b2)
    lib.add_book(b3)
    lib.add_user(u1)
    lib.add_user(u2)

    # borrow one book by u1
    assert lib.borrow_book("a1", "u10") == "Book borrowed successfully"

    stats = lib.get_statistics()
    assert stats["total_books"] == 3
    assert stats["available_books"] == 2
    assert stats["borrowed_books"] == 1
    assert stats["total_users"] == 2
    assert stats["users_with_books"] == 1

    s = str(lib)
    assert "Branch Library" in s
    assert "3 books" in s
    assert "2 users" in s
