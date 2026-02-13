from flask import Flask, jsonify
import sqlite3
app = Flask(__name__)
DB_NAME = 'schedule.db'
# import queryHelper.py localfile 

from queryHelper import *

# if we wish to queries to the api, we can use the following code to fetch data from the database and return it as JSON:
# example, /api/data?classID=# to fetch data for a specific classID
# this is implemented with:

@app.route('/api/class/<int:classID>')
def get_data_by_classID(classID):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if classID:
        cursor.execute('SELECT * FROM course WHERE courseID = ?', (classID,))
    else:
        cursor.execute('SELECT * FROM course')

    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

"""
CREATE TABLE course (
  courseID INTEGER PRIMARY KEY,
  subjectName VARCHAR(5) NOT NULL,
  shortName TEXT NOT NULL,
  longName TEXT NOT NULL
);

  -- course_sec
  -- secNum (pk), courseID (fk),  startTime, timeDuration, days (bitfield /mask?)
CREATE TABLE course_sec (
  secNum INTEGER PRIMARY KEY,
  courseID INTEGER NOT NULL,
  startTime TEXT NOT NULL,
  timeDuration INTEGER NOT NULL,
  days TEXT NOT NULL,
  FOREIGN KEY (courseID) REFERENCES course(courseID)
);
-- tutor: 
-- tutorID (pk), firstName, lastName
 
-- tutor_block:
-- blockID (pk), tutorID (fk), dayOfWeek, startTime, timeDuration
CREATE TABLE tutor (
  tutorID INTEGER PRIMARY KEY,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL
);
CREATE TABLE tutor_block (
  blockID INTEGER PRIMARY KEY,
  tutorID INTEGER NOT NULL,
  courseID INTEGER,
  dayOfWeek TEXT NOT NULL,
  startTime TEXT NOT NULL,
  timeDuration INTEGER NOT NULL,
  FOREIGN KEY (tutorID) REFERENCES tutor(tutorID)
  FOREIGN KEY (courseID) REFERENCES course(courseID)
);
"""
# join course_sec and course to get the course name for each section
@app.route('/api/sections')
def get_sections():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT course_sec.secNum, course.shortName, course_sec.startTime, course_sec.timeDuration, course_sec.days
        FROM course_sec
        JOIN course ON course_sec.courseID = course.courseID
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)
# join tutor_block and tutor to get the tutor name for each block 
@app.route('/api/tutor_blocks')
def get_tutor_blocks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tutor_block.blockID, tutor.firstName || ' ' || tutor.lastName AS tutorName, tutor_block.courseID, tutor_block.dayOfWeek, tutor_block.startTime, tutor_block.timeDuration
        FROM tutor_block
        JOIN tutor ON tutor_block.tutorID = tutor.tutorID
    ''')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)


# optional id param for studentID
@app.route('/api/studentSchedules/<int:studentID>')
def get_student_schedules(studentID):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if studentID:
        cursor.execute('''
            SELECT * FROM student_schedules
            WHERE studentID = ?
        ''', (studentID,))
    else:
        cursor.execute('SELECT * FROM student_schedules')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/api/tutorsFor/<int:courseID>')
def get_tutors_for_course(courseID):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    #use tutor_blocks view 
    if courseID:
        cursor.execute('''
            SELECT * FROM tutor_blocks
            WHERE courseID = ?
        ''', (courseID,))
        
    else:
        cursor.execute('SELECT * FROM tutor_blocks')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/api/students')
def get_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # student names, IDs,
    cursor.execute('SELECT studentID, firstName || " " || lastName AS fullName FROM student')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/api/data')
def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)
# init 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    print("test")


