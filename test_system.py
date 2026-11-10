"""
test_system.py - Unit Tests for Coaching Center Student Result Management System
Tests Student class, ResultManager class, calculations, pass/fail rules, and CSV persistence.
"""

import unittest
import os
import tempfile
from student import Student
from result_manager import ResultManager


class TestStudentClass(unittest.TestCase):
    def setUp(self):
        self.marks_passing = {
            "Mathematics": 85.0,
            "Science": 90.0,
            "English": 75.0,
            "Social Studies": 80.0,
            "Computer": 95.0
        }
        self.student_pass = Student("S101", "Alice Wonder", self.marks_passing)

        self.marks_failing = {
            "Mathematics": 35.0,  # Below 40
            "Science": 80.0,
            "English": 70.0,
            "Social Studies": 65.0,
            "Computer": 75.0
        }
        self.student_fail = Student("S102", "Bob Builder", self.marks_failing)

    def test_total_calculation(self):
        # 85 + 90 + 75 + 80 + 95 = 425
        self.assertEqual(self.student_pass.calculate_total(), 425.0)

    def test_average_calculation(self):
        # 425 / 5 = 85.0
        self.assertEqual(self.student_pass.calculate_average(), 85.0)

    def test_percentage_calculation(self):
        # (425 / 500) * 100 = 85.0%
        self.assertEqual(self.student_pass.calculate_percentage(), 85.0)

    def test_grade_calculation(self):
        self.assertEqual(self.student_pass.calculate_grade(), "A")

        # Test A+ (>= 90)
        topper = Student("S999", "Top Student", {s: 95.0 for s in Student.DEFAULT_SUBJECTS})
        self.assertEqual(topper.calculate_grade(), "A+")

        # Test B (70 - 79.9)
        b_student = Student("S998", "B Student", {s: 72.0 for s in Student.DEFAULT_SUBJECTS})
        self.assertEqual(b_student.calculate_grade(), "B")

        # Test C (60 - 69.9)
        c_student = Student("S997", "C Student", {s: 65.0 for s in Student.DEFAULT_SUBJECTS})
        self.assertEqual(c_student.calculate_grade(), "C")

        # Test D (50 - 59.9)
        d_student = Student("S996", "D Student", {s: 52.0 for s in Student.DEFAULT_SUBJECTS})
        self.assertEqual(d_student.calculate_grade(), "D")

        # Test F (< 50)
        f_student = Student("S995", "F Student", {s: 35.0 for s in Student.DEFAULT_SUBJECTS})
        self.assertEqual(f_student.calculate_grade(), "F")

    def test_pass_fail_logic(self):
        # Alice passed all subjects with >= 40 and overall >= 40
        status, failed_subjs = self.student_pass.determine_status()
        self.assertEqual(status, "Pass")
        self.assertEqual(failed_subjs, [])
        self.assertEqual(self.student_pass.get_status(), "Pass")

        # Bob has overall 65.0% but Mathematics is 35 (< 40), so must fail
        status, failed_subjs = self.student_fail.determine_status()
        self.assertEqual(status, "Fail")
        self.assertIn("Mathematics", failed_subjs)
        self.assertEqual(self.student_fail.get_status(), "Fail")

    def test_report_card_output(self):
        report = self.student_pass.display_report_card()
        self.assertIn("Alice Wonder", report)
        self.assertIn("S101", report)
        self.assertIn("425.0", report)
        self.assertIn("Pass", report)


class TestResultManager(unittest.TestCase):
    def setUp(self):
        # Create a temp file for testing CSV persistence
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        self.temp_file.close()
        # Initialize ResultManager pointing to empty temp file
        self.manager = ResultManager(data_file=self.temp_file.name)
        # Clear any auto-loaded state
        self.manager.students = {}

        # Add 3 test students
        self.s1 = Student("T1", "Top Student", {"Mathematics": 90, "Science": 95, "English": 92, "Social Studies": 88, "Computer": 94})
        self.s2 = Student("T2", "Mid Student", {"Mathematics": 70, "Science": 72, "English": 68, "Social Studies": 75, "Computer": 71})
        self.s3 = Student("T3", "Low Student", {"Mathematics": 35, "Science": 42, "English": 40, "Social Studies": 45, "Computer": 38})
        self.manager.add_student(self.s1)
        self.manager.add_student(self.s2)
        self.manager.add_student(self.s3)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_add_duplicate_student_prevented(self):
        dup_student = Student("T1", "Duplicate Person", {"Mathematics": 50, "Science": 50, "English": 50, "Social Studies": 50, "Computer": 50})
        added = self.manager.add_student(dup_student)
        self.assertFalse(added)
        self.assertEqual(len(self.manager.students), 3)

    def test_search_student(self):
        # Case insensitive match
        found = self.manager.search_student("t1")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Top Student")

        not_found = self.manager.search_student("NONEXISTENT")
        self.assertIsNone(not_found)

    def test_highest_and_lowest_scoring_student(self):
        highest = self.manager.get_highest_scoring_student()
        lowest = self.manager.get_lowest_scoring_student()
        self.assertEqual(highest.student_id, "T1")
        self.assertEqual(lowest.student_id, "T3")

    def test_generate_class_summary(self):
        summary = self.manager.generate_class_summary()
        self.assertEqual(summary["total_students"], 3)
        # T1 and T2 pass, T3 fails (Math 35, Computer 38)
        self.assertEqual(summary["pass_count"], 2)
        self.assertEqual(summary["fail_count"], 1)
        self.assertAlmostEqual(summary["pass_percentage"], 66.67, delta=0.1)
        self.assertEqual(summary["highest_student"].student_id, "T1")
        self.assertEqual(summary["lowest_student"].student_id, "T3")
        self.assertIn("Mathematics", summary["subject_stats"])

    def test_empty_manager_summary(self):
        empty_manager = ResultManager(data_file=self.temp_file.name)
        empty_manager.students = {}
        summary = empty_manager.generate_class_summary()
        self.assertEqual(summary["total_students"], 0)
        self.assertIsNone(empty_manager.get_highest_scoring_student())
        self.assertIsNone(empty_manager.get_lowest_scoring_student())

    def test_csv_persistence(self):
        # Save records
        save_success = self.manager.save_to_csv()
        self.assertTrue(save_success)

        # Create new manager pointing to the same CSV file
        new_manager = ResultManager(data_file=self.temp_file.name)
        self.assertEqual(len(new_manager.students), 3)
        loaded_t1 = new_manager.search_student("T1")
        self.assertIsNotNone(loaded_t1)
        self.assertEqual(loaded_t1.calculate_total(), 459.0)

    def test_update_and_delete_student(self):
        # Update T2
        updated = self.manager.update_student("T2", {"Mathematics": 99.0})
        self.assertTrue(updated)
        self.assertEqual(self.manager.search_student("T2").marks["Mathematics"], 99.0)

        # Delete T3
        deleted = self.manager.delete_student("T3")
        self.assertTrue(deleted)
        self.assertIsNone(self.manager.search_student("T3"))
        self.assertEqual(len(self.manager.students), 2)


if __name__ == "__main__":
    unittest.main()
