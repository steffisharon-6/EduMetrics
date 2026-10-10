# Project Documentation: EduMetrics

## 1. Project Title and Student Details
- **Project Title:** EduMetrics: Student Performance Analytics System
- **Student Name:** [Your Name]
- **Student ID:** [Your ID]

## 2. Objective
The objective of this project is to build an interactive dashboard using Python, Pandas, NumPy, and Streamlit to analyze student performance, grades, and attendance data based on real-world constraints.

## 3. Technologies Used
- Python 3.11+
- Streamlit (Web framework)
- Pandas (Data manipulation and analysis)
- NumPy (Numerical computations)
- Plotly Express (Interactive charts)
- Pytest (Unit testing)

## 4. Dataset Description
The dataset is a CSV file comprising student academic records. It contains 63 anonymized student records migrated from the internal assessment workbook (`II_INTERNAL_MARK_III_Yr_CSBS_EVEN_25_26.xlsx`). To protect privacy, all student names have been replaced with unique fictional names, while all academic marks and identifiers remain completely authentic. The columns are:
- Student_ID (String, e.g., Register Number)
- Name (String, Anonymized)
- Department (String, CSBS)
- 23CB1601-CC (Marks: 0-100)
- 23CB1602-HRM (Marks: 0-100)
- 23CS1501-FSD (Marks: 0-100)
- 23CS1503-AIML (Marks: 0-100)
- 23CS1602-CD (Marks: 0-100, handles 'AB' as missing)
- 23AD1918-BA/23IT1909-EH (Marks: 0-100)

## 5. Implementation
The project consists of:
- `functions.py`: Contains modular logic for data validation, grading, calculations (total, average), and descriptive statistics.
- `main.py`: The Streamlit dashboard acting as the presentation layer. It manages page state, rendering of UI elements, and interactions.
- `test_functions.py`: Pytest suite to validate logic boundaries and edge cases.

## 6. Key Features
- **Data Validation:** Strict checks on uploaded CSV files for correct columns, numeric boundaries, and missing values.
- **Dynamic Dashboard:** Real-time updates based on active filters (Department, Grade, Pass/Fail).
- **Interactive Visualizations:** Subject performance, grade distributions, and attendance insights using Plotly.
- **Export System:** Ability to download filtered records and aggregated reports as CSV.

## 7. Output Screenshots
Screenshots of the working dashboard can be found in the `screenshots/` directory, illustrating the Overview page, Student Records, and Performance Analytics.

## 8. Final Outcome
A complete, functioning web application running on Streamlit that effectively visualizes student performance data in a modern, user-friendly interface using a futuristic Orbital Intelligence design theme.

## 9. Challenges and Learning
- **Challenge:** Handling real-world datasets with missing or textual data (e.g., 'AB' for absent) without breaking numeric calculations.
- **Learning:** Migrating from fictional sample datasets to real production data, using `pd.to_numeric(errors='coerce')` to gracefully handle 'AB', and replacing strict Python iterators with NaN-safe aggregations (`np.nanmean`, `np.nansum`).
- **Learning:** Creating a consistent design system (Orbital Intelligence) using Streamlit's custom CSS injection.

## 10. GitHub Repository Link
[Placeholder: Link to your GitHub Repository]
