from .file_system_component import FileSystemComponent


class File(FileSystemComponent):
    """Represents a file in the file system.

    This class serves as the 'Leaf' in the Composite pattern.
    """

    def __init__(self, name, size):
        # TODO: Call parent constructor with name using super()
        # TODO: Validate that size is not negative
        # TODO: Raise ValueError with message "Size cannot be negative" if size < 0
        # TODO: Store size as private attribute _size
        super().__init__(name)
        if size < 0:
            raise ValueError("Size cannot be negative")
        self._size = size

    def get_size(self):
        # TODO: Return the file's size (_size attribute)
        return self._size

    def display(self, indent=0):
        # TODO: Return formatted string with indentation
        # TODO: Format: " " * indent + f"File: {self.name} ({self.get_size()} KB)"
        # TODO: Use the name property and get_size() method
        return " " * indent + f"File: {self.name} ({self.get_size()} KB)"

    def add(self, component):
        # TODO: Raise NotImplementedError with message "Cannot add components to a file"
        # TODO: Files are leaf nodes and cannot have children
        raise NotImplementedError("Cannot add components to a file")

    def remove(self, component):
        # TODO: Raise NotImplementedError with message "Cannot remove components from
        # a file"
        # TODO: Files are leaf nodes and cannot have children to remove
        raise NotImplementedError("Cannot remove components from a file")

    def get_component(self, name):
        # TODO: Raise NotImplementedError with message "Files don't have components"
        # TODO: Files are leaf nodes and don't contain other components
        raise NotImplementedError("Files don't have components")
