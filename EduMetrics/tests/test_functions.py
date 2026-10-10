import pytest
import pandas as pd
import numpy as np
from functions import (
    validate_dataframe,
    calculate_totals_and_averages,
    assign_grades,
    determine_pass_fail,
    process_student_data,
    get_class_statistics,
    get_subject_summaries
)

def get_valid_df():
    return pd.DataFrame({
        'Student_ID': ['S1', 'S2', 'S3'],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Department': ['CSBS', 'CSBS', 'CSBS'],
        '23CB1601-CC': [90, 40, 30],
        '23CB1602-HRM': [85, 45, 80],
        '23CS1501-FSD': [92, 50, 75],
        '23CS1503-AIML': [88, 60, 65],
        '23CS1602-CD': [85, 70, pd.NA],
        '23AD1918-BA/23IT1909-EH': [95, 80, 70]
    })

def test_validate_valid_df():
    df = get_valid_df()
    is_valid, msg = validate_dataframe(df)
    assert is_valid is True
    assert msg == "Valid"

def test_validate_missing_columns():
    df = get_valid_df().drop(columns=['23CB1601-CC'])
    is_valid, msg = validate_dataframe(df)
    assert is_valid is False
    assert "Missing required columns: 23CB1601-CC" in msg

def test_validate_duplicate_ids():
    df = get_valid_df()
    df.loc[2, 'Student_ID'] = 'S1' # duplicate
    is_valid, msg = validate_dataframe(df)
    assert is_valid is False
    assert "Duplicate Student IDs found" in msg

def test_validate_invalid_marks():
    df = get_valid_df()
    df.loc[0, '23CB1601-CC'] = 150
    is_valid, msg = validate_dataframe(df)
    assert is_valid is False
    assert "Marks must be between 0 and 100" in msg

def test_validate_missing_values():
    df = get_valid_df()
    df.loc[0, 'Name'] = None
    is_valid, msg = validate_dataframe(df)
    assert is_valid is False
    assert "Missing Student_ID, Name, or Department" in msg

def test_totals_and_averages():
    df = get_valid_df()
    df = calculate_totals_and_averages(df)
    # Alice: 90+85+92+88+85+95 = 535
    assert df.loc[0, 'Total Marks'] == 535
    assert df.loc[0, 'Average Marks'] == 535 / 6

def test_assign_grades():
    assert assign_grades(95) == 'A+'
    assert assign_grades(90) == 'A+'
    assert assign_grades(89.9) == 'A'
    assert assign_grades(80) == 'A'
    assert assign_grades(75) == 'B'
    assert assign_grades(65) == 'C'
    assert assign_grades(55) == 'D'
    assert assign_grades(45) == 'F'

def test_determine_pass_fail():
    df = get_valid_df()
    # S1 passes all (>35)
    assert determine_pass_fail(df.iloc[0]) == 'Pass'
    # S3 has NA in CD and fails CC
    assert determine_pass_fail(df.iloc[2]) == 'Fail'

def test_process_student_data():
    df = get_valid_df()
    df = process_student_data(df)
    assert 'Total Marks' in df.columns
    assert 'Average Marks' in df.columns
    assert 'Grade' in df.columns
    assert 'Result Status' in df.columns
    assert 'Rank' in df.columns
    
    # Alice should be rank 1
    assert df.loc[0, 'Rank'] == 1
    # Charlie: 30+80+75+65+NA+70 = 320. Avg = 320 / 5 = 64.
    # Bob: 40+45+50+60+70+80 = 345. Avg = 345 / 6 = 57.5
    assert df.loc[1, 'Rank'] == 3

def test_get_class_statistics():
    df = get_valid_df()
    df = process_student_data(df)
    stats = get_class_statistics(df)
    assert stats['total_students'] == 3
    assert stats['passed_students'] == 2 # Alice and Bob
    assert stats['highest_average'] == df['Average Marks'].max()

def test_get_subject_summaries():
    df = get_valid_df()
    df = calculate_totals_and_averages(df)
    means = get_subject_summaries(df)
    assert np.isclose(means['23CB1601-CC'], (90+40+30)/3)
    assert '23CS1501-FSD' in means
