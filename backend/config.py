class Config:
    # Flask
    SECRET_KEY = "student_prediction"
    # MySQL Configuration
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "Root@12345"     
    MYSQL_DB = "student_prediction"
    MYSQL_CURSORCLASS = "DictCursor"
    DEBUG = True