import os
import sys
from flask import Flask, render_template

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import Config
from database.db_connection import init_db, mysql

# Import Blueprints
from routes.auth import auth
from routes.dashboard import dashboard
from routes.student import student
from routes.prediction import prediction
from routes.api import api

# Create Flask App
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Load Config
app.config.from_object(Config)

# Initialize Database
init_db(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(student)
app.register_blueprint(prediction)
app.register_blueprint(api)

# Home
@app.route("/")
def home():
    return render_template("index.html")

# Login
@app.route("/login")
def login():
    return render_template("login.html")

# Help
@app.route("/help")
def help():
    return render_template("help.html")

# Settings
@app.route("/settings")
def settings():
    return render_template("settings.html")

# Database Test
@app.route("/test-db")
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT DATABASE();")
        result = cur.fetchone()
        cur.close()
        return f"Connected Successfully : {result[0]}"

    except Exception as e:
        return f"Database Error : {e}"

# Run App
if __name__ == "__main__":
    app.run(debug=True)
    