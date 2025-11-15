"""
Decorators exercise 7 decorators_e007: Authorization Decorator (Access Control)

Concepts: Permission checking, role-based access control, decorator chaining
"""

from functools import update_wrapper

# Global context (simulating request context in web frameworks)
current_user = None


class User:
    """Simple user model with roles and permissions"""

    def __init__(self, username, roles=None, permissions=None):
        """
        Initialize a user.

        Parameters:
            username: User identifier
            roles: List of role names (e.g., ["admin", "moderator"])
            permissions: List of permission names (e.g., ["read", "write", "delete"])
        """
        self.username = username
        self.roles = set(roles or [])
        self.permissions = set(permissions or [])

    def has_role(self, role):
        """Check if user has a specific role"""
        return role in self.roles

    def has_permission(self, permission):
        """Check if user has a specific permission"""
        return permission in self.permissions

    def __repr__(self):
        return f"User({self.username}, roles={self.roles}, perms={self.permissions})"


class AuthorizationError(Exception):
    """Raised when authorization check fails"""

    pass


class RequireRole:
    """
    Decorator that requires user to have specific role(s).

    Usage:
        @RequireRole("admin")
        def delete_user(user_id):
            pass

        @RequireRole(["admin", "moderator"])  # User needs ANY of these roles
        def ban_user(user_id):
            pass
    """

    def __init__(self, func=None, required_roles=None):
        """
        Initialize the role requirement decorator.

        Parameters:
            func: The function being decorated (None if used as factory)
            required_roles: String or list of role names required
        """
        # TODO: Store function and required roles
        self.func = func
        # Simple and correct:
        if isinstance(required_roles, str):
            self.required_roles = {required_roles}  # Single role → set with one element
        else:
            self.required_roles = set(required_roles or [])  # List → set

        # Hint: Convert required_roles to a set for efficient checking
        # If it's a string, wrap it in a list first
        # Preserve function metadata if func is not None
        if func is not None:
            update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        """
        Check user role before executing function.

        Flow:
        1. Check if current_user is set
        2. Check if user has ANY of the required roles
        3. If authorized: execute function
        4. If not authorized: raise AuthorizationError
        """
        # TODO: Check current_user is not None (user must be logged in)
        if not current_user:
            raise AuthorizationError("No user logged in")
        # if not any(current_user.has_role(r) for r in self.required_roles):
        if not (self.required_roles & current_user.roles):
            raise AuthorizationError(
                f"User lacks required role. Required: {self.required_roles}, "
                + "User roles: {current_user.roles}"
            )

        # TODO: Check if user has any of the required roles
        # Hint: if not any(current_user.has_role(r) for r in self.required_roles):
        #           raise AuthorizationError(f"User lacks required role")

        # TODO: If authorized, call the original function
        return self.func(*args, **kwargs)


def require_role(required_roles):
    """
    Factory function for parameterized role requirement.

    Usage:
        @require_role("admin")
        @require_role(["editor", "moderator"])
        def publish_post(post_id):
            pass
    """

    def decorator(func):
        return RequireRole(func, required_roles=required_roles)

    return decorator


class RequirePermission:
    """
    Decorator that requires user to have specific permission(s).

    Similar to RequireRole but checks permissions instead.
    """

    def __init__(self, func=None, required_permissions=None):
        """
        Initialize the permission requirement decorator.

        Parameters:
            func: The function being decorated
            required_permissions: String or list of permission names
        """
        # TODO: Similar to RequireRole, store function and required permissions
        self.func = func
        # Simple and correct:
        if isinstance(required_permissions, str):
            self.required_permissions = {
                required_permissions
            }  # Single role → set with one element
        else:
            self.required_permissions = set(required_permissions or [])  # List → set
        if func is not None:
            update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        """
        Check user permission before executing function.

        Similar to RequireRole but checks permissions.
        """
        # TODO: Similar logic to RequireRole.__call__
        if not current_user:
            raise AuthorizationError("No user logged in")
        if not (
            self.required_permissions & current_user.permissions
        ):  # Same doubt as in RequireRole about which approach is better
            raise AuthorizationError(
                "User lacks required permission. Required: "
                + f"{self.required_permissions}, User permissions: "
                + f"{current_user.permissions}"
            )

        return self.func(*args, **kwargs)


def require_permission(required_permissions):
    """
    Factory function for parameterized permission requirement.
    """

    def decorator(func):
        return RequirePermission(func, required_permissions=required_permissions)

    return decorator


# Test scenarios
# Define some test users with different roles and permissions

admin_user = User(
    "alice", roles=["admin"], permissions=["read", "write", "delete", "manage"]
)
editor_user = User("bob", roles=["editor"], permissions=["read", "write"])
viewer_user = User("charlie", roles=["viewer"], permissions=["read"])


# Protected functions
@require_role("admin")
def delete_user(user_id):
    """Only admins can delete users"""
    return f"User {user_id} deleted by {current_user.username}"


@require_permission("write")
def create_post(title, content):
    """Only users with 'write' permission can create posts"""
    return f"Post '{title}' created by {current_user.username}"


@require_role(["admin", "moderator"])
def moderate_content(content_id):
    """Admins and moderators can moderate content"""
    return f"Content {content_id} moderated by {current_user.username}"


@require_permission("read")
def view_post(post_id):
    """Any user with 'read' permission can view posts"""
    return f"Post {post_id} viewed by {current_user.username}"


# Tests
if __name__ == "__main__":
    print("=== Test 1: Admin can delete users ===")
    current_user = admin_user
    try:
        result = delete_user(123)
        print(f"✅ {result}\n")
    except AuthorizationError as e:
        print(f"❌ Authorization failed: {e}\n")

    print("=== Test 2: Viewer cannot delete users ===")
    current_user = viewer_user
    try:
        result = delete_user(123)
        print(f"✅ {result}\n")
    except AuthorizationError as e:
        print(f"❌ Authorization failed: {e}\n")

    print("=== Test 3: Editor can create posts ===")
    current_user = editor_user
    try:
        result = create_post("Hello", "World")
        print(f"✅ {result}\n")
    except AuthorizationError as e:
        print(f"❌ Authorization failed: {e}\n")

    print("=== Test 4: Viewer cannot create posts ===")
    current_user = viewer_user
    try:
        result = create_post("Hello", "World")
        print(f"✅ {result}\n")
    except AuthorizationError as e:
        print(f"❌ Authorization failed: {e}\n")

    print("=== Test 5: Moderator can moderate content ===")
    moderator_user = User("david", roles=["moderator"], permissions=["read"])
    current_user = moderator_user
    try:
        result = moderate_content(456)
        print(f"✅ {result}\n")
    except AuthorizationError as e:
        print(f"❌ Authorization failed: {e}\n")

    print("=== Test 6: No user logged in ===")
    current_user = None
    try:
        result = view_post(789)
        print(f"✅ {result}\n")
    except AuthorizationError as e:
        print(f"❌ Authorization failed: {e}\n")

    print("=== Test 7: Stacking authorization decorators ===")

    @require_role("admin")
    @require_permission("delete")
    def super_sensitive_operation():
        return f"Sensitive operation executed by {current_user.username}"

    print("Admin with 'delete' permission:")
    current_user = User("admin_with_delete", roles=["admin"], permissions=["delete"])
    try:
        result = super_sensitive_operation()
        print(f"✅ {result}\n")
    except AuthorizationError as e:
        print(f"❌ Authorization failed: {e}\n")

    print("Admin without 'delete' permission:")
    current_user = User("admin_no_delete", roles=["admin"], permissions=["read"])
    try:
        result = super_sensitive_operation()
        print(f"✅ {result}\n")
    except AuthorizationError as e:
        print(f"❌ Authorization failed: {e}\n")

    print("✅ All tests complete!")
