"""
Test suite for DatabaseConnection singleton pattern implementation.
Tests verify singleton behavior, connection management, and instance state.
"""

import pytest

from exercises.singleton_pattern import DatabaseConnection


@pytest.fixture
def db_connection():
    """
    Fixture providing a fresh database connection instance.
    Ensures connection is disconnected after each test.
    """
    connection = DatabaseConnection()
    yield connection
    connection.disconnect()


def test_singleton_returns_same_instance():
    """Verify that multiple instantiations return the same object."""
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2
    assert id(db1) == id(db2)


def test_initial_connection_state(db_connection):
    """Verify that new instances start in disconnected state."""
    assert db_connection.host == "localhost"
    assert not db_connection.connected


def test_connect_updates_state(db_connection):
    """Verify connect() method properly updates connection state."""
    db_connection.connect()
    assert db_connection.connected


def test_disconnect_updates_state(db_connection):
    """Verify disconnect() method properly updates connection state."""
    db_connection.connect()
    db_connection.disconnect()
    assert not db_connection.connected


def test_shared_state_between_instances():
    """Verify that all instances share the same state."""
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()

    db1.connect()
    assert db2.connected

    db2.disconnect()
    assert not db1.connected


def test_connection_messages(capsys):
    """Verify that connection methods print expected messages."""
    db = DatabaseConnection()

    db.connect()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Connected to database at localhost"

    db.disconnect()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Disconnected from database"


def test_multiple_connections_disconnections(db_connection):
    """Verify that multiple connect/disconnect cycles work correctly."""
    for _ in range(3):
        db_connection.connect()
        assert db_connection.connected
        db_connection.disconnect()
        assert not db_connection.connected
