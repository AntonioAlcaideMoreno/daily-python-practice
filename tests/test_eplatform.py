"""Tests for the simple e-learning domain objects in `exercises.eplatform`.

This file follows the project's test conventions (ensure `src/` on sys.path,
use pytest style assertions, and keep tests small and focused).
"""

import sys
from pathlib import Path

# Ensure `src/` is importable so tests run consistently in different environments
repo_root = Path(__file__).resolve().parent.parent
src_dir = repo_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from exercises.eplatform import Course, Instructor, Student


def test_course_initialization_and_defaults():
    c = Course("Math 101", "Basic math")
    assert c.title == "Math 101"
    assert c.description == "Basic math"
    assert c.max_capacity == 30
    assert c.instructor is None
    assert isinstance(c.students, list) and c.students == []
    assert isinstance(c.completed_students, list) and c.completed_students == []


def test_add_student_success_and_capacity_and_duplicates():
    c = Course("Tiny", "Small class", max_capacity=1)
    s1 = Student("Alice", "a@example.com")
    s2 = Student("Bob", "b@example.com")

    # first enroll should succeed
    assert c.add_student(s1) is True
    assert s1 in c.students

    # duplicate enroll should be rejected
    assert c.add_student(s1) is False

    # capacity full -> next student rejected
    assert c.add_student(s2) is False
    assert s2 not in c.students


def test_remove_student_and_unenroll():
    c = Course("History", "Desc")
    s = Student("Carl", "c@example.com")

    # remove non-enrolled student should return False
    assert c.remove_student(s) is False

    # add and then remove
    assert c.add_student(s) is True
    assert c.remove_student(s) is True
    assert s not in c.students

    # Student.unenroll mirrors course removal
    c.add_student(s)
    # attach course record to student as a normal flow
    s.enrolled_courses.append(c)
    assert s.unenroll(c) is True
    assert c not in s.enrolled_courses


def test_student_enroll_and_complete_course_moves_records():
    c = Course("Physics", "Desc")
    s = Student("Dana", "d@example.com")

    # enroll via student helper; should update both sides
    assert s.enroll(c) is True
    assert c in s.enrolled_courses
    assert s in c.students

    # completing the course should move course to completed lists
    assert s.complete_course(c) is True
    assert c in s.completed_courses
    assert s in c.completed_students
    assert c not in s.enrolled_courses
    assert s not in c.students


def test_instructor_assignment_methods():
    c = Course("Biology", "Desc")
    instr = Instructor("Prof X", "x@example.com", expertise=["bio"])

    # assign via course
    assert c.assign_instructor(instr) is True
    assert c.instructor is instr

    # assign via instructor helper should also record course in instructor.courses
    instr2 = Instructor("Prof Y", "y@example.com", expertise="biology")
    assert instr2.assign_to_course(c) is True
    assert c in instr2.courses
    # course.instructor should now be instr2 (reassigned)
    assert c.instructor is instr2
