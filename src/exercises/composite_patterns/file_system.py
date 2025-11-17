from .directory import Directory


class FileSystem:
    """Represents the overall file system.

    This class serves as a facade for working with the file system components.
    """

    def __init__(self):
        # TODO: Create root directory with name "root"
        # TODO: Store it as self.root
        self.root = Directory("root")

    def _get_directory_from_path(self, path):
        """Helper method to navigate to a directory from a path."""
        # TODO: If path is empty or "/", return self.root
        # TODO: Split path by "/" and remove empty parts
        # TODO: Navigate through path parts starting from root
        # TODO: For each part except last, get component and verify it's a directory
        # TODO: Return (parent_directory, target_component) tuple
        # TODO: Raise ValueError if path not found or component is not directory
        if not path or path == "/":
            return (self.root, None)
        parts = (part.strip() for part in path.split(separator="/"))
        found_item = self.root.find_component_recursive(parts[-1])
        if not found_item:
            raise ValueError(f"Component {parts[-1]} not found")
        return (Directory(parts[-2]), Directory(parts[-1], 1))

    def add_to_path(self, path, component):
        """Adds a component at the specified path."""
        # TODO: If path is empty or "/", add component to root directory
        # TODO: Otherwise, get parent directory from path
        # TODO: Add component to parent directory
        if not path or path == "/":
            self.root.add(component)
            return None
        self._get_directory_from_path(path)[0].add(component)

    def remove_from_path(self, path):
        """Removes a component at the specified path."""
        # TODO: Check if trying to remove root directory (raise ValueError)
        # TODO: Get parent directory and target component from path
        # TODO: If component exists, remove it from parent
        # TODO: Otherwise raise ValueError for path not found
        if path == "root":
            raise ValueError("Cannot remove root folder")
        parent_directory, target_component = self._get_directory_from_path(path)

    def get_from_path(self, path):
        """Retrieves a component at the specified path."""
        # TODO: If path is empty or "/", return root directory
        # TODO: Otherwise, use _get_directory_from_path to get component
        # TODO: Return the component
        if not path or path == "/":
            return self.root
        return self._get_directory_from_path(path)[1]

    def display(self):
        """Displays the entire file system."""
        # TODO: Return the result of calling display() on root directory
        return self.root.display()

    def get_total_size(self):
        """Returns the total size of all files in the system."""
        # TODO: Return the result of calling get_size() on root directory
        return self.root.get_size()
