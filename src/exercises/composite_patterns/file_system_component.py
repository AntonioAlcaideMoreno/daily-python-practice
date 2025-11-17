from abc import ABC, abstractmethod


class FileSystemComponent(ABC):
    """Abstract base class for all file system components.

    This class serves as the 'Component' in the Composite pattern.
    """

    def __init__(self, name):
        # TODO: Initialize the component with a name
        # TODO: Store the name as a private attribute _name
        self._name = name

    @property
    def name(self):
        # TODO: Implement getter that returns the private _name attribute
        return self._name

    @name.setter
    def name(self, value):
        # TODO: Implement setter that validates the name is not empty
        # TODO: Raise ValueError with message "Name cannot be empty" if value is empty
        # TODO: Set self._name to the value if validation passes
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @abstractmethod
    def get_size(self):
        """Returns the size of the component."""
        # TODO: Abstract method that must be implemented by concrete classes
        # TODO: Should return the size of the component in KB
        pass

    @abstractmethod
    def display(self, indent=0):
        """Displays the component with proper indentation."""
        # TODO: Abstract method that must be implemented by concrete classes
        # TODO: Should return a string representation with proper indentation
        # TODO: indent parameter specifies number of spaces for indentation
        pass

    @abstractmethod
    def add(self, component):
        """Adds a component to this component."""
        # TODO: Abstract method for adding child components
        # TODO: Should add the component to this component's children
        pass

    @abstractmethod
    def remove(self, component):
        """Removes a component from this component."""
        # TODO: Abstract method for removing child components
        # TODO: Should remove the component from this component's children
        pass

    @abstractmethod
    def get_component(self, name):
        """Retrieves a component by name."""
        # TODO: Abstract method for finding child components by name
        # TODO: Should return the component if found, None otherwise
        pass
