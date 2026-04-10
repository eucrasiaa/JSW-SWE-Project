import json

# fixes the single quote thing. 
def fix_quotes(s):
    if not s:
        return ''
    return str(s).replace("'", "''")

def go():
    print("json read.....")
    
    with open('courseInfo.json', 'r', encoding='utf-8') as f:
        data1 = json.load(f)
    with open('UpdatedTutorSchedule.json', 'r', encoding='utf-8') as f:
        data2 = json.load(f)
    out = "-- ==========================================\n"
    out += "-- WILLS AWESOME GENERATOR FROM JSON FILES YAYAYAYAY\n"
    out += "-- ==========================================\n\n"

    out += "-- \n"
    for item in data1:
        c_code = f"{item['Dept']} {item['CourseNumber']}"
        name = fix_quotes(item.get('LongTitle', ''))
        out += (f"INSERT OR IGNORE INTO course (course_code, department, course_number, long_title) "
                f"VALUES ('{c_code}', '{item['Dept']}', '{item['CourseNumber']}', '{name}');\n")
    out += "\n"

    out += "-- tutor section\n"
    # validate we don't have duplicates
    people = sorted(list({t['Tutor'] for t in data2}))
    for p in people:
        id_tag = f"ID_{p.upper()}"
        out += (f"INSERT OR IGNORE INTO tutor (student_ID, first_name, last_name, preferred_name) "
                f"VALUES ('{id_tag}', '{p}', 'TBD', '{p}');\n")
    out += "\n"

    out += "-- shifts and the middle table thingy\n"
    s_id = 1 

    for node in data2:
        t_id = f"ID_{node['Tutor'].upper()}"

        for s in node['Schedule']:
            # the main shift
            out += (f"INSERT INTO weekly_shift (shift_id, tutor_ID, day_of_week, start_time, end_time) "
                    f"VALUES ({s_id}, '{t_id}', '{s['Day']}', '{s['StartTime']}', '{s['EndTime']}');\n")
            # linking courses to shifts
            for code in s['Courses']:
                out += (f"INSERT INTO shift_course_junct (shift_id, course_code) "
                        f"VALUES ({s_id}, '{code}');\n")
            
            s_id += 1
        out += "\n"
    # dump it all into file
    with open('populate_database.sql', 'w', encoding='utf-8') as f:
        f.write(out)
        
    print("done! check populate_database.sql")

if __name__ == "__main__":
    go()
