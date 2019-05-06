from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
from time import gmtime, strftime
from flask import g
import hashlib
import sqlite3 as sql
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "hw13.db"
USER = "admin"
PASSWORD = "password"

# Flask initialize
app = Flask(__name__)
app.secret_key = 'app secret key'
# --------------------------------
# ---- database config
# --------------------------------
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_first_request
def init_database_config():
    init_db()

# -----------------------------------
# ----- index but redirect to login page
# -----------------------------------
@app.route('/')
def index():

    return render_template('login.html', error='f')


# -----------------------------------
# ----- user login
# -----------------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USER and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='t')
    else:
        return render_template('login.html', error='f')

# -----------------------------------
# ----- user dashboard
# -----------------------------------
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if not session.get('logged_in'):
        return render_template('login.html', error='f')
    else:
        cur = get_db().execute("SELECT * FROM students")
        students = cur.fetchall()
        cur = get_db().execute("SELECT * FROM quiz")
        quizs = cur.fetchall()
        return render_template('dashboard.html', students=students, quizs=quizs)

@app.route('/student/add', methods=['POST', 'GET'])
def create_student():
    if not session.get('logged_in'):
        return render_template('login.html', error='f')
    else:
        if request.method == 'POST':
            firstName = request.form['firstName']
            lastName = request.form['lastName']

            if not firstName == '' and not lastName == '':
                get_db().execute("INSERT INTO students (firstName, lastName) VALUES (?,?)", (firstName, lastName))
                get_db().commit()
                return redirect(url_for('dashboard'))
            else:
                return render_template('create_student.html', error='t')
        else:
            return render_template('create_student.html', error='f')

@app.route('/quiz/add', methods=['POST', 'GET'])
def create_quiz():
    if not session.get('logged_in'):
        return render_template('login.html', error='f')
    else:
        if request.method == 'POST':
            subject = request.form['subject']
            questions = request.form['questions']
            quizdate = request.form['quizDate']

            if not subject == '' and not questions == '' and not quizdate == '':
                get_db().execute("INSERT INTO quiz (subject, questions, quizDate) VALUES (?,?,?)", (subject, questions, quizdate))
                get_db().commit()
                return redirect(url_for('dashboard'))
            else:
                return render_template('create_quiz.html', error='t')
        else:
            return render_template('create_quiz.html', error='f')


@app.route('/student/<id>', methods=['GET'])
def view_quiz_result(id):
    if not session.get('logged_in'):
        return render_template('login.html', error='f')
    else:
        if request.method == 'GET':
            student = id

            if not student == '':
                cur = get_db().execute("SELECT * FROM results JOIN quiz ON results.quizid = quiz.id WHERE studentid='%s'" % student)
                results = cur.fetchall()
                return render_template('view_quiz_result.html', results=results)
            else:
                return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('dashboard'))


@app.route('/results/add', methods=['POST', 'GET'])
def create_quiz_result():
    if not session.get('logged_in'):
        return render_template('login.html', error='f')
    else:
        if request.method == 'POST':
            quizid = request.form['quizid']
            studentid = request.form['studentid']
            score = request.form['score']

            if not quizid == '' and not studentid == '' and not score == '':
                get_db().execute("INSERT INTO results (quizid, studentid, score) VALUES (?,?,?)", (quizid, studentid, score))
                get_db().commit()
                return redirect(url_for('dashboard'))
            else:
                return render_template('create_quiz_result.html', error='t')
        else:
            cur = get_db().execute("SELECT * FROM students")
            students = cur.fetchall()
            cur = get_db().execute("SELECT * FROM quiz GROUP BY subject")
            quizs = cur.fetchall()
            return render_template('create_quiz_result.html', error='f', students=students, quizs=quizs)

@app.route('/delete_student/<id>', methods=['GET'])
def delete_student(id):
    if not session.get('logged_in'):
        return render_template('login.html', error='f')
    else:
        if request.method == 'GET':
            student = id

            if not student == '':
                get_db().execute("DELETE FROM students  WHERE id='%s'" % student)
                get_db().commit()
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('dashboard'))


@app.route('/delete_quiz/<id>', methods=['GET'])
def delete_quiz(id):
    if not session.get('logged_in'):
        return render_template('login.html', error='f')
    else:
        if request.method == 'GET':
            quiz = id

            if not quiz == '':
                get_db().execute("DELETE FROM quiz  WHERE id='%s'" % quiz)
                get_db().commit()
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('dashboard'))


@app.route('/delete_result/<id>', methods=['GET'])
def delete_result(id):
    if not session.get('logged_in'):
        return render_template('login.html', error='f')
    else:
        if request.method == 'GET':
            result = id

            if not result == '':
                get_db().execute("DELETE FROM results  WHERE id='%s'" % result)
                get_db().commit()
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('dashboard'))



if __name__ == '__main__':
    app.run()