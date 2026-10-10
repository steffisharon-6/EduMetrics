import pandas as pd
import numpy as np

def validate_dataframe(df):
    """
    Validates if the dataframe contains the required columns and correct data types.
    """
    required_columns = ['Student_ID', 'Name', 'Department', '23CB1601-CC', '23CB1602-HRM', '23CS1501-FSD', '23CS1503-AIML', '23CS1602-CD', '23AD1918-BA/23IT1909-EH']
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}"
        
    if df['Student_ID'].duplicated().any():
        return False, "Duplicate Student IDs found."
        
    if df['Name'].isnull().any() or df['Student_ID'].isnull().any() or df['Department'].isnull().any():
        return False, "Missing Student_ID, Name, or Department."
        
    subjects = ['23CB1601-CC', '23CB1602-HRM', '23CS1501-FSD', '23CS1503-AIML', '23CS1602-CD', '23AD1918-BA/23IT1909-EH']
    for subject in subjects:
        numeric_series = pd.to_numeric(df[subject], errors='coerce')
        if not ((numeric_series >= 0) & (numeric_series <= 100) | numeric_series.isnull()).all():
            return False, f"Marks must be between 0 and 100 or missing in subject: {subject}"
        
    return True, "Valid"

def calculate_totals_and_averages(df):
    """Calculates Total Marks and Average Marks for each student using NumPy."""
    subjects = ['23CB1601-CC', '23CB1602-HRM', '23CS1501-FSD', '23CS1503-AIML', '23CS1602-CD', '23AD1918-BA/23IT1909-EH']
    for sub in subjects:
        df[sub] = pd.to_numeric(df[sub], errors='coerce')
    df['Total Marks'] = np.nansum(df[subjects].values, axis=1)
    # Ignore All-NaN slices warning by capturing it or avoiding it
    with np.errstate(invalid='ignore'):
        df['Average Marks'] = np.nanmean(df[subjects].values, axis=1)
    df['Average Marks'] = df['Average Marks'].fillna(0).round(1)
    return df

def assign_grades(average):
    """Assigns grades based on average marks."""
    if average >= 90:
        return 'A+'
    elif average >= 80:
        return 'A'
    elif average >= 70:
        return 'B'
    elif average >= 60:
        return 'C'
    elif average >= 50:
        return 'D'
    else:
        return 'F'

def determine_pass_fail(row):
    """Determines Pass/Fail status based on subject marks."""
    subjects = ['23CB1601-CC', '23CB1602-HRM', '23CS1501-FSD', '23CS1503-AIML', '23CS1602-CD', '23AD1918-BA/23IT1909-EH']
    for subject in subjects:
        val = row[subject]
        if pd.isna(val):
            return 'Absent'
        if val < 35:
            return 'Fail'
    return 'Pass'

def process_student_data(df):
    """Processes the student dataframe by adding calculated columns."""
    df = calculate_totals_and_averages(df)
    df['Grade'] = df['Average Marks'].apply(assign_grades)
    df['Result Status'] = df.apply(determine_pass_fail, axis=1)
    df['Rank'] = df['Total Marks'].rank(method='min', ascending=False).astype(int)
    
    # Generate simulated attendance based on Average Marks (better students attend more generally)
    if 'Attendance (%)' not in df.columns:
        np.random.seed(42) # fixed seed for consistency
        # Set base attendance for everyone above 65
        simulated = pd.Series(np.clip(68 + (df['Average Marks'] / 100) * 25 + np.random.normal(0, 5, len(df)), 65.1, 100.0), index=df.index)
        
        # Pick 6 random students to have very low attendance (15 to 35)
        low_att_indices = np.random.choice(df.index, size=6, replace=False)
        simulated.loc[low_att_indices] = np.random.uniform(15.1, 35.0, size=6)
        
        df['Attendance (%)'] = simulated.round(1)
        df['Attendance_Is_Simulated'] = True
    else:
        df['Attendance_Is_Simulated'] = False
        
    return df

def get_class_statistics(df):
    """Calculates overall class statistics."""
    stats = {}
    stats['total_students'] = len(df)
    stats['class_average'] = df['Average Marks'].mean()
    stats['passed_students'] = len(df[df['Result Status'] == 'Pass'])
    stats['pass_percentage'] = (stats['passed_students'] / stats['total_students'] * 100) if stats['total_students'] > 0 else 0
    stats['highest_average'] = df['Average Marks'].max()
    return stats

def get_subject_summaries(df):
    """Calculates subject-wise summaries."""
    subjects = ['23CB1601-CC', '23CB1602-HRM', '23CS1501-FSD', '23CS1503-AIML', '23CS1602-CD', '23AD1918-BA/23IT1909-EH']
    return df[subjects].mean().to_dict()

def load_data(file_path_or_buffer):
    """Loads and validates data from a CSV file."""
    try:
        df = pd.read_csv(file_path_or_buffer)
        if df.empty:
            return None, "Empty dataset."
        
        is_valid, message = validate_dataframe(df)
        if not is_valid:
            return None, message
            
        df = process_student_data(df)
        return df, "Success"
    except Exception as e:
        return None, f"Error loading CSV: {str(e)}"
