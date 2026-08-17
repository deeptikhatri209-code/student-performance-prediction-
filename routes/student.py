from flask import Blueprint, render_template, request, redirect, url_for,flash, send_file
from database.db_connection import mysql
from reportlab.pdfgen import canvas
import os
student = Blueprint("student", __name__)

# Show All Students
@student.route("/students")
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()
    return render_template("students.html", students=students)

# Add Student Page
@student.route("/add_student")
def add_student():
    return render_template("add_student.html")

# Save Student
@student.route("/save_student", methods=["POST"])
def save_student():
    roll_no = request.form["roll_no"]
    name = request.form["name"]
    attendance = request.form["attendance"]
    study_hours = request.form["study_hours"]
    assignment_marks = request.form["assignment_marks"]
    previous_grade = request.form["previous_grade"]
    final_grade = request.form["final_grade"]
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO students
        (roll_no, name, attendance, study_hours, assignment_marks, previous_grade, final_grade)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        roll_no,
        name,
        attendance,
        study_hours,
        assignment_marks,
        previous_grade,
        final_grade
    ))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("student.students"))

# Edit Student Page
@student.route("/edit_student/<int:id>")
def edit_student(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE id=%s", (id,))
    student_data = cur.fetchone()
    cur.close()
    return render_template(
        "edit_student.html",
        student=student_data
    )

# Update Student
@student.route("/update_student/<int:id>", methods=["POST"])
def update_student(id):
    roll_no = request.form["roll_no"]
    name = request.form["name"]
    attendance = request.form["attendance"]
    study_hours = request.form["study_hours"]
    assignment_marks = request.form["assignment_marks"]
    previous_grade = request.form["previous_grade"]
    final_grade = request.form["final_grade"]
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE students
        SET
            roll_no=%s,
            name=%s,
            attendance=%s,
            study_hours=%s,
            assignment_marks=%s,
            previous_grade=%s,
            final_grade=%s
        WHERE id=%s
    """, (
        roll_no,
        name,
        attendance,
        study_hours,
        assignment_marks,
        previous_grade,
        final_grade,
        id
    ))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("student.students"))

# Delete Student
@student.route("/delete_student/<int:id>")
def delete_student(id):
    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("student.students"))

@student.route("/download_student/<int:id>")
def download_student(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id,name,attendance,study_hours,
               assignment_marks,previous_grade,final_grade
        FROM students
        WHERE id=%s
    """, (id,))
    student = cur.fetchone()
    cur.close()
    if not student:
        return "Student not found"
    pdf_path = f"student_{id}.pdf"
    c = canvas.Canvas(pdf_path)
    c.setFont("Helvetica-Bold",18)
    c.drawString(170,800,"Student Performance Report")
    c.setFont("Helvetica",12)
    y = 760
    c.drawString(50,y,f"ID : {student['id']}")
    y -= 30
    c.drawString(50,y,f"Name : {student['name']}")
    y -= 30
    c.drawString(50,y,f"Attendance : {student['attendance']} %")
    y -= 30
    c.drawString(50,y,f"Study Hours : {student['study_hours']}")
    y -= 30
    c.drawString(50,y,f"Assignment Marks : {student['assignment_marks']}")
    y -= 30
    c.drawString(50,y,f"Previous Grade : {student['previous_grade']}")
    y -= 30
    c.drawString(50,y,f"Final Grade : {student['final_grade']}")
    c.save()
    return send_file(pdf_path, as_attachment=True)
    
@student.route("/download_report")
def download_report():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, name, attendance, study_hours,
        assignment_marks, previous_grade, final_grade
        FROM students
    """)
    students = cur.fetchall()
    cur.close()
    pdf_path = "student_report.pdf"
    c = canvas.Canvas(pdf_path)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(170, 800, "Student Performance Report")
    y = 770
    c.setFont("Helvetica", 10)
    for s in students:
        # line = f"ID:{s[0]}  Name:{s[1]}  Attendance:{s[2]}%  Study:{s[3]}  Assignment:{s[4]}  Previous:{s[5]}  Final:{s[6]}"
        line = (
            f"ID:{s['id']}  "
            f"Name:{s['name']}  "
            f"Attendance:{s['attendance']}%  "
            f"Study:{s['study_hours']}  "
            f"Assignment:{s['assignment_marks']}  "
            f"Previous:{s['previous_grade']}  "
            f"Final:{s['final_grade']}"
        )
        c.drawString(20, y, line)
        y -= 20
        if y < 40:
            c.showPage()
            y = 800
    c.save()
    return send_file(pdf_path, as_attachment=True)