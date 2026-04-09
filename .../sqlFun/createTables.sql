-- The core shift block
CREATE TABLE shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tutor_name TEXT NOT NULL,
    day_of_week TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    status TEXT DEFAULT 'Scheduled' -- 'Scheduled', 'Checked In', 'Late', 'Cancelled'
);

-- The courses tied to that shift
CREATE TABLE shift_courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    shift_id INTEGER NOT NULL,
    course_name TEXT NOT NULL,
    FOREIGN KEY(shift_id) REFERENCES shifts(id) ON DELETE CASCADE
);

CREATE TABLE tutor (
  tutorID INTEGER PRIMARY KEY,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL,
  perfName TEXT
)



