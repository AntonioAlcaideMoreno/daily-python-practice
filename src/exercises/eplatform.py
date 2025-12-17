"""Simple e-learning platform domain objects: Course, Student, Instructor.

The module provides small, easy-to-read implementations intended for
exercise use. Each class includes a concise docstring and methods contain
clear, standardized docstrings/comments so other developers can quickly
understand the responsibilities and return values.
"""

from typing import List, Optional


class Course:
    """Represents a single course.

    Attributes:
        title (str): Human-readable course title
        description (str): Short course description
        max_capacity (int): Maximum number of enrolled students
        instructor (Optional[Instructor]): Assigned instructor or None
        students (List[Student]): Students currently enrolled
        completed_students (List[Student]): Students who completed the course
    """

    def __init__(self, title: str, description: str, max_capacity: int = 30):
        # Basic attributes describing the course and its state
        self.title = title
        self.description = description
        self.max_capacity = max_capacity
        self.instructor: Optional["Instructor"] = None
        self.students: List["Student"] = []
        self.completed_students: List["Student"] = []

    def add_student(self, student: "Student") -> bool:
        """Enroll `student` in the course.

        Returns:
            bool: True if student was added, False otherwise (full or already enrolled)
        """
        # Prevent adding when full or when student is already present
        if len(self.students) >= self.max_capacity or student in self.students:
            return False
        try:
            self.students.append(student)
            return True
        except Exception:
            # Defensive catch: return False in case of unexpected errors
            return False

    def remove_student(self, student: "Student") -> bool:
        """Remove `student` from the course if present.

        Returns:
            bool: True if removed successfully, False if student was not enrolled
        """
        if student not in self.students:
            return False
        try:
            self.students.remove(student)
            return True
        except Exception:
            return False

    def mark_completed(self, student: "Student") -> bool:
        """Mark `student` as completed: move from `students` to `completed_students`.

        Returns:
            bool: True if operation succeeded, False if student was not enrolled
        """
        if student not in self.students:
            return False
        try:
            self.students.remove(student)
            self.completed_students.append(student)
            return True
        except Exception:
            return False

    def assign_instructor(self, instructor: "Instructor") -> bool:
        """Assign an instructor to the course.

        Returns True to indicate success.
        """
        self.instructor = instructor
        return True


class Student:
    """Represents a student and their course relationships.

    Attributes:
        name (str): Student's full name
        email (str): Student's contact email
        enrolled_courses (List[Course]): Courses the student is currently enrolled in
        completed_courses (List[Course]): Courses the student has completed
    """

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.enrolled_courses: List[Course] = []
        self.completed_courses: List[Course] = []

    def enroll(self, course: Course) -> bool:
        """Attempt to enroll this student in `course`.

        Uses the `course.add_student(self)` call to ensure the course controls
        capacity and duplicate checks. On success, the course is also added to
        the student's `enrolled_courses` list.
        """
        if course in self.enrolled_courses:
            return False
        try:
            if course.add_student(self):
                self.enrolled_courses.append(course)
                return True
            return False
        except Exception:
            return False

    def unenroll(self, course: Course) -> bool:
        """Unenroll this student from `course`.

        Returns True if course removal succeeded and the student's records are
        updated; otherwise returns False.
        """
        if course not in self.enrolled_courses:
            return False
        try:
            if course.remove_student(self):
                self.enrolled_courses.remove(course)
                return True
            return False
        except Exception:
            return False

    def complete_course(self, course: Course) -> bool:
        """Mark `course` as completed for this student.

        This calls `course.mark_completed(self)` to let the course perform its
        own checks. On success the course is moved from `enrolled_courses` to
        `completed_courses`.
        """
        if course not in self.enrolled_courses:
            return False
        try:
            if course.mark_completed(self):
                # Keep student-local tracking in sync with course state
                self.enrolled_courses.remove(course)
                self.completed_courses.append(course)
                return True
            return False
        except Exception:
            return False


class Instructor:
    """Represents an instructor who can be assigned to teach courses."""

    def __init__(self, name: str, email: str, expertise):
        self.name = name
        self.email = email
        # Expertise may be a string or list; keep as-is for simplicity
        self.expertise = expertise
        self.courses: List[Course] = []

    def assign_to_course(self, course: Course) -> bool:
        """Assign this instructor to `course` and record it locally."""
        course.assign_instructor(self)
        self.courses.append(course)
        return True
