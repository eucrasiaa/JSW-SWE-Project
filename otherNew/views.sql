CREATE VIEW vw_base_weekly_schedule AS
SELECT 
    ws.shift_id,
    t.preferred_name AS tutor_name,
    ws.day_of_week,
    ws.start_time,
    ws.end_time,
    GROUP_CONCAT(sc.course_code, ', ') AS courses_taught
FROM weekly_shift ws
JOIN tutor t ON ws.tutor_ID = t.student_ID
LEFT JOIN shift_course_junct sc ON ws.shift_id = sc.shift_id
GROUP BY ws.shift_id;


CREATE VIEW vw_course_search AS
SELECT 
    c.course_code,
    c.long_title,
    ws.day_of_week,
    ws.start_time,
    ws.end_time,
    t.preferred_name AS tutor_name,
    ws.shift_id
FROM course c
JOIN shift_course_junct sc ON c.course_code = sc.course_code
JOIN weekly_shift ws ON sc.shift_id = ws.shift_id
JOIN tutor t ON ws.tutor_ID = t.student_ID;


-- SELECT * FROM vw_course_search WHERE course_code = 'BIOL 101' ORDER BY strftime('%w', day_of_week);

CREATE VIEW vw_resolved_exceptions AS
SELECT 
    e.exception_id,
    e.target_date,
    e.status,
    COALESCE(e.start_time, ws.start_time) AS effective_start_time,
    COALESCE(e.end_time, ws.end_time) AS effective_end_time,
    ws.day_of_week,
    t.preferred_name AS tutor_name,
    ws.shift_id
FROM exceptions e
JOIN weekly_shift ws ON e.shift_id = ws.shift_id
JOIN tutor t ON ws.tutor_ID = t.student_ID;

-- SELECT * FROM vw_resolved_exceptions WHERE target_date = '2026-04-13';
--handles nulls and proper joins 
