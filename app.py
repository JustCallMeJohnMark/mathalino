from flask import Flask, render_template, request, redirect, url_for,jsonify, abort, session
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from random import shuffle
from flask_bcrypt import Bcrypt
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.linear_model import LinearRegression
import numpy as np
from mysql.connector import Error
import logging
import json



app = Flask(__name__)
app.secret_key = 'non'
bcrypt = Bcrypt(app)
SECRET_KEY = "BSCS4A"
logging.basicConfig(level=logging.ERROR)


# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="", 
    database="math"
)

cursor = db.cursor()




# Index Route
@app.route('/')
def index():
    return render_template('index.html')

# Registration Route
@app.route('/student_register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        fullname = request.form.get('fullname')
        section = request.form.get('section')
        age = request.form.get('age')
        gender = request.form.get('gender')

        # Validate that all fields are filled
        if not username or not password or not fullname or not section or not age or not gender:
            return "All fields are required!"

        # Hash password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if username exists
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            users = cursor.fetchone()

            if users:
                return 'Username already exists!'
        except mysql.connector.Error as err:
            print(f"Error checking username: {err}")
            return "Error checking username"

        # Insert new user
        try:
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, fullname, section, age, gender) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """, 
                (username, password_hash, fullname, section, age, gender)
            )
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting user: {err}")
            return "Error inserting user"

        return redirect(url_for('student_login'))

    return render_template('student_register.html')


@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username exists and get user details
        try:
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                # Verify password using bcrypt
                if bcrypt.check_password_hash(user[2], password):
                    # Set session data without sensitive information
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    return redirect(url_for('student_dashboard'))
                else:
                    return 'Invalid username or password.'  # Password mismatch
            else:
                return 'Invalid username or password.'  # User not found
        except mysql.connector.Error as err:
            print("Error checking user credentials: {}".format(err))
            return "Error checking user credentials"

    return render_template('student_login.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            answers = request.form.to_dict()
            score = 0

            # Fetch correct answers from the database
            cursor.execute("SELECT id, correct_answer FROM questions")
            questions = cursor.fetchall()

            # Checking answers
            for question in questions:
                q_id = str(question[0])
                correct_answer = question[1]
                user_answer = answers.get(f"answer_{q_id}")

                if user_answer and user_answer.strip().lower() == correct_answer.strip().lower():
                    score += 1

            # Calculate score and proficiency
            total_questions = len(questions)
            percentage_score = (score / total_questions) * 100 if total_questions > 0 else 0

            if 100 >= percentage_score >= 81:
                proficiency = "Highly Proficient"
            elif 80 >= percentage_score >= 61:
                proficiency = "Proficient"
            elif 60 >= percentage_score >= 41:
                proficiency = "Nearly Proficient"
            elif 40 >= percentage_score >= 21:
                proficiency = "Low Proficient"
            else:
                proficiency = "Not Proficient"

            # Get total_time_spent
            total_time_spent = request.form.get('total_time_spent', '0')
            try:
                total_time_spent = int(total_time_spent)  # Convert to integer
            except ValueError:
                total_time_spent = 0  # Default to 0 if conversion fails

            # Get time_per_question as JSON
            time_per_question = request.form.get('time_per_question', '[]')
            print("Raw time_per_question data received:", time_per_question)  # Debugging line
            try:
                time_per_question = json.loads(time_per_question)  # Parse JSON to list
                if not isinstance(time_per_question, list) or not all(isinstance(i, int) for i in time_per_question):
                    time_per_question = [0] * total_questions  # Default if invalid
            except json.JSONDecodeError as e:
                print("JSON Decode Error:", str(e))  # Log the error message
                time_per_question = [0] * total_questions  # Default if JSON decoding fails
            except ValueError as ve:
                print("Value Error:", str(ve))  # Log the error message
                time_per_question = []  # Default if it's not a valid list

            cursor.execute("""
                INSERT INTO scores (user_id, score, proficiency, total_time_spent, time_per_question) 
                VALUES (%s, %s, %s, %s, %s)
            """, (session['user_id'], int(percentage_score), proficiency, total_time_spent, json.dumps(time_per_question)))
            db.commit()
            print("Data inserted successfully into `scores` table.")

            return redirect(url_for('result', score=int(percentage_score), proficiency=proficiency, correct_answers=score, total_questions=total_questions))
        
        except Exception as err:
            print(f"Error processing quiz: {err}")
            return "Error processing quiz"

    # GET request - Fetch and shuffle questions
    try:
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        shuffle(questions)
    except mysql.connector.Error as err:
        print(f"Error fetching questions from database: {err}")
        return "Error fetching questions from database"

    return render_template('quiz.html', questions=questions)


@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('student_login'))

    user_id = session['user_id']

    # Fetch recent test scores for the user
    try:
        cursor.execute("SELECT * FROM scores WHERE user_id = %s ORDER BY date_taken DESC LIMIT 5", (user_id,))
        scores = cursor.fetchall()
    except mysql.connector.Error as err:
        logging.error(f"Error fetching scores from database: {err}")
        return "Error fetching scores from database"

    # Format the date and time for each score
    formatted_scores = []
    for score in scores:
        date_taken = score[4]
        try:
            date_taken = datetime.fromtimestamp(float(date_taken)).strftime('%Y-%m-%d %H:%M:%S')
        except (TypeError, ValueError):
            logging.warning(f"Invalid date format for score: {score}")
            date_taken = str(date_taken)  # Keep original format if conversion fails

        formatted_scores.append({
            'score': float(score[3]),
            'proficiency': score[5],
            'date_taken': date_taken
        })

    return render_template('student_dashboard.html', username=session['username'], recent_scores=formatted_scores)


@app.route('/result', methods=['GET'])
def result():
    # Parse query parameters safely with default values if missing
    try:
        score = int(request.args.get('score', 0))  # Default to 0 if missing
        proficiency = request.args.get('proficiency', 'Not Proficient')
        correct_answers = int(request.args.get('correct_answers', 0))
        total_questions = int(request.args.get('total_questions', 1))  # Default to 1 to avoid division by zero
    except (TypeError, ValueError) as e:
        logging.error(f"Error parsing result parameters: {e}")
        return "Error parsing result parameters.", 400

    # Initialize predicted_score
    predicted_score = None

    # Ensure user_id is available in the session
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('student_login'))

    # Attempt to predict the next score for the student
    try:
        model = train_linear_regression(user_id)
        if model:
            next_test_timestamp = datetime.now().timestamp()
            # Prepare input for prediction
            predicted_score = model.predict(np.array([[next_test_timestamp, 0, 0]]))[0][0]
        else:
            logging.warning(f"Not enough data to train the model for user_id: {user_id}")
    except Exception as e:
        logging.error(f"Error predicting score: {e}")

    return render_template('result.html', score=score, proficiency=proficiency, 
                           correct_answers=correct_answers, total_questions=total_questions, 
                           predicted_score=predicted_score)


def train_linear_regression(user_id):
    try:
        cursor.execute("""
            SELECT score, date_taken, total_time_spent, time_per_question 
            FROM scores 
            WHERE user_id = %s 
            ORDER BY date_taken ASC
        """, (user_id,))
        scores_data = cursor.fetchall()
        logging.debug(f"Fetched scores data for user_id {user_id}: {scores_data}")

        # Check for insufficient data
        if len(scores_data) < 2:
            logging.warning(f"Not enough data to train the model for user_id: {user_id}. Found {len(scores_data)} records.")
            return None

        dates = np.array([data[1].timestamp() for data in scores_data]).reshape(-1, 1)
        scores = np.array([float(data[0]) for data in scores_data]).reshape(-1, 1)
        total_time_spent = np.array([float(data[2]) if data[2] is not None else 0 for data in scores_data]).reshape(-1, 1)

        time_per_question = []
        for data in scores_data:
            if data[3]:
                try:
                    mean_time = np.mean(json.loads(data[3])) if json.loads(data[3]) else 0
                    time_per_question.append(float(mean_time))
                except (json.JSONDecodeError, TypeError) as e:
                    logging.error(f"Invalid JSON for time_per_question: {data[3]}, Error: {e}")
                    time_per_question.append(0)
            else:
                time_per_question.append(0)
        time_per_question = np.array(time_per_question).reshape(-1, 1)

        # Combine all features into one array and handle NaNs
        features = np.hstack((dates, total_time_spent, time_per_question))
        if np.isnan(features).any():
            logging.error("Features contain NaN values. Cannot train the model.")
            return None

        model = LinearRegression()
        model.fit(features, scores)
        logging.debug(f"Model coefficients: {model.coef_}")
        logging.debug(f"Model intercept: {model.intercept_}")

        return model

    except Exception as e:
        logging.error(f"Error during model training: {e}")
        return None


@app.route('/predict_next_score', methods=['GET'])
def predict_next_score():
    if 'user_id' not in session:
        return redirect(url_for('student_login'))

    user_id = session['user_id']

    try:
        cursor.execute("""
            SELECT total_time_spent, time_per_question 
            FROM scores 
            WHERE user_id = %s 
            ORDER BY date_taken DESC 
            LIMIT 1
        """, (user_id,))
        latest_data = cursor.fetchone()

        if latest_data is None:
            logging.warning(f"No recent data found for user_id: {user_id}")
            return jsonify({"error": "No recent data available for prediction."}), 404

        total_time_spent = latest_data[0] if latest_data[0] is not None else 0
        time_per_question_json = latest_data[1]

        time_per_question = 0
        if time_per_question_json and time_per_question_json != '[]':
            try:
                time_per_question = np.mean(json.loads(time_per_question_json))
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON for time_per_question: {e}")

        model = train_linear_regression(user_id)
        if model is None:
            return jsonify({"error": "Not enough data to make predictions."}), 400

        next_test_timestamp = datetime.now().timestamp()
        input_features = np.array([[next_test_timestamp, total_time_spent, time_per_question]])

        if input_features.shape[1] != 3:
            logging.error(f"Input features shape mismatch: {input_features.shape}. Expected 3 features.")
            return jsonify({"error": "Input features must have exactly 3 features."}), 400

        predicted_score = model.predict(input_features)[0][0]
        logging.debug(f"Predicted score: {predicted_score}")

        return jsonify({"predicted_score": predicted_score})

    except Exception as e:
        logging.error(f"Error predicting score: {e}")
        return jsonify({"error": "An error occurred while predicting the score."}), 500
             
# Teacher Registration Route
@app.route('/teacher_register', methods=['GET', 'POST'])
def teacher_register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        password = request.form.get('password')
        section = request.form.get('section')
        input_secret_key = request.form.get('secret_key')

        # Validate form data
        if not fullname or not password or not section or not input_secret_key:
            return "All fields are required."

        # Check if the input secret key matches the predefined secret key
        if input_secret_key != SECRET_KEY:
            return "Invalid secret key."

        # Hash the password (use 'pbkdf2:sha256' explicitly to avoid any hashing method errors)
        try:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        except ValueError as e:
            print(f"Hashing error: {e}")
            return "Error hashing password."

        # Check if the teacher already exists in the database
        try:
            cursor.execute("SELECT * FROM teachers WHERE fullname = %s", (fullname,))
            existing_teacher = cursor.fetchone()

            if existing_teacher:
                return "Teacher with that full name already exists."
        except mysql.connector.Error as err:
            print(f"Error checking teacher: {err}")
            return "Error checking teacher in the database."

        # Insert new teacher into the database
        try:
            cursor.execute(
                "INSERT INTO teachers (fullname, password_hash, section, secret_key) VALUES (%s, %s, %s, %s)",
                (fullname, password_hash, section, SECRET_KEY)
            )
            db.commit()
            print(f"Teacher '{fullname}' registered successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting teacher: {err}")
            return "Error inserting teacher into the database."

        return redirect(url_for('teacher_login'))

    # GET request returns the registration form
    return render_template('teacher_register.html')


# Teacher Login Route
@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        password = request.form.get('password')

        # Validate form data
        if not fullname or not password:
            return "Full name and password are required."

        # Fetch the teacher's data from the database
        try:
            cursor.execute("SELECT id, password_hash, fullname FROM teachers WHERE fullname = %s", (fullname,))
            teacher = cursor.fetchone()

            if teacher is None:
                print(f"No teacher found with fullname: {fullname}")
                return "No user found with that full name."
        except mysql.connector.Error as err:
            print(f"Error fetching teacher from database: {err}")
            return "Error fetching teacher from the database."

        # Check password
        teacher_id, password_hash, teacher_name = teacher
        try:
            if check_password_hash(password_hash, password):
                # Set session variables
                session['teacher_id'] = teacher_id
                session['teacher_name'] = teacher_name
                print(f"Teacher '{teacher_name}' logged in successfully.")
                return redirect(url_for('teacher_dashboard'))
            else:
                print("Invalid password attempt.")
                return "Invalid full name or password."
        except ValueError as e:
            print(f"Password checking error: {e}")
            return "Error checking password."

    # GET request returns the login form
    return render_template('teacher_login.html')


@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))
    
    teacher_id = session['teacher_id']
    teacher_name, teacher_section = get_teacher_name_and_section(teacher_id)  # Updated function name
    if teacher_name is None:
        abort(404)
    
    # Fetch and format only the results for students in the teacher's section
    recent_results = get_recent_results(teacher_id, teacher_section)
    formatted_results = format_results(recent_results)

    # Prepare chart data using only the latest results
    chart_data = {
        'scores': [result['latest_result']['score'] for result in formatted_results],
        'dates': [result['latest_result']['date_taken'] for result in formatted_results],
        'recent_results': formatted_results
    }

    return render_template(
        'teacher_dashboard.html', 
        teacher_name=teacher_name, 
        recent_results=formatted_results,
        chart=chart_data
    )

def get_teacher_name_and_section(teacher_id):
    query = "SELECT fullname, section FROM teachers WHERE id = %s"
    try:
        cursor.execute(query, (teacher_id,))
        teacher_data = cursor.fetchone()
        if teacher_data:
            return teacher_data[0], teacher_data[1]  # Return both name and section
        return None, None
    except Error as err:
        logging.error(f"Error fetching teacher from database: {err}")
        abort(500)

def get_recent_results(teacher_id, section):
    query = """
        SELECT 
            u.id AS student_id,
            u.username, 
            u.section,
            u.age, 
            u.gender,
            s.score, 
            s.proficiency, 
            s.date_taken 
        FROM 
            users u 
        INNER JOIN 
            scores s ON u.id = s.user_id 
        WHERE 
            u.section = %s AND (s.teacher_id IS NULL OR s.teacher_id = %s)  
        ORDER BY 
            u.id, s.date_taken DESC
    """
    try:
        cursor.execute(query, (section, teacher_id))  # Filter by section and teacher_id
        results = cursor.fetchall()
        return results if results else []
    except Error as err:
        logging.error(f"Error fetching results from database: {err}")
        abort(500)

def format_results(results):
    formatted_results = []
    student_results = {}
    
    for result in results:
        student_id, username, section, age, gender, score, proficiency, date_taken = result
        
        # Group results by student_id
        if student_id not in student_results:
            student_results[student_id] = {
                'student_id': student_id,
                'username': username,
                'section': section,
                'age': age,
                'gender': gender,
                'results': []
            }
        
        # Append each result to the student's result list
        student_results[student_id]['results'].append({
            'score': score,
            'proficiency': proficiency,
            'date_taken': date_taken
        })
    
    # For each student, save only the latest result at the top
    for student in student_results.values():
        latest_result = student['results'][0]
        formatted_results.append({
            'student_id': student['student_id'],
            'username': student['username'],
            'section': student['section'],
            'age': student['age'],
            'gender': student['gender'],
            'latest_result': latest_result,
            'all_results': student['results']  # Include all results for toggling
        })

    return formatted_results


def train_teacher_linear_regression(teacher_id):
    try:
        cursor.execute("""
            SELECT 
                u.id AS student_id,
                AVG(s.score) AS avg_score, 
                AVG(s.total_time_spent) AS avg_time_spent, 
                AVG(s.time_per_question) AS avg_time_per_question
            FROM 
                scores s
            INNER JOIN 
                users u ON s.user_id = u.id
            WHERE 
                s.teacher_id = %s
            GROUP BY 
                u.id
        """, (teacher_id,)) 

        scores_data = cursor.fetchall()
        if len(scores_data) < 2:
            return None

        features = np.array([[data[2], data[3]] for data in scores_data])
        scores = np.array([[data[1]] for data in scores_data])

        if np.isnan(features).any() or np.isnan(scores).any():
            return None

        model = LinearRegression()
        model.fit(features, scores)
        return model

    except Exception as e:
        logging.error(f"Error during model training for teacher: {e}")
        return None


@app.route('/predict_teacher_score', methods=['GET'])
def predict_teacher_score():
    teacher_id = request.args.get('teacher_id')
    logging.info(f"Received teacher_id: {teacher_id}")
    
    if not teacher_id:
        logging.error("Teacher ID is missing in request.")
        return jsonify({"error": "Teacher ID is missing. Please provide a valid teacher ID."}), 400

    try:
        teacher_id = int(teacher_id)
        logging.info(f"Teacher ID after conversion: {teacher_id}")
        
        model = train_teacher_linear_regression(teacher_id)
        if model is None:
            logging.warning("Not enough data to train the model for the teacher.")
            return jsonify({"error": "Not enough data to make predictions for the teacher."}), 400

        cursor.execute("""
            SELECT 
                AVG(total_time_spent) AS avg_time_spent, 
                AVG(time_per_question) AS avg_time_per_question
            FROM 
                scores s
            INNER JOIN 
                users u ON s.user_id = u.id
            WHERE 
                u.teacher_id = %s
        """, (teacher_id,))
        
        latest_data = cursor.fetchone()
        if latest_data is None or (latest_data[0] is None and latest_data[1] is None):
            logging.warning("No recent data available for prediction.")
            return jsonify({"error": "No recent data available for prediction."}), 404

        avg_time_spent = latest_data[0] if latest_data[0] is not None else 0
        avg_time_per_question = latest_data[1] if latest_data[1] is not None else 0
        logging.info(f"Average time spent: {avg_time_spent}, Average time per question: {avg_time_per_question}")

        features = np.array([[avg_time_spent, avg_time_per_question]])
        predicted_score = model.predict(features)[0][0]
        logging.info(f"Predicted score: {predicted_score}")

        return jsonify({
            "predicted_score": predicted_score,
            "avg_time_spent": avg_time_spent,
            "avg_time_per_question": avg_time_per_question
        })

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return jsonify({"error": "Invalid teacher ID format."}), 400
    except Exception as e:
        logging.error(f"Exception during prediction: {str(e)}")
        return jsonify({"error": "An error occurred while predicting the score."}), 500
# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('teacher_id', None)
    session.pop('teacher_name', None)
    return redirect(url_for('student_login'))

if __name__ == '__main__':
    app.run(debug=True)