import os
import joblib
import pandas as pd

# Load Trained Model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "student_model.pkl")

model = joblib.load(MODEL_PATH)

# Prediction Function
def predict_student(attendance,
                    study_hours,
                    assignment_marks,
                    previous_grade):
    """
    Predict the student's final grade.
    """

    data = pd.DataFrame({
        "attendance": [attendance],
        "study_hours": [study_hours],
        "assignment_marks": [assignment_marks],
        "previous_grade": [previous_grade]
    })

    prediction = model.predict(data)

    return prediction[0]