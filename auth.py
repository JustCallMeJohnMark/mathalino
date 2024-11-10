from models import Teacher, Student
import mysql.connector

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="math"
)

cursor = db.cursor()

def load_teacher(teacher_id):
    try:
        cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
        teacher_data = cursor.fetchone()
        if teacher_data:
            return Teacher(teacher_data[0], teacher_data[1], teacher_data[2], teacher_data[3])
    except mysql.connector.Error as err:
        print("Error loading teacher from database: {}".format(err))
    return None

def load_student(student_id):
    try:
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student_data = cursor.fetchone()
        if student_data:
            return Student(student_data[0], student_data[1], student_data[2], student_data[3])
    except mysql.connector.Error as err:
        print("Error loading student from database: {}".format(err))
    return None

def login_user(user):
    # Log in the user
    pass

def logout_user():
    # Log out the user
    pass