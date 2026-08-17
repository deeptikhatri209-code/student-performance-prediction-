import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load Dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(
    BASE_DIR,
    "..",
    "dataset",
    "student_data.csv"
)

data = pd.read_csv(dataset_path)

# Features
X = data[[
    "attendance",
    "study_hours",
    "assignment_marks",
    "previous_grade"
]]

# Target
y = data["final_grade"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Test Accuracy
prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("Model Accuracy :", round(accuracy * 100, 2), "%")

# Save Model
model_path = os.path.join(
    BASE_DIR,
    "student_model.pkl"
)

joblib.dump(model, model_path)

print("Model Saved Successfully")
print("Saved at :", model_path)