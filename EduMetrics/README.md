# EduMetrics: Student Performance Analytics System

"Understand Performance. Discover Potential."

EduMetrics is a premium, interactive web dashboard built with Python and Streamlit to analyze student performance data.

## Features
- **Premium Welcome Dashboard**: An animated landing page introducing the platform before seamless entry.
- **Intelligent Routing**: Built-in state management preserving data while navigating between pages.
- Complete academic dataset analysis
- Grade and Pass/Fail calculations based on configurable rules
- Interactive data visualizations with Plotly
- Searchable and filterable student records
- Top performers and attendance insights
- Data validation for uploaded CSV files
- Export functionality for all reports

## Technologies
- Python 3.11+
- Streamlit
- Pandas
- NumPy
- Plotly Express

## Setup & Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run main.py
   ```
5. Run tests:
   ```bash
   pytest
   ```

## Dataset Requirements
The application accepts CSV files with the following columns:
- Student_ID
- Name
- Department
- 23CB1601-CC
- 23CB1602-HRM
- 23CS1501-FSD
- 23CS1503-AIML
- 23CS1602-CD
- 23AD1918-BA/23IT1909-EH

*Note: The dataset uses authentic academic records but all student names have been fully anonymized for privacy protection.*

Marks must be between 0 and 100.

## AI Student Avatars
The dashboard includes realistic, AI-generated fictional student portraits displayed in the Data Table and Individual Profiles. 
- Avatars are stored locally in the `assets/student_avatars/` directory.
- The system automatically maps each `Student_ID` to an avatar file consistently. 
- To add new avatars, simply save them as `avatar_00X.jpg` in the assets folder. The app gracefully falls back to a default silhouette if an image is missing.

## Grading Rules
- A+: 90 to 100
- A: 80 to below 90
- B: 70 to below 80
- C: 60 to below 70
- D: 50 to below 60
- F: below 50

- F: below 50

A student must score at least 35 in all subjects to pass. Missing records (such as 'AB' for absent) are treated as failing grades for pass/fail logic, but are ignored when computing averages mathematically.

## Publishing to GitHub
1. Initialize a git repository: `git init`
2. Add all files: `git add .`
3. Commit the changes: `git commit -m "Initial commit"`
4. Add remote origin: `git remote add origin <your-repo-url>`
5. Push to main: `git push -u origin main`
