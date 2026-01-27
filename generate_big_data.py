import pandas as pd
import numpy as np

NUM_STUDENTS = 10000 

np.random.seed(42)

student_ids = np.arange(1001, 1001 + NUM_STUDENTS)

attendance = np.random.normal(loc=75, scale=15, size=NUM_STUDENTS)
attendance = np.clip(attendance, 0, 100).round(1)

study_hours = np.random.gamma(shape=2, scale=2.5, size=NUM_STUDENTS)
study_hours = np.clip(study_hours, 0, 20).round(1)

previous_scores = (0.5 * attendance) + np.random.normal(loc=40, scale=10, size=NUM_STUDENTS)
previous_scores = np.clip(previous_scores, 0, 100).round(1)

internet_access = np.random.choice(['Yes', 'No'], size=NUM_STUDENTS, p=[0.85, 0.15])

score_metric = (0.3 * attendance) + (2.5 * study_hours) + (0.4 * previous_scores)
noise = np.random.normal(0, 10, NUM_STUDENTS)
final_metric = score_metric + noise

threshold = np.percentile(final_metric, 30)
results = ['Pass' if x > threshold else 'Fail' for x in final_metric]

df = pd.DataFrame({
    'Student_ID': student_ids,
    'Attendance_Rate': attendance,
    'Study_Hours': study_hours,
    'Previous_Scores': previous_scores,
    'Internet_Access': internet_access,
    'Result': results
})

mask = np.random.choice([True, False], size=NUM_STUDENTS, p=[0.05, 0.95])
df.loc[mask, 'Attendance_Rate'] = np.nan

filename = "large_student_data.csv"
df.to_csv(filename, index=False)

print(f"Generated {filename} with {NUM_STUDENTS} rows.")