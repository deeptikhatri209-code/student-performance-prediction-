from flask_mysqldb import MySQL
# Create MySQL object
mysql = MySQL()
def init_db(app):
    """
    Initialize MySQL with Flask application
    """
    mysql.init_app(app)