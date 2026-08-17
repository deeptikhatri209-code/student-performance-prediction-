from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db_connection import mysql

auth = Blueprint("auth", __name__)
# Login Page
@auth.route("/login")
def login():
    return render_template("login.html")

# Login Authentication
@auth.route("/login", methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cur.fetchone()
    cur.close()
    if user:
        session["user"] = user["username"]
        return redirect(url_for("dashboard.dashboard_page"))
    flash("Invalid Username or Password")
    return redirect(url_for("auth.login"))

# Logout
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))