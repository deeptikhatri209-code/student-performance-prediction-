from flask import Blueprint, render_template, request
from backend.model.predictor import predict_student
prediction = Blueprint("prediction", __name__)

# Prediction Page
@prediction.route("/prediction")
def prediction_page():
    return render_template("prediction.html")

# Predict Student Performance
@prediction.route("/predict", methods=["POST"])
def predict():
    try:
        attendance = float(request.form["attendance"])
        study_hours = float(request.form["study_hours"])
        assignment_marks = float(request.form["assignment_marks"])
        previous_grade = float(request.form["previous_grade"])
        result = predict_student(
            attendance,
            study_hours,
            assignment_marks,
            previous_grade
        )
        return render_template(
            "prediction.html",
            prediction=result,
            attendance=attendance,
            study_hours=study_hours,
            assignment_marks=assignment_marks,
            previous_grade=previous_grade
        )
    except Exception as e:
        return render_template(
            "prediction.html",
            error=str(e)
        )