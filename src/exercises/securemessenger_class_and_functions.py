class SecureMessenger:
    """
    Simple secure messenger class that manages messages behind a login.

    Attributes:
        username (str): Public username associated with the messenger.
        __password (str): Internal password used to authenticate (default 'secure123').
        __messages (list[str]): Internal list storing messages added while logged in.
        __login_attempts (int): Counter of attempted logins.
        __is_logged_in (bool): Flag indicating whether the user is currently logged in.

    Usage:
        - Call login(password) to authenticate. Each call increments the login attempt
          counter.
        - Once logged in, add_message(message) appends a message to the internal store.
        - get_messages() returns the stored messages (joined by newline) or a suitable
          message if empty.
        - get_login_attempts() returns a human-readable count of login attempts.
    """

    def __init__(self, username, password="secure123"):
        self.username = username
        self.__password = password
        self.__messages = []
        self.__login_attempts = 0
        self.__is_logged_in = False

    def add_message(self, message):
        """
        Add a message to the internal message list.

        Args:
            message (str): Text to store.

        Returns:
            str: Confirmation when the message is added, or an error string when not
                 logged in.

        Behavior:
            - Only stores messages when the user is authenticated
              (self.__is_logged_in is True).
            - Does not raise exceptions; returns error strings to indicate failure
              (keeps API simple).
        """
        # Only allow adding messages when logged in
        if self.__is_logged_in:
            self.__messages.append(message)
            return f"Message added: {message}"
        return "Error: You must be logged in to add messages"

    def login(self, password):
        """
        Attempt to log in using the provided password.

        Args:
            password (str): Password to validate.

        Returns:
            str: "Login successful" on success, otherwise an error message.

        Side effects:
            - Increments the login attempts counter on each call.
            - Sets internal logged-in flag on successful authentication.
        """
        self.__login_attempts += 1
        if self.__password == password:
            self.__is_logged_in = True
            return "Login successful"
        return "Login failed: Incorrect password"

    def get_messages(self):
        """
        Retrieve stored messages as a single string.

        Returns:
            str: Joined messages separated by newlines, "No messages" if none,
                 or an error string if not logged in.

        Notes:
            - Requires authentication; otherwise returns an error message.
            - Keeps the internal list intact (no deletion or mutation performed).
        """
        if self.__is_logged_in:
            if not self.__messages:
                return "No messages"
            return "\n".join(self.__messages)
        return "Error: You must be logged in to view messages"

    def get_login_attempts(self):
        """
        Return a human-readable count of login attempts.

        Returns:
            str: Example: "Login attempts: 3"
        """
        return f"Login attempts: {self.__login_attempts}"
