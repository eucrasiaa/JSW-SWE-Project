"""
 -- create the sqlite db file:
 -- tables:
  -- course:
  -- courseID (pk), shortName, longName
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
 -- days Just a string of 7 characters, each being 0 or 1, representing the days of the week (e.g., "1010100" for Monday, Wednesday, and Friday)

CREATE FUNCTION parseDays(days TEXT) RETURNS TEXT AS $$
DECLARE
  dayList TEXT := '';
BEGIN
  IF substr(days, 1, 1) = '1' THEN
    dayList := dayList || 'Monday ';
  END IF;
  IF substr(days, 2, 1) = '1' THEN
    dayList := dayList || 'Tuesday ';
  END IF;
  IF substr(days, 3, 1) = '1' THEN
    dayList := dayList || 'Wednesday ';
  END IF;
  IF substr(days, 4, 1) = '1' THEN
    dayList := dayList || 'Thursday ';
  END IF;
  IF substr(days, 5, 1) = '1' THEN
    dayList := dayList || 'Friday ';
  END IF;
  IF substr(days, 6, 1) = '1' THEN
    dayList := dayList || 'Saturday ';
  END IF;
  IF substr(days, 7, 1) = '1' THEN
    dayList := dayList || 'Sunday ';
  END IF;
  RETURN trim(dayList);
END;
$$ LANGUAGE plpgsql;

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

# create a sqlite db file and populate it with some sample data for testing
# (use ./createDB.sql to create db)
# this script will generate random sample data:
import sqlite3
import random
import string
import datetime
DB_NAME = 'schedule.db'

NameList = ["Emma", "Madison", "Emily", "Kaitlyn", "Hailey", "Olivia", "Isabella", "Hannah", "Sarah", "Abigail", "Sophia", "Kaylee", "Alyssa", "Madeline", "Brianna", "Jacob", "Aidan", "Ethan", "Ryan", "Matthew", "Michael", "Tyler", "Joshua", "Nicholas", "Connor", "Zachary", "Andrew", "Dylan", "Jack"]
LastNames = ["L.", "J.", "S.", "B.", "M.", "D.", "C.", "G.", "H.", "K.", "N.", "P.", "R.", "T.", "V."]

Classes = ["CMSC", "MATH", "PHYS", "CHEM", "BIO"]
    # "CMSC331 Principles of Programming Language",
    # "CMSC411  Computer Architecture",
    # "CMSC449  Malware Analysis",
    # "CMSC451  Automata Theory and Formal Languages",
    # "ART210 02-2599 Visual Concepts I",
    # "MATH221 01-4903 Introduction to Linear Algebra",
    # "MATH155 09-5592 Applied Calculus",
    # "IS300 09-2244 Management Information Systems",
    # "IS310 01-1283 Software and Hardware Concepts",
    # "IS451 01-1297 Network Design and Management",
    # "HIST327 01-6654 Modern Latin American History",
    # "IS436 05-7222 Structured Systems Analysis and Design",
    # "IS448 06-7221 Markup and Scripting Languages"
EXAMPLE_COURSES = [
    ("CMSC331", "Principles of Programming Language"),
    ("CMSC411", "Computer Architecture"),
    ("CMSC449", "Malware Analysis"),
    ("CMSC451", "Automata Theory and Formal Languages"),
    ("ART210", "Visual Concepts I"),
    ("MATH221", "Introduction to Linear Algebra"),
    ("MATH155", "Applied Calculus"),
    ("IS300", "Management Information Systems"),
    ("IS310", "Software and Hardware Concepts"),
    ("IS451", "Network Design and Management"),
    ("HIST327", "Modern Latin American History"),
    ("IS436", "Structured Systems Analysis and Design"),
    ("IS448", "Markup and Scripting Languages")
]

# give each course like 3 random sections, classes start on hour or :30, last 1:15 MW, MWF,or TTh 

def random_time():
    hour = random.randint(8, 18) 
    minute = random.choice([0, 30])  
    return f"{hour:02d}:{minute:02d}"
duration=75
def random_days():
    patterns = ["1010100", "1110000", "0101010"]  
    return random.choice(patterns)

def random_sections(courseID):
    sections = []
    for _ in range(random.randint(1, 3)):
        startTime = random_time()
        days = random_days()
        # sectionNum is just an auto-incrementing integer, so we can use None for that
        sections.append((None, courseID, startTime, duration, days))

    return sections

def addAllCourses(conn):
    cursor = conn.cursor()
    for shortName, longName in EXAMPLE_COURSES:
        subjectName = ''.join(filter(str.isalpha, shortName))
        cursor.execute('INSERT INTO course (subjectName, shortName, longName) VALUES (?, ?, ?)', (subjectName, shortName, longName))
        courseID = cursor.lastrowid
        sections = random_sections(courseID)
        cursor.executemany('INSERT INTO course_sec (secNum, courseID, startTime, timeDuration, days) VALUES (?, ?, ?, ?, ?)', sections)
    conn.commit()

# add some random tutors
def random_tutor():
    firstName = random.choice(NameList)
    lastName = random.choice(LastNames)
    return firstName, lastName


#tie a tutor in this script to a subject, and only generate their blocks for that subject, so we can test the matching algorithm later
def addAllTutors(conn):
    cursor = conn.cursor()
    for subject in Classes:
        for _ in range(5):  # 5 tutors per subject
            firstName, lastName = random_tutor()
            cursor.execute('INSERT INTO tutor (firstName, lastName) VALUES (?, ?)', (firstName, lastName))
            tutorID = cursor.lastrowid
            # generate random blocks for this tutor, only for courses in this subject
            cursor.execute('SELECT courseID FROM course WHERE subjectName = ?', (subject,))
            courseIDs = [row[0] for row in cursor.fetchall()]
            for courseID in courseIDs:
                for _ in range(random.randint(1, 3)):  # 1-3 blocks per course
                    dayOfWeek = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
                    startTime = random_time()
                    timeDuration = duration
                    cursor.execute('INSERT INTO tutor_block (tutorID, courseID, dayOfWeek, startTime, timeDuration) VALUES (?, ?, ?, ?, ?)', (tutorID, courseID, dayOfWeek, startTime, timeDuration))
    conn.commit()





#visualize the data in the database (for testing purposes)
def visualize_data(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM course JOIN course_sec ON course.courseID = course_sec.courseID')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # select (fancyName = firstName || ' ' || lastName, courseID, tutorblockID, timeStart), join tutor and tutor_block on tutorID, and join course_sec on courseID 

    cursor.execute('SELECT (firstName || " " || lastName) AS fancyName, tutor_block.courseID, blockID, tutor_block.startTime,  shortName FROM tutor JOIN tutor_block ON tutor.tutorID = tutor_block.tutorID JOIN course ON tutor_block.courseID = course.courseID')
    rows = cursor.fetchall()
    for row in rows:
        print(row)



def addNewStudent(conn, firstName, lastName):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO student (firstName, lastName) VALUES (?, ?)', (firstName, lastName))
    studentID = cursor.lastrowid
    return studentID
def addStudentsTest(conn):
    for _ in range(5):
        firstName, lastName = random_tutor()
        studentID = addNewStudent(conn, firstName, lastName)
        print(f"Added student {firstName} {lastName} with ID {studentID}")

# for each student, add 5 sections to enroll in. in cases of time conflicts, print the section and skip, then try again (limit 20 attempts or something to avoid infinite loop)

# CREATE TABLE studentSchedule (
#   studentID INTEGER NOT NULL,
#   secNum INTEGER NOT NULL,
#   PRIMARY KEY (studentID, secNum),
#   FOREIGN KEY (studentID) REFERENCES student(studentID),
#   FOREIGN KEY (secNum) REFERENCES course_sec(secNum)
# );
def enrollStudentInSections(conn, studentID):
        cursor = conn.cursor()
        # pick 5 existing sections, making sure:
        # 1. no duplicate courses
        # 2. no time conflicts (check day of weeks, time start, and time duration)
        student_sections = []
        cursor.execute('SELECT secNum, courseID, startTime, timeDuration, days FROM course_sec')
        sections = cursor.fetchall()
        random.shuffle(sections)
        #itis not shuffling
        print (f"Available sections for enrollment: {sections}")
        selected_sections = []
        selected_courseIDs = set()
        print(f"Enrolling student {studentID} in sections...")
        for secNum, courseID, startTime, timeDuration, days in sections:
            print(f"Trying to add section {secNum} of course {courseID} with start time {startTime} and days {days}")
            if courseID in selected_courseIDs:
                continue
            conflict = False
            # if student already in this course, skip
            if not conflict:
                selected_sections.append((secNum, courseID, startTime, timeDuration, days))
                selected_courseIDs.add(courseID)
            if len(selected_sections) >= 5:
                break
        if len(selected_sections) < 5:
            print("Could not find 5 non-conflicting sections for the student.")
        else:
            print(f"Enrolled student {studentID} in sections: {selected_sections}")
            for secNum, courseID, startTime, timeDuration, days in selected_sections:
                cursor.execute('INSERT INTO studentSchedule (studentID, secNum) VALUES (?, ?)', (studentID, secNum))
            conn.commit()


def aacreateStudent(conn):
    cursor = conn.cursor()
    firstName, lastName = random_tutor()
    cursor.execute('INSERT INTO student (firstName, lastName) VALUES (?, ?)', (firstName, lastName))
    studentID = cursor.lastrowid
    # pick 5 existing sections, making sure:
    # 1. no duplicate courses
    # 2. no time conflicts (check day of weeks, time start, and time duration)
    cursor.execute('SELECT secNum, courseID, startTime, timeDuration, days FROM course_sec')
    sections = cursor.fetchall()
    random.shuffle(sections)
    selected_sections = []
    selected_courseIDs = set()
    for secNum, courseID, startTime, timeDuration, days in sections:
        print(f"Trying to add section {secNum} of course {courseID} with start time {startTime} and days {days}")
        if courseID in selected_courseIDs:
            continue
        conflict = False
        for _, _, s_startTime, s_timeDuration, s_days in selected_sections:
            # check for time conflict
            if set(days) & set(s_days): 
                if checkTimeConflict((None, None, startTime, timeDuration, days), (None, None, s_startTime, s_timeDuration, s_days)):
                    conflict = True
                    break
        if not conflict:
            selected_sections.append((secNum, courseID, startTime, timeDuration, days))
            selected_courseIDs.add(courseID)
        if len(selected_sections) >= 5:
            break

    if len(selected_sections) < 5:
        print("Could not find 5 non-conflicting sections for the student.")
    else:
        print(f"Created student {firstName} {lastName} with sections: {selected_sections}")


if __name__ == '__main__':
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # addAllCourses(conn)
    # addAllTutors(conn)
    addStudentsTest(conn)
    # enroll all student that exist:
    cursor.execute('SELECT studentID FROM student')
    studentIDs = [row[0] for row in cursor.fetchall()]
    print(f"Enrolling students with IDs: {studentIDs}")
    for studentID in studentIDs:
        enrollStudentInSections(conn, studentID)
    
    # visualize_data(conn)
    conn.close()
# if __name__ == '__main__':
#     conn = sqlite3.connect(DB_NAME)
#
#     visualize_data(conn)
#     conn.close()
