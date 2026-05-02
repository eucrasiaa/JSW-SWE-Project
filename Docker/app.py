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

def get_todays_shifts():
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

@app.route('/api/shifts')
def get_shifts_by_date():
    target_date = request.args.get('date')
    conn = get_db_connection()
    
    query = '''
        SELECT 
            s.shift_id, 
            s.start_time, 
            s.end_time, 
            s.tutor_name, 
            s.courses_taught,
            e.status AS exception_status
        FROM vw_base_weekly_schedule s
        LEFT JOIN exceptions e ON s.shift_id = e.shift_id 
        WHERE day_of_week = ? 
    '''
    shifts = conn.execute(query, (target_date,)).fetchall()
    conn.close()
    result = []
    for shift in shifts:
        s = dict(shift)
        result.append({
            'shift_id': s['shift_id'],
            'tutor': s['tutor_name'],
            'start': s['start_time'],
            'end': s['end_time'],
            'courses': s['courses_taught'],
        })
    return result
    

def notify_clients():
    data = get_todays_shifts()
    for q in clients:
        q.put(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/staff-cancel')
def staff_cancel():
    return render_template('staff-cancel.html')

@app.route('/api/shifts/today')
def api_shifts_today():
    return jsonify(get_todays_shifts())

@app.route('/api/update_live_status', methods=['POST'])
def update_status():
    data = request.json
    shift_id = str(data.get('shift_id'))
    new_status = data.get('status')
    live_statuses[shift_id] = new_status
    notify_clients()
    
    return jsonify({"success": True})

@app.route('/api/stream_statuses')
def stream_statuses():
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

if __name__ == '__main__':
    # idek brah something weird thrown here but. TODO :??
    app.run(port=4413, debug=True)
