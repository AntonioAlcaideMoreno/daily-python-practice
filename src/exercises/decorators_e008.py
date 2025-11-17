"""
Decorators exercise 8 decorators_e008: Property Decorator & Descriptor Protocol

Concepts: Descriptors, __get__/__set__/__delete__, metaprogramming
"""

from functools import update_wrapper


class ValidatedProperty:
    """
    A descriptor that validates attribute values before assignment.

    Descriptors are Python's mechanism for customizing attribute access.
    They implement the descriptor protocol: __get__, __set__, __delete__.

    When you access obj.attr, Python calls descriptor.__get__(obj, type(obj))
    When you assign obj.attr = value, Python calls descriptor.__set__(obj, value)

    This enables implementing properties, type checking, caching, etc.
    """

    def __init__(self, name, validator=None, default=None):
        """
        Initialize the validated property.

        Parameters:
            name: Name of the attribute (e.g., "age", "email")
            validator: Callable that validates values (raises ValueError if invalid)
            default: Default value if not set
        """
        # TODO: Store configuration
        self.name = name
        self.validator = validator
        self.default = default
        self.data = {}
        # Hint: self.name, self.validator, self.default
        # Also need: self.data = {} to store instance-specific values

    def __get__(self, obj, objtype=None):
        """
        Called when attribute is accessed: result = obj.attr

        Parameters:
            obj: The instance (e.g., person in person.age)
            objtype: The class (e.g., Person class)

        Returns:
            The value stored for this attribute on this instance
        """
        # TODO: Return the value stored for this instance
        if obj is None:
            return self
        return self.data.get(id(obj), self.default)
        # Hint: If obj is None (accessing via class), return self (the descriptor)
        # Otherwise, return self.data.get(id(obj), self.default)

    def __set__(self, obj, value):
        """
        Called when attribute is assigned: obj.attr = value

        Parameters:
            obj: The instance
            value: The new value
        """
        # TODO: Validate the value if validator is set
        if self.validator is not None and not self.validator(
            value
        ):  # If validator exists and it returns an invalid (False) result,
            # then raise an error
            raise ValueError(f"Invalid value for {self.name}")
        # Hint: if self.validator and not self.validator(value):
        #           raise ValueError(f"Invalid value for {self.name}")
        self.data[id(obj)] = value

        # TODO: Store the validated value
        # Hint: self.data[id(obj)] = value

    def __delete__(self, obj):
        """
        Called when attribute is deleted: del obj.attr

        Parameters:
            obj: The instance
        """
        # TODO: Remove the value for this instance
        self.data.pop(id(obj), None)
        # Hint: self.data.pop(id(obj), None)


class ComputedProperty:
    """
    A descriptor that computes property values from other attributes.

    Example: full_name is computed from first_name and last_name
    """

    def __init__(self, func):
        """
        Initialize the computed property.

        Parameters:
            func: Function that computes the value
        """
        # TODO: Store the computation function
        self.func = func
        update_wrapper(self, func)
        # Hint: self.func = func
        # Also preserve metadata: update_wrapper(self, func)

    def __get__(self, obj, objtype=None):
        """
        Called when property is accessed.

        Computes the value by calling self.func(obj)
        """
        # TODO: If accessed via class (obj is None), return self
        if not obj:
            return self
        return self.func(obj)
        # Otherwise, compute and return the value
        # Hint: if obj is None: return self
        #       return self.func(obj)

    def __set__(self, obj, value):
        """
        Computed properties are read-only.

        Raise AttributeError if someone tries to set it.
        """
        # TODO: Raise AttributeError
        raise AttributeError("Computed properties are read-only")
        # Hint: raise AttributeError(f"Cannot set computed property")

    def __delete__(self, obj):
        """ "
        Computed properties cannot be deleted

        Raise AttributeError if someone tries to delete it.
        """
        raise AttributeError("Computed properties cannot be deleted")


class CachedProperty:
    """
    A descriptor that caches computed values.

    First access: Compute the value (slow)
    Subsequent accesses: Return cached value (fast)
    """

    def __init__(self, func):
        """
        Initialize the cached property.

        Parameters:
            func: Function that computes the value
        """
        # TODO: Store function and cache dictionary
        self.func = func
        self._cache = {}
        update_wrapper(self, func)
        # Hint: self.func = func, self.cache = {}
        # Also: update_wrapper(self, func)

    def __get__(self, obj, objtype=None):
        """
        Called when property is accessed.

        Returns cached value if available, otherwise computes and caches.
        """
        # TODO: Check if value is cached
        if id(obj) in self._cache:
            return self._cache[id(obj)]
        self._cache[id(obj)] = self.func(obj)
        return self._cache[id(obj)]
        # Hint: obj_id = id(obj)
        #       if obj_id in self.cache: return self.cache[obj_id]

        # TODO: Compute and cache the value
        # Hint: value = self.func(obj)
        #       self.cache[obj_id] = value
        #       return value

    def __set__(self, obj, value):
        """
        Cached properties are read-only.
        """
        # TODO: Raise AttributeError
        raise AttributeError("Cached properties are read-only")


# Example: Person class with validated and computed properties
class Person:
    """
    A person with validated and computed attributes.

    Demonstrates descriptor protocol with ValidatedProperty and ComputedProperty.
    """

    # Validated properties (with type checking)
    age = ValidatedProperty(
        "age", validator=lambda x: isinstance(x, int) and 0 <= x <= 150, default=0
    )

    email = ValidatedProperty(
        "email", validator=lambda x: isinstance(x, str) and "@" in x, default=""
    )

    def __init__(self, first_name, last_name, age=0, email=""):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age  # Calls ValidatedProperty.__set__
        self.email = email

    @ComputedProperty
    def full_name(self):
        """Computed from first_name and last_name"""
        return f"{self.first_name} {self.last_name}"

    @CachedProperty
    def expensive_computation(self):
        """Expensive computation, cached on first access"""
        import time

        print(f"  Computing expensive value for {self.first_name}...")
        time.sleep(0.5)  # Simulate expensive work
        return f"Result for {self.first_name}"


# Tests
if __name__ == "__main__":
    print("=== Test 1: Validated property assignment ===")
    person = Person("Alice", "Smith", age=30, email="alice@example.com")
    print(f"Name: {person.first_name}")
    print(f"Age: {person.age}")
    print(f"Email: {person.email}\n")

    print("=== Test 2: Computed property ===")
    print(f"Full name: {person.full_name}\n")

    print("=== Test 3: Invalid age assignment ===")
    try:
        person.age = 200  # Invalid: age > 150
        print("Age set to 200 (should not reach here)")
    except ValueError as e:
        print(f"✅ Validation failed as expected: {e}\n")

    try:
        person.age = -1  # Invalid: negative age
        print("Age set to -1 (should not reach here)")
    except ValueError as e:
        print(f"✅ Validation failed as expected: {e}\n")

    print("=== Test 4: Invalid email assignment ===")
    try:
        person.email = "invalid-email"  # Invalid: no @
        print("Email set to invalid value (should not reach here)")
    except ValueError as e:
        print(f"✅ Validation failed as expected: {e}\n")

    try:
        person.email = ""  # Invalid: empty email
        print("Email set to empty (should not reach here)")
    except ValueError as e:
        print(f"✅ Validation failed as expected: {e}\n")

    print("=== Test 5: Cached property (first access—slow) ===")
    import time

    start = time.time()
    result1 = person.expensive_computation
    elapsed1 = time.time() - start
    print(f"Result: {result1}")
    print(f"Time: {elapsed1:.3f}s\n")

    print("=== Test 6: Cached property (second access—fast) ===")
    start = time.time()
    result2 = person.expensive_computation
    elapsed2 = time.time() - start
    print(f"Result: {result2}")
    print(f"Time: {elapsed2:.6f}s (cached)\n")

    print("=== Test 7: Multiple instances with separate state ===")
    person1 = Person("Bob", "Jones", age=25, email="bob@example.com")
    person2 = Person("Charlie", "Brown", age=35, email="charlie@example.com")

    print(f"Person 1: {person1.full_name}, age {person1.age}")
    print(f"Person 2: {person2.full_name}, age {person2.age}")
    print("Changing person1 age to 26...")
    person1.age = 26
    print(f"Person 1 age: {person1.age}")
    print(f"Person 2 age: {person2.age} (unchanged)\n")

    print("=== Test 8: Attempt to delete computed property ===")
    try:
        del person.full_name  # Should raise AttributeError
        print("Computed property deleted (should not reach here)")
    except AttributeError as e:
        print(f"✅ Deletion failed as expected: {e}\n")

    print("=== Test 9: Attempt to set computed property ===")
    try:
        person.full_name = "New Name"  # Should raise AttributeError
        print("Computed property set (should not reach here)")
    except AttributeError as e:
        print(f"✅ Setting computed property failed as expected: {e}\n")

    print("=== Test 10: Test CachedProperty with multiple instances ===")
    person3 = Person("David", "Smith", age=40, email="david@example.com")
    start = time.time()
    result3 = person3.expensive_computation
    elapsed3 = time.time() - start
    print(f"Result for person3: {result3}")
    print(f"Time for first access: {elapsed3:.3f}s\n")

    start = time.time()
    result4 = person3.expensive_computation  # Should be cached
    elapsed4 = time.time() - start
    print(f"Result for person3 (cached): {result4}")
    print(f"Time for second access: {elapsed4:.6f}s (cached)\n")

    print("=== Test 11: Test deletion of validated properties ===")
    try:
        del person.age  # Should remove the age
        print("Age deleted successfully.")
    except Exception as e:
        print(f"Failed to delete age: {e}")

    print("=== Test 12: Test deletion of email property ===")
    try:
        del person.email  # Should remove the email
        print("Email deleted successfully.")
    except Exception as e:
        print(f"Failed to delete email: {e}")

    print("✅ All tests complete!")
