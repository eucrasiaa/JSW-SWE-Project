 -- create the sqlite db file:
 -- tables:
  -- course:
  -- courseID (pk), shortName, longName, subject name, 
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
 -- days Just a string of 7 characters, each being 0 or 1, representing the days of the week (e.g., "1010100" for Monday, Wednesday, and Friday)

-- student:
-- studentID (pk), firstName, lastName
CREATE TABLE student (
  studentID INTEGER PRIMARY KEY,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL
);
-- studentSchedule (studentID (fk), secNum (fk))
CREATE TABLE studentSchedule (
  studentID INTEGER NOT NULL,
  secNum INTEGER NOT NULL,
  PRIMARY KEY (studentID, secNum),
  FOREIGN KEY (studentID) REFERENCES student(studentID),
  FOREIGN KEY (secNum) REFERENCES course_sec(secNum)
);



