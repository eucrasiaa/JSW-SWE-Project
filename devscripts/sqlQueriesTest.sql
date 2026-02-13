
-- CREATE TABLE course (
  --   courseID INTEGER PRIMARY KEY,
  --   subjectName VARCHAR(5) NOT NULL,
  --   shortName TEXT NOT NULL,
  --   longName TEXT NOT NULL
  -- );
-- CREATE TABLE course_sec (
  --   secNum INTEGER PRIMARY KEY,
  --   courseID INTEGER NOT NULL,
  --   startTime TEXT NOT NULL,
  --   timeDuration INTEGER NOT NULL,
  --   days TEXT NOT NULL,
  --   FOREIGN KEY (courseID) REFERENCES course(courseID)
  -- );
-- CREATE TABLE tutor (
  --   tutorID INTEGER PRIMARY KEY,
  --   firstName TEXT NOT NULL,
  --   lastName TEXT NOT NULL
  -- );
-- CREATE TABLE tutor_block (
  --   blockID INTEGER PRIMARY KEY,
  --   tutorID INTEGER NOT NULL,
  --   courseID INTEGER,
  --   dayOfWeek TEXT NOT NULL,
  --   startTime TEXT NOT NULL,
  --   timeDuration INTEGER NOT NULL,
  --   FOREIGN KEY (tutorID) REFERENCES tutor(tutorID)
  --   FOREIGN KEY (courseID) REFERENCES course(courseID)
  -- );
--  -- days Just a string of 7 characters, each being 0 or 1, representing the days of the week (e.g., "1010100" for Monday, Wednesday, and Friday)
--
-- CREATE TABLE student (
  --   studentID INTEGER PRIMARY KEY,
  --   firstName TEXT NOT NULL,
  --   lastName TEXT NOT NULL
  -- );
-- CREATE TABLE studentSchedule (
  --   studentID INTEGER NOT NULL,
  --   secNum INTEGER NOT NULL,
  --   PRIMARY KEY (studentID, secNum),
  --   FOREIGN KEY (studentID) REFERENCES student(studentID),
  --   FOREIGN KEY (secNum) REFERENCES course_sec(secNum)
  -- );
--
-- basic visualization of data:
--

.mode column
.headers on

-- 1: List students with their schedules
--dont create the view if it already exists

-- DROP VIEW IF EXISTS student_schedules;
CREATE VIEW IF NOT EXISTS student_schedules AS
  SELECT s.studentID, s.firstName, s.lastName,
  c.shortName AS courseShortName,
  cs.startTime AS sectionStartTime,
  cs.timeDuration AS sectionDuration,
  cs.days AS sectionDays,
  cs.courseID AS courseID
  FROM student s
  JOIN studentSchedule ss ON s.studentID = ss.studentID
  JOIN course_sec cs ON ss.secNum = cs.secNum
  JOIN course c ON cs.courseID = c.courseID;

SELECT * FROM student_schedules
  ORDER BY studentID;

SELECT * FROM student_schedules
  WHERE studentID = 1;

  -- DROP VIEW IF EXISTS tutor_blocks;
 -- 2: List tutors with their available blocks 
CREATE VIEW IF NOT EXISTS tutor_blocks AS
  SELECT t.tutorID, t.firstName, t.lastName,
  c.shortName AS courseShortName,
  tb.startTime AS blockStartTime,
  tb.timeDuration AS blockDuration,
  tb.dayOfWeek AS blockDayOfWeek,
  tb.courseID AS courseID
  FROM tutor t
  JOIN tutor_block tb ON t.tutorID = tb.tutorID
  LEFT JOIN course c ON tb.courseID = c.courseID;

SELECT * FROM tutor_blocks
  ORDER BY tutorID;

-- 3: List names and IDS of students to populate dropdown 
CREATE VIEW IF NOT EXISTS student_list AS
  SELECT studentID, firstName || ' ' || lastName AS fullName
  FROM student;
SELECT * FROM student_list
  ORDER BY studentID;
-- 4: List names and IDs of tutors to populate dropdown
CREATE VIEW IF NOT EXISTS tutor_list AS
  SELECT tutorID, firstName || ' ' || lastName AS fullName
  FROM tutor;
SELECT * FROM tutor_list
  ORDER BY tutorID;

-- are views saved permanently?
-- yes, they are saved permanently until dropped

