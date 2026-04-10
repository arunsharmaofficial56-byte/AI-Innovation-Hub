import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle
import os

print("--- Starting Student Performance Model Training ---")

# --- 1. Generate High Quality Synthetic Dataset ---
print("Generating synthetic student dataset...")
np.random.seed(42)
n_samples = 1500

# Base features
study_hours = np.random.uniform(1.0, 14.0, n_samples)
attendance = np.random.uniform(50.0, 100.0, n_samples)
previous_marks = np.random.uniform(30.0, 95.0, n_samples)
sleep_hours = np.random.uniform(4.0, 10.0, n_samples)
internet_usage = np.random.uniform(1.0, 10.0, n_samples) # hours primarily on non-academic
extracurricular_activities = np.random.choice(["None", "Sports", "Music", "Debate", "Tech Club"], n_samples)

# Deriving the Final Exam Score logically based on the features with some noise
# Formula logic: 
# Base score comes heavily from previous marks and attendance.
# Study hours add positively up to a point.
# Too little sleep penalizes.
# High non-academic internet usage penalizes slightly.
# Extracurriculars have slight positive or neutral impact.

raw_score = (previous_marks * 0.4) + (attendance * 0.3) + (study_hours * 2.5) 
raw_score += np.where(sleep_hours < 6, -5, np.where(sleep_hours > 8, 2, 0)) # Sleep penalty/bonus
raw_score -= (internet_usage * 1.5) # Internet distraction penalty

# Adjusting purely based on clubs
club_bonus = {'None': 0, 'Sports': 2, 'Music': 3, 'Debate': 4, 'Tech Club': 5}
for i in range(n_samples):
    raw_score[i] += club_bonus[extracurricular_activities[i]]

# Add random noise for realism
noise = np.random.normal(0, 5, n_samples)
final_score = raw_score + noise

# Cap the scores realistically between 0 and 100
final_score = np.clip(final_score, 10, 100)

df = pd.DataFrame({
    'study_hours': study_hours,
    'attendance': attendance,
    'previous_marks': previous_marks,
    'sleep_hours': sleep_hours,
    'internet_usage': internet_usage,
    'extracurricular_activities': extracurricular_activities,
    'final_score': final_score
})

df.to_csv("student_data.csv", index=False)
print(f"Generated student_data.csv with {n_samples} records.")


# --- 2. Train the Random Forest Model ---
print("Preparing data pipeline...")

X = df.drop('final_score', axis=1)
y = df['final_score']

# Separate numerical and categorical columns
numeric_features = ['study_hours', 'attendance', 'previous_marks', 'sleep_hours', 'internet_usage']
categorical_features = ['extracurricular_activities']

# Create preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Create full pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Random Forest Regressor (this may take a moment)...")
pipeline.fit(X_train, y_train)

# Calculate Accuracy (R^2 Score for Regression)
score = pipeline.score(X_test, y_test)
print(f"Model trained successfully! R^2 Accuracy Score: {score*100:.2f}%")

# Save the Pipeline (Includes both scaler/encoder and model)
print("Saving model pipeline to disk...")
model_path = os.path.join(os.getcwd(), 'model_pipeline.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(pipeline, f)

# Save metrics
metrics_path = os.path.join(os.getcwd(), 'metrics.pkl')
with open(metrics_path, 'wb') as f:
     pickle.dump({'accuracy': score}, f)

print("Done! Ensure the Streamlit app uses 'model_pipeline.pkl'")
