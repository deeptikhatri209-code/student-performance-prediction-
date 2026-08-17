from flask import Blueprint, render_template
from database.db_connection import mysql

dashboard = Blueprint("dashboard", __name__)
@dashboard.route("/dashboard")
def dashboard_page():
    cur = mysql.connection.cursor()
    # Total Students
    cur.execute("SELECT COUNT(*) AS total_students FROM students")
    total_students = cur.fetchone()["total_students"]

    # Average Attendance
    cur.execute("SELECT ROUND(AVG(attendance),2) AS avg_attendance FROM students")
    avg_attendance = cur.fetchone()["avg_attendance"]

    # Average Study Hours
    cur.execute("SELECT ROUND(AVG(study_hours),2) AS avg_study_hours FROM students")
    avg_study_hours = cur.fetchone()["avg_study_hours"]

    # Average Assignment Marks
    cur.execute("SELECT ROUND(AVG(assignment_marks),2) AS avg_assignment_marks FROM students")
    avg_assignment_marks = cur.fetchone()["avg_assignment_marks"]

    # Average Final Grade
    cur.execute("""
    SELECT ROUND(AVG(
        CASE final_grade
            WHEN 'A+' THEN 100
            WHEN 'A'  THEN 90
            WHEN 'B+' THEN 80
            WHEN 'B'  THEN 70
            WHEN 'C+' THEN 60
            WHEN 'C'  THEN 50
            WHEN 'D'  THEN 40
            ELSE 0
        END
    ), 2) AS avg_final_grade
    FROM students
    """)
    result = cur.fetchone()
    avg_final_grade = result["avg_final_grade"] if result["avg_final_grade"] is not None else 0
    
    # Pass Students
    cur.execute("""
    SELECT COUNT(*) AS pass_students
    FROM students
    WHERE final_grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C')
    """)
    pass_students = cur.fetchone()["pass_students"]

    # Fail Students
    cur.execute("""
    SELECT COUNT(*) AS fail_students
    FROM students
    WHERE final_grade IN ('D', 'F')
    """)
    fail_students = cur.fetchone()["fail_students"]

    cur.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        avg_attendance=avg_attendance,
        avg_study_hours=avg_study_hours,
        avg_assignment_marks=avg_assignment_marks,
        avg_final_grade=avg_final_grade,
        pass_students=pass_students,
        fail_students=fail_students
    )
@dashboard.route("/help")
def help_page():
    return render_template("help.html")
@dashboard.route("/settings")
def settings_page():
    return render_template("settings.html")
