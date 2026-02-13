# variety of functions to aid in querying the database
import sqlite3
DB_NAME = 'schedule.db'
import random


"""
CREATE TABLE course (
  courseID INTEGER PRIMARY KEY,
  subjectName VARCHAR(5) NOT NULL,
  shortName TEXT NOT NULL,
  longName TEXT NOT NULL
);
CREATE TABLE course_sec (
  secNum INTEGER PRIMARY KEY,
  courseID INTEGER NOT NULL,
  startTime TEXT NOT NULL,
  timeDuration INTEGER NOT NULL,
  days TEXT NOT NULL,
  FOREIGN KEY (courseID) REFERENCES course(courseID)
);
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


CREATE VIEW IF NOT EXISTS student_schedules AS
  SELECT s.studentID, s.firstName, s.lastName,
  c.shortName AS courseShortName,
  cs.secNum AS sectionNumber,
  cs.startTime AS sectionStartTime,
  cs.timeDuration AS sectionDuration,
  cs.days AS sectionDays
  FROM student s
  JOIN studentSchedule ss ON s.studentID = ss.studentID
  JOIN course_sec cs ON ss.secNum = cs.secNum
  JOIN course c ON cs.courseID = c.courseID;

CREATE VIEW IF NOT EXISTS tutor_blocks AS
  SELECT t.tutorID, t.firstName, t.lastName,
  c.shortName AS courseShortName,
  tb.dayOfWeek AS blockDayOfWeek,
  tb.startTime AS blockStartTime,
  tb.timeDuration AS blockDuration
  FROM tutor t
  JOIN tutor_block tb ON t.tutorID = tb.tutorID
  LEFT JOIN course c ON tb.courseID = c.courseID;

CREATE VIEW IF NOT EXISTS student_list AS
  SELECT studentID, firstName || ' ' || lastName AS fullName
  FROM student;
SELECT * FROM student_list
  ORDER BY studentID;


CREATE VIEW IF NOT EXISTS tutor_list AS
  SELECT tutorID, firstName || ' ' || lastName AS fullName
  FROM tutor;
SELECT * FROM tutor_list
  ORDER BY tutorID;
"""

# dropdown helpers:
def pull_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT studentID, firstName || " " || lastName AS fullName FROM student')
    students = cursor.fetchall()
    conn.close()
    return students

def pull_tutors():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT tutorID, firstName || " " || lastName AS fullName FROM tutor')
    tutors = cursor.fetchall()
    conn.close()
    return tutors
