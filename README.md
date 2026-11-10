# Coaching Center - Student Result Management System

A Python terminal-based application designed for coaching centers and academic institutions to manage student marks, compute academic statistics, and generate automated performance reports.

Built with **Object-Oriented Programming (OOP)**, robust input validation, conditional logic, and persistent CSV storage (Bonus Challenge).

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Grading System & Evaluation Criteria](#grading-system--evaluation-criteria)
- [Project Architecture & File Structure](#project-architecture--file-structure)
- [Prerequisites & Installation](#prerequisites--installation)
- [How to Run the Application](#how-to-run-the-application)
- [Running Automated Unit Tests](#running-automated-unit-tests)
- [Application Output Demonstrations](#application-output-demonstrations)


---

## Project Overview

Coaching centers often face challenges manually managing student marks across multiple subjects, calculating totals, averages, grades, and identifying students who need additional academic assistance.

This application provides a **menu-driven terminal solution** that:
1. Manages student records across **5 core subjects** (Mathematics, Science, English, Social Studies, Computer).
2. Computes total marks, averages, percentages, and letter grades.
3. Applies conditional logic to evaluate pass/fail standing (requiring passing marks in every subject).
4. Enables instant student searches by unique ID with formatted report card generation.
5. Identifies highest-scoring and lowest-scoring students.
6. Aggregates class-wide statistics: pass rates, subject-wise performance, and grade distributions.
7. Preserves records in a persistent CSV file (`students_data.csv`).

---

## Key Features

- **Object-Oriented Design (OOP)**: Clear separation of concerns using `Student` (entity/model) and `ResultManager` (business logic and data repository).
- **5-Subject Marks Tracking**: Supports individual subject scores out of 100 with strict numeric validation (0 – 100).
- **Multi-Factor Pass/Fail Logic**:
  - Requires **$\ge 40.0$** marks in each individual subject.
  - Requires **$\ge 40.0\%$** overall aggregate score.
  - Flags specific failed subjects if a student fails.
- **Search by Student ID**: Instant case-insensitive ID lookup generating a printable report card.
- **Top & Lowest Scorer Identification**: Direct queries to display toppers and students needing extra coaching.
- **Class Performance Summary**: Complete institutional analytics including pass rate, class average score, grade distribution histogram, and subject-wise averages, minimums, and maximums.
- **Bonus Challenge - CSV Persistence**: Automatic loading on startup and saving on modification, plus manual export/import options.
- **Resilient Error Handling (15% Rubric)**:
  - Prevents duplicate Student IDs.
  - Rejects empty strings, negative marks, and values $> 100$.
  - Handles corrupted CSV rows gracefully without crashing.
  - Prevents division-by-zero errors when no student records exist.

---

## Grading System & Evaluation Criteria

### Letter Grades
| Percentage Range | Grade | Description |
|---|---|---|
| **90.0% – 100.0%** | **A+** | Outstanding |
| **80.0% – 89.9%** | **A** | Excellent |
| **70.0% – 79.9%** | **B** | Very Good |
| **60.0% – 69.9%** | **C** | Good / Average |
| **50.0% – 59.9%** | **D** | Below Average |
| **Below 50.0%** | **F** | Fail |

### Pass / Fail Conditional Logic
A student is awarded **"Pass"** status **only if**:
1. Marks in **every** individual subject are $\ge 40$.
2. The overall percentage is $\ge 40.0\%$.

If a student scores below 40 in any subject, the status is marked **"Fail"**, and the report card specifies the exact subject(s) requiring improvement.

---

## Project Architecture & File Structure

```
project2/
│
├── student.py                   # Student class (model, calculations, grade & pass/fail logic)
├── result_manager.py           # ResultManager class (data collection, analytics, CSV I/O)
├── main.py                     # Menu-driven CLI interface with input loops & functions
├── test_system.py              # Automated unittest test suite (13 comprehensive test cases)
├── students_data.csv           # Persistent CSV file storing student records
├── .gitignore                  # Ignores Python bytecode cache (__pycache__)
└── README.md                   # Complete documentation and evaluation guide
```

---

## Prerequisites & Installation

### 1. Prerequisites
- **Python 3.10+** (tested on Python 3.14).
- Uses only built-in standard Python libraries (`csv`, `os`, `sys`). No external `pip` installations needed to run the project.

### 2. Setup
Navigate to the project folder:
```bash
cd "aws-pyhw/Projects/project2"
```

---

## How to Run the Application

Launch the interactive terminal application:

```bash
python main.py
```

---

## Running Automated Unit Tests

A comprehensive unit test suite is included in `test_system.py` to verify all formulas, conditional logic, and edge cases:

```bash
python test_system.py
```

**Output:**
```
.............
----------------------------------------------------------------------
Ran 13 tests in 0.014s

OK
```

The test suite validates:
- Total, average, and percentage calculations.
- Letter grade boundary evaluations ($A+$, $A$, $B$, $C$, $D$, $F$).
- Pass/Fail conditional logic with single-subject failure detection.
- Prevention of duplicate student IDs.
- Highest and lowest scorer retrieval.
- Class summary calculations on populated and empty datasets.
- CSV saving and reloading consistency.

---

## Application Output Demonstrations

### 1. Main Menu Interface
```text
*****************************************************************
  Welcome to Coaching Center Student Result Management System
  Loaded 5 existing student record(s) on startup.
*****************************************************************

=================================================================
       COACHING CENTER - STUDENT RESULT MANAGEMENT SYSTEM        
=================================================================
  [1] Add New Student Record
  [2] View All Student Records (Tabular List)
  [3] Search Student by ID (Detailed Report Card)
  [4] View Highest and Lowest Scoring Students
  [5] Generate Class Performance Summary
  [6] Update Student Marks
  [7] Delete Student Record
  [8] Save Records to CSV (Bonus Challenge)
  [9] Reload Records from CSV
  [0] Exit Application
=================================================================
  Select an option (0-9): 
```

### 2. Adding a New Student Record
```text
=================================================================
                        ADD NEW STUDENT                          
=================================================================
  Enter Student ID (e.g., S101, 1001): S106
  Enter Student Name: Emily Watson

  Enter marks for 5 subjects (Max: 100 per subject):
  Enter mark for Mathematics (0 - 100): 88.0
  Enter mark for Science (0 - 100): 91.5
  Enter mark for English (0 - 100): 84.0
  Enter mark for Social Studies (0 - 100): 79.0
  Enter mark for Computer (0 - 100): 94.5

  [SUCCESS] Student 'Emily Watson' (ID: S106) was added successfully!
  Calculated Total : 437.0 / 500
  Percentage       : 87.40%
  Grade            : A
  Status           : Pass
```

### 3. Tabular View of All Enrolled Students
```text
=================================================================
                  ALL ENROLLED STUDENT RECORDS                   
=================================================================
 ID       Name               Tot/500   Avg     %       Grade  Status
-----------------------------------------------------------------
 S101     Chadni             461.0     92.2    92.2    A+     Pass  
 S102     Ankit              400.0     80.0    80.0    A      Pass  
 S103     Sifat              339.0     67.8    67.8    C      Pass  
 S104     David              269.0     53.8    53.8    D      Pass  
 S105     John               225.0     45.0    45.0    F      Fail  
-----------------------------------------------------------------
 Total records displayed: 5
```

### 4. Search by ID & Performance Report Card
```text
=================================================================
                      SEARCH STUDENT BY ID                       
=================================================================
  Enter Student ID to search: S101

=======================================================
          STUDENT PERFORMANCE REPORT CARD
=======================================================
 Student ID : S101            Name : Chadni
-------------------------------------------------------
 Subject                   Max Marks    Obtained  
-------------------------------------------------------
 Mathematics               100          92.0      
 Science                   100          95.0      
 English                   100          88.0      
 Social Studies            100          90.0      
 Computer                  100          96.0      
-------------------------------------------------------
 Total Marks : 461.0 / 500
 Average     : 92.20
 Percentage  : 92.20%
 Grade       : A+
 Status      : Pass
 Remark      : Passed successfully!
=======================================================
```

### 5. Highest and Lowest Scoring Students
```text
=================================================================
               HIGHEST AND LOWEST SCORING STUDENTS               
=================================================================

  >>> HIGHEST-SCORING STUDENT (TOPPER) <<<
  ID         : S101
  Name       : Chadni
  Total Marks: 461.0 / 500
  Percentage : 92.20%
  Grade      : A+
  Status     : Pass

  >>> LOWEST-SCORING STUDENT <<<
  ID         : S105
  Name       : John
  Total Marks: 225.0 / 500
  Percentage : 45.00%
  Grade      : F
  Status     : Fail
```

### 6. Class Performance Summary
```text
=================================================================
                    CLASS PERFORMANCE SUMMARY                    
=================================================================
  Total Enrolled Students : 5
  Passed Students         : 4 (80.0%)
  Failed Students         : 1 (20.0%)
  Class Average Score     : 67.76%
  Highest Scorer          : Chadni (92.2%)
  Lowest Scorer           : John (45.0%)

  --- Grade Distribution ---
    Grade A+ : 1   #
    Grade A  : 1   #
    Grade B  : 0   
    Grade C  : 1   #
    Grade D  : 1   #
    Grade F  : 1   #

  --- Subject-wise Performance ---
  Subject            Average    Highest    Lowest    
  ------------------------------------------------
  Mathematics        63.8       92.0       32.0      
  Science            72.4       95.0       55.0      
  English            65.2       88.0       45.0      
  Social Studies     65.6       90.0       38.0      
  Computer           71.8       96.0       50.0      
```

---

