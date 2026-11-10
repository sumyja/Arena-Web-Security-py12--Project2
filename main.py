"""
main.py - Coaching Center Student Result Management System
Terminal-based, menu-driven interface using loops, functions, and OOP classes.
"""

import sys
import os
from student import Student
from result_manager import ResultManager


def print_header(title: str):
    """Prints a styled section header."""
    print("\n" + "=" * 65)
    print(f" {title.upper()} ".center(65, "="))
    print("=" * 65)


def get_valid_string(prompt: str, allow_empty: bool = False) -> str:
    """Prompts user for non-empty text input."""
    while True:
        val = input(prompt).strip()
        if not val and not allow_empty:
            print("  [!] Error: Input cannot be blank. Please try again.")
            continue
        return val


def get_valid_mark(subject_name: str) -> float:
    """
    Prompts user for a mark between 0 and 100 with comprehensive validation.
    """
    while True:
        raw_val = input(f"  Enter mark for {subject_name} (0 - 100): ").strip()
        try:
            score = float(raw_val)
            if 0.0 <= score <= 100.0:
                return score
            else:
                print(f"  [!] Invalid range: Mark must be between 0 and 100. You entered '{raw_val}'.")
        except ValueError:
            print(f"  [!] Invalid input: '{raw_val}' is not a valid number. Please enter a numeric mark.")


def add_student_view(manager: ResultManager):
    """Handles user input to create and add a new Student."""
    print_header("Add New Student")
    
    # 1. Get unique student ID
    while True:
        student_id = get_valid_string("  Enter Student ID (e.g., S101, 1001): ")
        if manager.search_student(student_id):
            print(f"  [!] Error: Student ID '{student_id}' already exists! Please use a unique ID.")
            continue
        break

    # 2. Get student Name
    name = get_valid_string("  Enter Student Name: ")

    # 3. Get marks for the five standard subjects
    print(f"\n  Enter marks for {len(Student.DEFAULT_SUBJECTS)} subjects (Max: 100 per subject):")
    marks = {}
    for subject in Student.DEFAULT_SUBJECTS:
        marks[subject] = get_valid_mark(subject)

    # 4. Create Student instance and add to manager
    new_student = Student(student_id=student_id, name=name, marks=marks)
    success = manager.add_student(new_student)

    if success:
        print(f"\n  [SUCCESS] Student '{name}' (ID: {student_id}) was added successfully!")
        print(f"  Calculated Total : {new_student.calculate_total():.1f} / 500")
        print(f"  Percentage       : {new_student.calculate_percentage():.2f}%")
        print(f"  Grade            : {new_student.calculate_grade()}")
        print(f"  Status           : {new_student.get_status()}")
    else:
        print("  [!] Failed to add student. A record with this ID already exists.")


def display_all_students_view(manager: ResultManager):
    """Displays all enrolled students in a formatted tabular layout."""
    print_header("All Enrolled Student Records")
    students = manager.get_all_students()

    if not students:
        print("  No student records found in the system.")
        print("  Use Option 1 from the main menu to add students.")
        return

    # Print table header
    print(f" {'ID':<8} {'Name':<18} {'Tot/500':<9} {'Avg':<7} {'%':<7} {'Grade':<6} {'Status':<6}")
    print("-" * 65)

    for s in students:
        total = s.calculate_total()
        avg = s.calculate_average()
        pct = s.calculate_percentage()
        grade = s.calculate_grade()
        status = s.get_status()
        print(f" {s.student_id:<8} {s.name[:17]:<18} {total:<9.1f} {avg:<7.1f} {pct:<7.1f} {grade:<6} {status:<6}")

    print("-" * 65)
    print(f" Total records displayed: {len(students)}")


def search_student_view(manager: ResultManager):
    """Searches and displays individual student performance report card."""
    print_header("Search Student by ID")
    students = manager.get_all_students()
    if not students:
        print("  No student records available to search.")
        return

    student_id = get_valid_string("  Enter Student ID to search: ")
    student = manager.search_student(student_id)

    if student:
        print("\n" + student.display_report_card())
    else:
        print(f"\n  [!] No student found with ID '{student_id}'.")


def view_toppers_and_lowest_view(manager: ResultManager):
    """Displays highest-scoring and lowest-scoring students."""
    print_header("Highest and Lowest Scoring Students")
    students = manager.get_all_students()
    if not students:
        print("  No student records found. Add students first.")
        return

    highest = manager.get_highest_scoring_student()
    lowest = manager.get_lowest_scoring_student()

    print("\n  >>> HIGHEST-SCORING STUDENT (TOPPER) <<<")
    print(f"  ID         : {highest.student_id}")
    print(f"  Name       : {highest.name}")
    print(f"  Total Marks: {highest.calculate_total():.1f} / 500")
    print(f"  Percentage : {highest.calculate_percentage():.2f}%")
    print(f"  Grade      : {highest.calculate_grade()}")
    print(f"  Status     : {highest.get_status()}")

    print("\n  >>> LOWEST-SCORING STUDENT <<<")
    print(f"  ID         : {lowest.student_id}")
    print(f"  Name       : {lowest.name}")
    print(f"  Total Marks: {lowest.calculate_total():.1f} / 500")
    print(f"  Percentage : {lowest.calculate_percentage():.2f}%")
    print(f"  Grade      : {lowest.calculate_grade()}")
    print(f"  Status     : {lowest.get_status()}")


def class_summary_view(manager: ResultManager):
    """Displays comprehensive class performance report."""
    print_header("Class Performance Summary")
    summary = manager.generate_class_summary()

    if summary["total_students"] == 0:
        print("  No student records available to calculate class summary.")
        return

    print(f"  Total Enrolled Students : {summary['total_students']}")
    print(f"  Passed Students         : {summary['pass_count']} ({summary['pass_percentage']}%)")
    print(f"  Failed Students         : {summary['fail_count']} ({summary['fail_percentage']}%)")
    print(f"  Class Average Score     : {summary['class_average_percentage']}%")

    if summary["highest_student"]:
        print(f"  Highest Scorer          : {summary['highest_student'].name} ({summary['highest_student'].calculate_percentage():.1f}%)")
    if summary["lowest_student"]:
        print(f"  Lowest Scorer           : {summary['lowest_student'].name} ({summary['lowest_student'].calculate_percentage():.1f}%)")

    print("\n  --- Grade Distribution ---")
    for grade, count in summary["grade_counts"].items():
        bar = "#" * count
        print(f"    Grade {grade:<3}: {count:<3} {bar}")

    print("\n  --- Subject-wise Performance ---")
    print(f"  {'Subject':<18} {'Average':<10} {'Highest':<10} {'Lowest':<10}")
    print("  " + "-" * 48)
    for subj, stats in summary["subject_stats"].items():
        print(f"  {subj:<18} {stats['average']:<10.1f} {stats['highest']:<10.1f} {stats['lowest']:<10.1f}")


def update_student_view(manager: ResultManager):
    """Allows updating marks of an existing student."""
    print_header("Update Student Marks")
    student_id = get_valid_string("  Enter Student ID to update: ")
    student = manager.search_student(student_id)

    if not student:
        print(f"  [!] No student found with ID '{student_id}'.")
        return

    print(f"  Updating marks for {student.name} (ID: {student.student_id})")
    print("  Press Enter to keep the existing mark, or type a new mark (0-100):")
    updated_marks = {}
    for subj in Student.DEFAULT_SUBJECTS:
        current_mark = student.marks.get(subj, 0.0)
        while True:
            raw = input(f"  {subj} [Current: {current_mark}]: ").strip()
            if raw == "":
                updated_marks[subj] = current_mark
                break
            try:
                val = float(raw)
                if 0.0 <= val <= 100.0:
                    updated_marks[subj] = val
                    break
                else:
                    print("  [!] Mark must be between 0 and 100.")
            except ValueError:
                print("  [!] Please enter a valid number.")

    manager.update_student(student_id, updated_marks)
    print(f"\n  [SUCCESS] Marks updated for '{student.name}'. Changes saved to CSV.")


def delete_student_view(manager: ResultManager):
    """Deletes a student record with confirmation."""
    print_header("Delete Student Record")
    student_id = get_valid_string("  Enter Student ID to delete: ")
    student = manager.search_student(student_id)

    if not student:
        print(f"  [!] No student found with ID '{student_id}'.")
        return

    confirm = get_valid_string(f"  Are you sure you want to delete {student.name} (ID: {student.student_id})? (y/n): ")
    if confirm.lower() in ["y", "yes"]:
        manager.delete_student(student_id)
        print(f"  [SUCCESS] Student '{student.name}' was deleted.")
    else:
        print("  [CANCELLED] Deletion was cancelled.")


def save_csv_view(manager: ResultManager):
    """Explicitly saves data to CSV."""
    print_header("Save Data to CSV")
    filename = input(f"  Enter filename (press Enter for default '{manager.data_file}'): ").strip()
    target_file = filename if filename else manager.data_file
    if manager.save_to_csv(target_file):
        print(f"  [SUCCESS] All records successfully saved to '{target_file}'.")
    else:
        print(f"  [!] Failed to save records to '{target_file}'.")


def load_csv_view(manager: ResultManager):
    """Loads or reloads data from a CSV file."""
    print_header("Load Data from CSV")
    filename = input(f"  Enter filename (press Enter for default '{manager.data_file}'): ").strip()
    target_file = filename if filename else manager.data_file
    count = manager.load_from_csv(target_file)
    print(f"  [SUCCESS] Loaded {count} student records from '{target_file}'.")


def display_menu():
    """Prints the main interactive menu."""
    print("\n" + "=" * 65)
    print("       COACHING CENTER - STUDENT RESULT MANAGEMENT SYSTEM       ")
    print("=" * 65)
    print("  [1] Add New Student Record")
    print("  [2] View All Student Records (Tabular List)")
    print("  [3] Search Student by ID (Detailed Report Card)")
    print("  [4] View Highest and Lowest Scoring Students")
    print("  [5] Generate Class Performance Summary")
    print("  [6] Update Student Marks")
    print("  [7] Delete Student Record")
    print("  [8] Save Records to CSV (Bonus Challenge)")
    print("  [9] Reload Records from CSV")
    print("  [0] Exit Application")
    print("=" * 65)


def main():
    """Main program entry loop."""
    manager = ResultManager("students_data.csv")
    print("\n" + "*" * 65)
    print("  Welcome to Coaching Center Student Result Management System")
    print(f"  Loaded {len(manager.students)} existing student record(s) on startup.")
    print("*" * 65)

    while True:
        display_menu()
        choice = input("  Select an option (0-9): ").strip()

        if choice == "1":
            add_student_view(manager)
        elif choice == "2":
            display_all_students_view(manager)
        elif choice == "3":
            search_student_view(manager)
        elif choice == "4":
            view_toppers_and_lowest_view(manager)
        elif choice == "5":
            class_summary_view(manager)
        elif choice == "6":
            update_student_view(manager)
        elif choice == "7":
            delete_student_view(manager)
        elif choice == "8":
            save_csv_view(manager)
        elif choice == "9":
            load_csv_view(manager)
        elif choice == "0":
            # Auto-save before quitting
            manager.save_to_csv()
            print("\n  [INFO] Student records saved to CSV.")
            print("  Thank you for using the Coaching Center System. Goodbye!\n")
            sys.exit(0)
        else:
            print(f"  [!] Invalid choice '{choice}'. Please enter a number between 0 and 9.")


if __name__ == "__main__":
    main()
