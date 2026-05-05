import sqlite3
import json
from datetime import datetime
from flask import Flask, render_template, request, Response, jsonify
from gevent.queue import Queue


######################
### IMPORTANT NOTE: LOTS OF QUERIES ARE FIXED TIMES+DATES, ENSURE THEY ARE DYNAMIC ON REAL SYSTEM!!
######################
app = Flask(__name__)

# ok we'll pass upates via server side events, we have probably not heacvy user traffic so its less insane than a websocket ig?

# --- IN-MEMORY STATE ---
# store live status of shifts (e.g., {"1": "Arrived", "3": "Late"})
# default = Scheduled
live_statuses = {} 

# connect list. b/c. heh,
clients = []

# --- DATABASE HELPER ---
def get_db_connection():
    conn = sqlite3.connect('tutoring.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_todays_shifts_OLD():
    # would use datetime.now().strftime('%A')
    day_of_week = 'Monday' 
    # day_of_week = datetime.now().strftime('%A')


    conn = get_db_connection()
    shifts = conn.execute(
        "SELECT * FROM vw_base_weekly_schedule WHERE day_of_week = ?", 
        (day_of_week,)
    ).fetchall()
    conn.close()

    result = []
    for shift in shifts:
        s = dict(shift)
        status = live_statuses.get(str(s['shift_id']), 'Scheduled')
        result.append({
            'shift_id': s['shift_id'],
            'tutor': s['tutor_name'],
            'start': s['start_time'],
            'end': s['end_time'],
            'courses': s['courses_taught'],
            'status': status
        })
    return result

def get_todays_shifts(target_date=None):
    # rewrite + debug date handling!
    now = datetime.now()

    if not target_date:
        target_date = now.strftime('%Y-%m-%d')
    # convert to day of week text
    day_of_week = datetime.strptime(target_date, '%Y-%m-%d').strftime('%A')

    conn = get_db_connection()
    # join with exceptions that exist on THIS specific date (so that current schedule can still rerfer to just day_of_week
    # not just dat!e!!!!!)
    query = '''
        SELECT 
            s.*, 
            e.status AS exception_status
        FROM vw_base_weekly_schedule s
        LEFT JOIN exceptions e ON s.shift_id = e.shift_id AND e.target_date = ?
        WHERE s.day_of_week = ?
    '''
    shifts = conn.execute(query, (target_date, day_of_week)).fetchall()
    conn.close()

    result = []
    for shift in shifts:
        s = dict(shift)        
        db_status = s.get('exception_status')
        live_status = live_statuses.get(str(s['shift_id']))
        
        final_status = db_status if db_status else (live_status if live_status else 'Scheduled')

        result.append({
            'shift_id': s['shift_id'],
            'tutor': s['tutor_name'],
            'start': s['start_time'],
            'end': s['end_time'],
            'courses': s['courses_taught'],
            'status': final_status
        })
    return result


def insert_cancelation(session_id):
    conn = get_db_connection()
    shifts = conn.execute(
        'SELECT shift_id FROM weekly_shift WHERE session_id = ?', 
        (session_id,)
    ).fetchall()
    for shift in shifts:
        conn.execute(
            '''INSERT INTO exceptions (shift_id, target_date, status) 
               VALUES (?, ?, ?)''',
            (shift['shift_id'], target_date, 'canceled')
        )
    
    conn.commit()
    conn.close()
#
# @app.route('/api/shifts')
# def get_shifts_by_date():
#     target_date = request.args.get('date')
#     conn = get_db_connection()
#
#     query = '''
#         SELECT 
#             s.shift_id, 
#             s.start_time, 
#             s.end_time, 
#             s.tutor_name, 
#             s.courses_taught,
#             e.status AS exception_status
#         FROM vw_base_weekly_schedule s
#         LEFT JOIN exceptions e ON s.shift_id = e.shift_id 
#         WHERE day_of_week = ? 
#     '''
#     shifts = conn.execute(query, (target_date,)).fetchall()
#     conn.close()
#     result = []
#     for shift in shifts:
#         s = dict(shift)
#         result.append({
#             'shift_id': s['shift_id'],
#             'tutor': s['tutor_name'],
#             'start': s['start_time'],
#             'end': s['end_time'],
#             'courses': s['courses_taught'],
#         })
#     return result
 
# slopppp
@app.route('/api/exceptions/all')
def get_all_exceptions():
    conn = get_db_connection()
    exceptions = conn.execute('SELECT * FROM vw_resolved_exceptions ORDER BY target_date DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in exceptions])

def notify_clients():
    data = get_todays_shifts()
    for q in clients:
        q.put(data)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nav')
def nav():
    return render_template('nav.html')

@app.route('/rw')
def rw():
    return render_template('htmlrework.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/staff-cancel')
def staff_cancel():
    return render_template('staff-cancel.html')

@app.route('/api/shifts/today')
def api_shifts_today():
    return jsonify(get_todays_shifts())


@app.route('/api/get_live_status')
def get_statuses():
    return jsonify(live_statuses);


@app.route('/api/update_live_status', methods=['POST'])
def update_status():
    data = request.json
    shift_id = str(data.get('shift_id'))
    new_status = data.get('status')
    live_statuses[shift_id] = new_status
    notify_clients()
    
    return jsonify({"success": True})

#@app.route('/api/stream_statuses')
def stream_statusesOLD():
    def event_stream():
        q = Queue()
        clients.append(q)
        try:
            yield f"data: {json.dumps(get_todays_shifts())}\n\n"
            while True:
                data = q.get()
                yield f"data: {json.dumps(data)}\n\n"
        except GeneratorExit:
            clients.remove(q)

    return Response(event_stream(), mimetype="text/event-stream")
# rewrite to proper handle cancelations
@app.route('/api/stream_statuses')
def stream_statuses():
    target_date = request.args.get('date')

    def event_stream(date_filter):
        q = Queue()
        clients.append(q)
        try:
            yield f"data: {json.dumps(get_todays_shifts(date_filter))}\n\n"
            while True:
                # only refrsh data for n date being watched (WIP??)
                q.get() 
                data = get_todays_shifts(date_filter)
                yield f"data: {json.dumps(data)}\n\n"
        except GeneratorExit:
            clients.remove(q)

    return Response(event_stream(target_date), mimetype="text/event-stream")

@app.route('/api/shifts')
def get_shifts_by_date():
    # yyyy-mm-dd
    target_date = request.args.get('date') 
    # Monday, Tuesday, etc
    day_name = request.args.get('day') 

    conn = get_db_connection()
    # join the base schedule with exceptions only for that specific date
    query = '''
        SELECT 
            s.shift_id, 
            s.start_time, 
            s.end_time, 
            s.tutor_name, 
            s.courses_taught,
            e.status AS exception_status
        FROM vw_base_weekly_schedule s
        LEFT JOIN exceptions e ON s.shift_id = e.shift_id AND e.target_date = ?
        WHERE s.day_of_week = ? 
    '''
    shifts = conn.execute(query, (target_date, day_name)).fetchall()
    conn.close()
    
    return jsonify([dict(s) for s in shifts])

# for populating history
# ?id=#
@app.route('/api/by_shift_id')
def get_by_shift_id():
        targetid = request.args.get('id')
        conn = get_db_connection()
        query='''
        SELECT * FROM weekly_shift JOIN tutor on tutor.student_id = tutor_ID WHERE shift_id = ?
        '''
        shift_by_id = conn.execute(query, targetid).fetchall()
        conn.close()
        return jsonify([dict(s) for s in shift_by_id])
@app.route('/api/batch_update_exceptions', methods=['POST'])
def batch_update_exceptions():
    data = request.json
    target_date = data.get('date')
    updates = data.get('updates')
    conn = get_db_connection()
    try:
        for shift_id, status in updates.items():
            if status == 'canceled':
                # overwrite!!!! this was so fussy....
                conn.execute('''
                    INSERT INTO exceptions (shift_id, target_date, status) 
                    VALUES (?, ?, ?)
                    ON CONFLICT(shift_id, target_date) DO UPDATE SET status='canceled'
                ''', (shift_id, target_date, 'canceled'))
            else:
                # setting to "active" just deleted the cancel/exception
                conn.execute('''
                    DELETE FROM exceptions 
                    WHERE shift_id = ? AND target_date = ?
                ''', (shift_id, target_date))
        
        conn.commit()
        notify_clients()  #  push updates.. just incase
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    # idek brah something weird thrown here but. TODO :??
    app.run(port=4413, debug=True)
