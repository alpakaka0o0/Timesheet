from flask import Flask, jsonify, request, send_file
from flask_restx import Api, Resource
from flask_migrate import Migrate
from sqlalchemy import text

from models import db, Employee, Pay, Timesheet, Image, Timecheck
from resources import payroll_ns, upload_ns, modi_ns
from flask_restx import Api, Resource, Namespace
from flask_cors import CORS
import os

import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
CORS(app)
app.config.from_pyfile('config.py')
db.init_app(app)

api = Api(app, version='1.0', title='Timesheet API', description='Timesheet API', doc='/api-docs')
api.add_namespace(payroll_ns)
api.add_namespace(upload_ns)
api.add_namespace(modi_ns)

with app.app_context():
    db.create_all()

base_url = "http://development.localhost:8000"
api_key = "339b44c46940c17"
api_secret = "8c594aad84a012f"
token = f'{api_key}:{api_secret}'

@app.route('/users')
def users():
    #users 데이터를 Json 형식으로 반환한다.
    return {"members": [{"id" : 1, "name" : "jihyun"},
                        {"id" : 2, "name" : "jerry"}]}

@app.route('/api/checkin_test', methods = ['Get'])
def checkin_test():
    frappe_checkin(1, "2024-09-01 00:00", "2024-09-01 12:00", "2024-09-01 16:00")
    return "goooooood"

@app.route('/api/frappe_checkin', methods=['Get'])
def frappe_checkin(timesheet_id, date, in_time, out_time, late_entry = False, early_exit = False):
    url = 'http://development.localhost:8000/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field'
    
    headers = {
       'Authorization': 'token ecd3425cf79376d:f18b18b4ef03781'
    }
    db_param = {
        "timesheet_id": timesheet_id,
        "date": date,
        "in_time": in_time,
        "out_time" : out_time,
        "late_entry" : late_entry, # boolean
        "early_exit" : early_exit # boolean
    }

    # # Log information about the incoming request
    # print(f"Connection from {request.remote_addr}")

    response = requests.get(url, headers=headers, params=db_param)
    print(response.text)

    if response.status_code == 200:
        return response
    else:
        return f"Error: {response.status_code}"
    
@app.route('/api/attendance_test', methods = ['Get'])
def attendance_test():
    response = attendance("2024-01-09", "Present", "HR-EMP-00001")
    return response
    
@app.route('/api/frappe_attendance', methods=['Get'])
def attendance(attendance_date, status, employee_id, late_entry = None,early_exit=None):
    url = 'http://development.localhost:8000/api/metahod/hrms.hr.doctype.attendance.attendance.mark_attendance'    
    headers = {
       'Authorization': 'token ecd3425cf79376d:f18b18b4ef03781'
    }

    
    db_param = {
        "attendance_date" : attendance_date,
        "status" : status,
        "employee" : employee_id,
        "late_entry" : late_entry,
        "early_exit" : early_exit
    }
    # # Log information about the incoming request
    # print(f"Connection from {request.remote_addr}")

    response = requests.post(url, headers=headers, params=db_param)
    print(response.text, response.status_code)

    if response.status_code == 200:
        return response
    else:
        return f"Error: {response.status_code}"
    


def payroll(timesheet, hourly_pay):
    
    weekly_work_hours = 0.0
    weekly_work_payment = 0.0

    week_starting_date = timesheet.week_starting_date

    base_pay = hourly_pay # 기본 시급
    evening_rate = 1.5  # 오후 6시부터 10시까지의 급여 요율
    night_rate = 2.0  # 오후 10시부터 오전 4시까지의 급여 요율

    sql_query = text("""
        SELECT 
            date,
            total_work_hours,
            CASE 
                WHEN total_work_hours <= 8 THEN total_work_hours * :base_pay
                WHEN total_work_hours > 8 AND max_out_time <= '2024-01-01 18:00:00' THEN (8 * :base_pay) + ((total_work_hours - 8) * :evening_pay)
                WHEN total_work_hours > 8 AND max_out_time > '2024-01-01 18:00:00' AND max_out_time <= '2024-01-01 22:00:00' THEN (8 * :base_pay) + ((total_work_hours - 8) * :evening_pay)
                WHEN total_work_hours > 8 AND (max_out_time > '2024-01-01 22:00:00' OR min_in_time < '2024-01-01 04:00:00') THEN (8 * :base_pay) + ((total_work_hours - 8) * :night_pay)
                ELSE total_work_hours * :base_pay
            END AS daily_wage,
            LEAST(total_work_hours, 8) AS regular_work_hours,
            GREATEST(total_work_hours - 8, 0) AS overtime_hours
        FROM (
            SELECT 
                date,
                SUM(TIMESTAMPDIFF(HOUR, in_time, out_time)) AS total_work_hours,
                MAX(out_time) AS max_out_time,
                MIN(in_time) AS min_in_time
            FROM 
                timecheck
            WHERE 
                timesheet_id = :timesheet_id AND
                date BETWEEN :week_starting_date AND DATE_ADD(:week_starting_date, INTERVAL 6 DAY)
            GROUP BY 
                date
        ) AS daily_work_hours
        ORDER BY 
            date;   
    """)

    # 쿼리 매개변수 설정
    params = {
        'base_pay': base_pay,
        'evening_pay': base_pay * evening_rate,
        'night_pay': base_pay * night_rate,
        'timesheet_id': 1,  # 예시로 1을 사용
        'week_starting_date' : week_starting_date
    }

    result = db.session.execute(sql_query, params)
    rows = result.fetchall()
    for row in rows:
        '''
        row[0] = date
        row[1] = total_work_hours
        row[2] = daily_wage
        row[3] = regular_work_hours
        row[4] = overtime_hours
        '''
        temp_work_hours = 45 - weekly_work_hours
        if 8 >= temp_work_hours >=0:
            row[2] += base_pay * 0.5 * (float(row[3]) - temp_work_hours)
        elif temp_work_hours <= 0:
            row[2] += base_pay * 0.5 * float(row[3])
        weekly_work_hours += float(row[1])
        get_date = str(row[0].year) +"-" + str(row[0].month) 
        weekly_work_payment += float(row[2])

        get_pay = Pay.query.filter_by(employee_id = timesheet.employee_id, date = get_date).first()

        if get_pay:
            get_pay.total_hour += weekly_work_hours
            get_pay.total_pay += weekly_work_payment
            db.session.commit()
        else:
            db.session.add(Pay(date = get_date, employee_id = timesheet.employee_id, total_hour = weekly_work_hours, total_pay = weekly_work_payment))
            db.session.commit()

@app.route('/api/employee_list', methods=['GET'])
def get_employee_list():
    token = f'{api_key}:{api_secret}'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/json'
    }
    url = f'{base_url}/api/resource/Employee' 
    response = requests.get(url, headers=headers)
    print("response: ", response.json())
    get_data = response.json()["data"]
    db.session.commit()
    
    for i in range(len(get_data)): # get employee's erpNext Id
        url = f'{base_url}/api/resource/Employee/{get_data[i]["name"]}' 
        get_employee = Employee.query.filter_by(employee_id=get_data[i]["name"]).first()
        if get_employee:
            continue
        response = requests.get(url, headers=headers)
        employee_info = response.json()["data"]
        db.session.add(Employee(employee_id = employee_info["employee"], first_name = employee_info["first_name"]))
        db.session.commit()

    if response.status_code == 200:
        return response.json()
    else:
        return None
 
if __name__ == '__main__':
    app.run(debug = True)

