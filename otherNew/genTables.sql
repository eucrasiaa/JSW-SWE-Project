CREATE TABLE tutor (
  student_ID TEXT PRIMARY KEY NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  preferred_name TEXT NOT NULL 
);

CREATE TABLE course (
  course_code TEXT PRIMARY KEY NOT NULL,
  department TEXT NOT NULL,
  course_number TEXT NOT NULL,
  long_title TEXT NOT NULL
);

CREATE TABLE weekly_shift (
  shift_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  tutor_ID TEXT NOT NULL,
  day_of_week TEXT NOT NULL,
  start_time TEXT NOT NULL,
  end_time TEXT NOT NULL,
  FOREIGN KEY (tutor_ID) REFERENCES tutor (student_ID) ON DELETE CASCADE
);

CREATE TABLE shift_course_junct (
  shift_id INTEGER NOT NULL,
  course_code TEXT NOT NULL,
  PRIMARY KEY (shift_id, course_code), 
  FOREIGN KEY (shift_id) REFERENCES weekly_shift (shift_id) ON DELETE CASCADE,
  FOREIGN KEY (course_code) REFERENCES course (course_code) ON DELETE CASCADE
);

CREATE TABLE exceptions (
  exception_id INTEGER PRIMARY KEY AUTOINCREMENT,
  shift_id INTEGER NOT NULL,
  target_date TEXT,
  status TEXT,
  start_time TEXT,
  end_time TEXT,
  FOREIGN KEY (shift_id) REFERENCES weekly_shift (shift_id) ON DELETE CASCADE
);
