"""
Tests for the composite pattern file system implementation.

Places tested:
- exercises.composite_patterns.file_system_component.FileSystemComponent
    (via concrete subclasses)
- exercises.composite_patterns.file.File
- exercises.composite_patterns.directory.Directory
- exercises.composite_patterns.file_system.FileSystem

The tests are written to be resilient to minor formatting differences in display()
but enforce functional behaviour: size accounting, add/remove, name validation,
recursive search and basic FileSystem root operations.
"""

import sys
from pathlib import Path

import pytest

from exercises.composite_patterns.directory import Directory
from exercises.composite_patterns.file import File
from exercises.composite_patterns.file_system import FileSystem

# Ensure src/ is on sys.path so imports work consistently in CI / IDE runs.
repo_src = Path(__file__).resolve().parent.parent  # this points to <repo>/src
if str(repo_src) not in sys.path:
    sys.path.insert(0, str(repo_src))


def test_file_name_size_and_display_and_name_validation():
    f = File("notes.txt", 10)
    # name getter and size
    assert f.name == "notes.txt"
    assert f.get_size() == 10
    # display should include the file name and size; indentation should be respected
    assert "File: notes.txt" in f.display(2)
    assert "(10 KB)" in f.display(2)

    # setting an empty name should raise ValueError (validation in setter)
    with pytest.raises(ValueError):
        f.name = ""


def test_file_negative_size_raises():
    with pytest.raises(ValueError):
        File("bad.bin", -5)


def test_directory_add_get_size_display_and_duplicate_and_remove():
    d = Directory("docs")
    f1 = File("a.txt", 2)
    f2 = File("b.txt", 3)

    # add files and verify retrieval and size aggregation
    d.add(f1)
    d.add(f2)
    assert d.get_component("a.txt") is f1
    assert d.get_size() == 5

    # display should include directory header and children's display strings
    disp = d.display(indent=0)
    assert "Directory: docs" in disp
    assert "File: a.txt" in disp and "File: b.txt" in disp

    # adding a component with the same name should raise ValueError
    with pytest.raises(ValueError):
        d.add(File("a.txt", 1))

    # removing existing component works
    d.remove(f1)
    assert d.get_component("a.txt") is None

    # removing non-existing component should raise
    with pytest.raises(ValueError):
        d.remove(File("nonexistent.txt", 1))


def test_find_component_recursive_and_nested_directories():
    root = Directory("root")
    sub = Directory("subdir")
    deep_file = File("deep.txt", 4)

    sub.add(deep_file)
    root.add(sub)

    # direct lookup on subdir works
    assert root.get_component("subdir") is sub

    # recursive search finds the deep file
    found = root.find_component_recursive("deep.txt")
    assert found is deep_file

    # searching for missing returns None
    assert root.find_component_recursive("no-such-file") is None


def test_filesystem_root_add_get_and_total_size_and_display():
    fs = FileSystem()

    # by default root exists and is a Directory
    root = fs.get_from_path("/")  # expected to return root directory
    assert root is not None
    assert root.name == "root"

    # add a file to root via FileSystem API and verify
    readme = File("readme.md", 1)
    fs.add_to_path("/", readme)

    # retrieving root and checking component presence
    root_after = fs.get_from_path("/")
    assert root_after.get_component("readme.md") is not None
    assert fs.get_total_size() == 1

    # display should include root header and the added file somewhere
    out = fs.display()
    assert "Directory: root" in out
    assert "readme.md" in out
