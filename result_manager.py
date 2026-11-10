"""
result_manager.py - Result Manager Class
Manages student records, class performance analytics, search operations,
and CSV data persistence for the coaching center application.
"""

import csv
import os
from student import Student


class ResultManager:
    """
    Manages student result records and overall class performance calculations.
    
    Attributes:
        data_file (str): Path to the CSV file used for persistent storage.
        students (dict): Mapping of student_id -> Student instance.
    """

    def __init__(self, data_file: str = "students_data.csv"):
        self.data_file = data_file
        self.students = {}  # {student_id: Student}
        self.load_from_csv()

    def add_student(self, student: Student) -> bool:
        """
        Adds a new student to the system.
        
        Args:
            student (Student): Student object to add.
            
        Returns:
            bool: True if successfully added, False if student_id already exists.
        """
        if student.student_id in self.students:
            return False
        self.students[student.student_id] = student
        self.save_to_csv()
        return True

    def search_student(self, student_id: str) -> Student | None:
        """
        Searches for a student by their ID (case-insensitive strip).
        
        Args:
            student_id (str): The ID to search.
            
        Returns:
            Student | None: The Student object if found, otherwise None.
        """
        target_id = str(student_id).strip().upper()
        for sid, student in self.students.items():
            if sid.upper() == target_id:
                return student
        return None

    def update_student(self, student_id: str, new_marks: dict) -> bool:
        """
        Updates marks for an existing student and saves changes.
        """
        student = self.search_student(student_id)
        if not student:
            return False
        for subj, mark in new_marks.items():
            student.marks[subj] = float(mark)
        self.save_to_csv()
        return True

    def delete_student(self, student_id: str) -> bool:
        """
        Deletes a student record by ID and saves changes.
        """
        student = self.search_student(student_id)
        if not student:
            return False
        del self.students[student.student_id]
        self.save_to_csv()
        return True

    def get_all_students(self) -> list[Student]:
        """Returns a list of all enrolled students."""
        return list(self.students.values())

    def get_highest_scoring_student(self) -> Student | None:
        """
        Finds and returns the student with the highest total marks.
        """
        if not self.students:
            return None
        return max(self.students.values(), key=lambda s: s.calculate_total())

    def get_lowest_scoring_student(self) -> Student | None:
        """
        Finds and returns the student with the lowest total marks.
        """
        if not self.students:
            return None
        return min(self.students.values(), key=lambda s: s.calculate_total())

    def generate_class_summary(self) -> dict:
        """
        Generates comprehensive performance statistics for the coaching center.
        
        Returns:
            dict containing:
                - total_students: int
                - pass_count: int
                - fail_count: int
                - pass_percentage: float
                - fail_percentage: float
                - class_average_percentage: float
                - highest_student: Student | None
                - lowest_student: Student | None
                - subject_stats: dict of subject -> {avg, max, min}
                - grade_counts: dict of grade -> count
        """
        total = len(self.students)
        if total == 0:
            return {
                "total_students": 0,
                "pass_count": 0,
                "fail_count": 0,
                "pass_percentage": 0.0,
                "fail_percentage": 0.0,
                "class_average_percentage": 0.0,
                "highest_student": None,
                "lowest_student": None,
                "subject_stats": {},
                "grade_counts": {g: 0 for g in ["A+", "A", "B", "C", "D", "F"]}
            }

        students_list = list(self.students.values())
        
        # Pass/Fail counts
        pass_count = sum(1 for s in students_list if s.get_status() == "Pass")
        fail_count = total - pass_count
        pass_pct = round((pass_count / total) * 100.0, 2)
        fail_pct = round((fail_count / total) * 100.0, 2)
        
        # Class average percentage
        avg_percentage = round(sum(s.calculate_percentage() for s in students_list) / total, 2)
        
        # Top and bottom performers
        highest_student = self.get_highest_scoring_student()
        lowest_student = self.get_lowest_scoring_student()
        
        # Grade distribution
        grade_counts = {g: 0 for g in ["A+", "A", "B", "C", "D", "F"]}
        for s in students_list:
            grade = s.calculate_grade()
            if grade in grade_counts:
                grade_counts[grade] += 1

        # Subject-wise statistics
        subject_stats = {}
        for subject in Student.DEFAULT_SUBJECTS:
            scores = [s.marks.get(subject, 0.0) for s in students_list if subject in s.marks]
            if scores:
                subject_stats[subject] = {
                    "average": round(sum(scores) / len(scores), 2),
                    "highest": round(max(scores), 2),
                    "lowest": round(min(scores), 2)
                }

        return {
            "total_students": total,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "pass_percentage": pass_pct,
            "fail_percentage": fail_pct,
            "class_average_percentage": avg_percentage,
            "highest_student": highest_student,
            "lowest_student": lowest_student,
            "subject_stats": subject_stats,
            "grade_counts": grade_counts
        }

    def save_to_csv(self, filename: str = None) -> bool:
        """
        Saves all student records to a CSV file.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        filepath = filename or self.data_file
        fieldnames = ["student_id", "name"] + Student.DEFAULT_SUBJECTS
        try:
            with open(filepath, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students.values():
                    writer.writerow(student.to_dict())
            return True
        except (IOError, OSError) as e:
            print(f"[Error] Failed to save data to CSV: {e}")
            return False

    def load_from_csv(self, filename: str = None) -> int:
        """
        Loads student records from a CSV file if it exists.
        
        Returns:
            int: Number of records successfully loaded.
        """
        filepath = filename or self.data_file
        if not os.path.exists(filepath):
            return 0

        loaded_count = 0
        try:
            with open(filepath, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # Extract and parse student record
                        student = Student.from_dict(row, subjects=Student.DEFAULT_SUBJECTS)
                        if student.student_id:
                            self.students[student.student_id] = student
                            loaded_count += 1
                    except (ValueError, KeyError) as parse_err:
                        print(f"[Warning] Skipping malformed row {row}: {parse_err}")
            return loaded_count
        except (IOError, OSError) as e:
            print(f"[Error] Failed to read CSV file '{filepath}': {e}")
            return 0
