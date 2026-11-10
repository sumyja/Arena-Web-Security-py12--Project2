"""
student.py - Student Model Class
Defines the Student class representing individual student data, marks calculation,
grade determination, and pass/fail status evaluation.
"""

class Student:
    """
    Represents a student in the coaching center.
    
    Attributes:
        student_id (str): Unique identifier for the student (e.g., 'S101').
        name (str): Full name of the student.
        marks (dict): Dictionary mapping subject names to marks (float/int).
    """

    DEFAULT_SUBJECTS = ["Mathematics", "Science", "English", "Social Studies", "Computer"]
    PASSING_MARK_PER_SUBJECT = 40.0
    PASSING_PERCENTAGE = 40.0

    def __init__(self, student_id: str, name: str, marks: dict):
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.marks = {subject: float(score) for subject, score in marks.items()}

    def calculate_total(self) -> float:
        """Calculates and returns the sum of marks across all subjects."""
        return round(sum(self.marks.values()), 2)

    def calculate_average(self) -> float:
        """Calculates and returns the average marks per subject."""
        if not self.marks:
            return 0.0
        return round(self.calculate_total() / len(self.marks), 2)

    def calculate_percentage(self) -> float:
        """
        Calculates percentage assuming each subject is out of 100.
        Maximum possible marks = len(self.marks) * 100.
        """
        if not self.marks:
            return 0.0
        max_marks = len(self.marks) * 100.0
        return round((self.calculate_total() / max_marks) * 100.0, 2)

    def calculate_grade(self) -> str:
        """
        Determines the letter grade based on the percentage scored.
        Grading Criteria:
            90% - 100% : A+ (Outstanding)
            80% - 89.9%: A  (Excellent)
            70% - 79.9%: B  (Very Good)
            60% - 69.9%: C  (Good)
            50% - 59.9%: D  (Pass)
            Below 50%  : F  (Fail)
        """
        percentage = self.calculate_percentage()
        if percentage >= 90.0:
            return "A+"
        elif percentage >= 80.0:
            return "A"
        elif percentage >= 70.0:
            return "B"
        elif percentage >= 60.0:
            return "C"
        elif percentage >= 50.0:
            return "D"
        else:
            return "F"

    def determine_status(self) -> tuple[str, list[str]]:
        """
        Determines pass/fail status using conditional logic.
        Rule: Student must score >= 40 in EVERY subject AND >= 40% overall.
        Returns:
            tuple: (status: "Pass" | "Fail", failed_subjects: list[str])
        """
        failed_subjects = [
            subject for subject, score in self.marks.items()
            if score < self.PASSING_MARK_PER_SUBJECT
        ]
        
        overall_pass = self.calculate_percentage() >= self.PASSING_PERCENTAGE
        
        if not failed_subjects and overall_pass:
            return "Pass", []
        else:
            return "Fail", failed_subjects

    def get_status(self) -> str:
        """Convenience method returning 'Pass' or 'Fail'."""
        status, _ = self.determine_status()
        return status

    def to_dict(self) -> dict:
        """Converts student attributes into a dictionary for storage."""
        data = {
            "student_id": self.student_id,
            "name": self.name,
            **self.marks
        }
        return data

    @classmethod
    def from_dict(cls, data: dict, subjects: list = None):
        """Creates a Student instance from a dictionary."""
        subjects = subjects or cls.DEFAULT_SUBJECTS
        student_id = str(data.get("student_id", "")).strip()
        name = str(data.get("name", "")).strip()
        marks = {}
        for subj in subjects:
            marks[subj] = float(data.get(subj, 0.0))
        return cls(student_id=student_id, name=name, marks=marks)

    def display_report_card(self) -> str:
        """Generates a detailed formatted report card for the student."""
        status, failed_subjs = self.determine_status()
        lines = [
            "=" * 55,
            f"          STUDENT PERFORMANCE REPORT CARD",
            "=" * 55,
            f" Student ID : {self.student_id:<15} Name : {self.name}",
            "-" * 55,
            f" {'Subject':<25} {'Max Marks':<12} {'Obtained':<10}",
            "-" * 55
        ]
        for subj, mark in self.marks.items():
            lines.append(f" {subj:<25} {'100':<12} {mark:<10.1f}")
        lines.append("-" * 55)
        lines.append(f" Total Marks : {self.calculate_total():.1f} / {len(self.marks) * 100}")
        lines.append(f" Average     : {self.calculate_average():.2f}")
        lines.append(f" Percentage  : {self.calculate_percentage():.2f}%")
        lines.append(f" Grade       : {self.calculate_grade()}")
        lines.append(f" Status      : {status}")
        if failed_subjs:
            lines.append(f" Remark      : Needs improvement in: {', '.join(failed_subjs)}")
        else:
            lines.append(f" Remark      : Passed successfully!")
        lines.append("=" * 55)
        return "\n".join(lines)

    def __str__(self) -> str:
        return (f"Student(ID={self.student_id}, Name='{self.name}', "
                f"Total={self.calculate_total()}, Avg={self.calculate_average()}, "
                f"Grade={self.calculate_grade()}, Status={self.get_status()})")
