"""Library management helpers: Book, User and Library classes.

This module provides a very small in-memory model of a library system
intended for learning and exercises. It exposes three main classes:

- Book: represents a single book and its availability state
- User: represents a library user and the list of borrowed books
- Library: manages collections of Book and User objects and basic
  operations like borrowing books and computing simple statistics

The implementation is deliberately simple (no persistence, no concurrency
handling) but includes clear docstrings and comments to make the logic
easy to follow for new readers.
"""

from __future__ import annotations

from typing import Dict, List, Optional


class Book:
    """A book with a title, author and ISBN identifier.

    Attributes:
        title (str): Book title
        author (str): Book author name
        isbn (str): Unique ISBN identifier
        available (bool): True if the book is available to borrow
        borrower (Optional[User]): The user who borrowed the book (if any)
    """

    borrower: Optional["User"]

    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.borrower = None

    def __str__(self) -> str:
        """Return a human-friendly representation including availability."""
        status = "Available" if self.available else "Not Available"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {status}"


class User:
    """A library user with an identifier and a borrowed-books list.

    Attributes:
        user_id (str): Unique user identifier
        name (str): User full name
        books_borrowed (List[Book]): List of currently borrowed books
    """

    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.books_borrowed: List[Book] = []

    def __str__(self) -> str:
        return (
            f"User: {self.name} (ID: {self.user_id}) - Books borrowed: "
            + f"{len(self.books_borrowed)}"
        )


class Library:
    """A very small library manager.

    The Library class keeps in-memory lists of books and users and offers
    methods to add books/users, borrow books, and compute simple statistics.

    Note: This is not thread-safe and does not validate ISBN uniqueness.
    """

    def __init__(self, name: str):
        self.name = name
        # Lists hold Book and User instances
        self.books: List[Book] = []
        self.users: List[User] = []

    def add_book(self, book: Book) -> None:
        """Add a Book to the library collection."""
        self.books.append(book)

    def add_user(self, user: User) -> None:
        """Register a new User in the library."""
        self.users.append(user)

    def borrow_book(self, book_isbn: str, user_id: str) -> str:
        """Attempt to lend a book identified by `book_isbn` to the user.

        Return a short status string describing the outcome. The method
        performs simple checks in order:
          1. Does the book exist?
          2. Does the user exist?
          3. Is the book available?
        """

        # Locate the book and user (or None if not found)
        book = next((b for b in self.books if b.isbn == book_isbn), None)
        user = next((u for u in self.users if u.user_id == user_id), None)

        # Handle error cases explicitly with short messages
        if not book:
            return "Book not found"
        if not user:
            return "User not found"
        if not book.available:
            return "Book is not available"

        # Mark the book as borrowed and record the borrower
        book.available = False
        book.borrower = user
        user.books_borrowed.append(book)
        return "Book borrowed successfully"

    def get_statistics(self) -> Dict[str, int]:
        """Return simple statistics about the library's current state.

        The statistics dictionary contains:
          - total_books: number of books in the collection
          - available_books: number of books currently available
          - borrowed_books: number of books currently lent out
          - total_users: number of registered users
          - users_with_books: number of users who have borrowed at least one book
        """
        total_books = len(self.books)
        available_books = sum(1 for book in self.books if book.available)

        # Build the stats dictionary with clear keys and values
        stats = {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": total_books - available_books,
            "total_users": len(self.users),
            "users_with_books": sum(1 for user in self.users if user.books_borrowed),
        }
        return stats

    def __str__(self) -> str:
        return (
            f"{self.name} Library with {len(self.books)} books and "
            + f"{len(self.users)} users"
        )
