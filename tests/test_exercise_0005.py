import pytest

from exercises.securemessenger_class_and_functions import SecureMessenger

# Tests for securemessenger_class_and_functions.py file


@pytest.fixture
def messenger():
    """Fresh SecureMessenger using the default password ('secure123')."""
    return SecureMessenger("alice")


def test_login_success_and_add_message(messenger):
    # successful login should return success and allow adding messages
    assert messenger.login("secure123") == "Login successful"
    assert messenger.add_message("hello") == "Message added: hello"
    assert messenger.get_messages() == "hello"


def test_login_failure_increments_attempts_and_blocks_actions(messenger):
    # failed login attempts increment counter and do not authenticate
    assert messenger.login("wrong") == "Login failed: Incorrect password"
    assert messenger.login("nope") == "Login failed: Incorrect password"
    assert messenger.get_login_attempts() == "Login attempts: 2"
    # still not logged in -> cannot add or view messages
    assert messenger.add_message("x") == "Error: You must be logged in to add messages"
    assert messenger.get_messages() == "Error: You must be logged in to view messages"


def test_messages_flow_and_no_messages(messenger):
    # when logged in and no messages, get_messages returns "No messages"
    messenger.login("secure123")
    assert messenger.get_messages() == "No messages"
    # messages should accumulate in order and be returned joined by newline
    messenger.add_message("first")
    messenger.add_message("second")
    assert messenger.get_messages() == "first\nsecond"


def test_custom_password_and_attempts_count():
    # a messenger created with a custom password should require that password
    m = SecureMessenger("bob", password="letmein")
    assert m.login("secure123") == "Login failed: Incorrect password"
    assert m.login("letmein") == "Login successful"
    # two attempts total
    assert m.get_login_attempts() == "Login attempts: 2"
