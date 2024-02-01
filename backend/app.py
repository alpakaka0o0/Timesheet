from flask import Flask, request
from flask_restx import Api, Resource
from flask_migrate import Migrate

from models import db, Employee, Pay, Timesheet, Image, Timecheck

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

import requests

base_url = "http://development.localhost:8000"
api_key = ""
api_secret = ""
token = f'{api_key}:{api_secret}'

@app.route('/')
def users():
    #users 데이터를 Json 형식으로 반환한다.
    return {"members": [{"id" : 1, "name" : "jihyun"},
                        {"id" : 2, "name" : "jerry"}]}

@app.route('/api/checkin', methods=['Post'])
def checkin():
    url = 'http://development.localhost:8000/api/method/hrms.api.get_all_employees'
    
    headers = {
       'Authorization': 'token ecd3425cf79376d:f18b18b4ef03781'
    }
    

    # # Log information about the incoming request
    # print(f"Connection from {request.remote_addr}")

    response = requests.get(url, headers=headers)
    print(response)

    if response.status_code == 200:
        return response
    else:
        return f"Error: {response.status_code}"
    
@app.route('/api/attendance', methods=['Get'])
def attendance():
    url = 'http://development.localhost:8000/api/method/hrms.hr.doctype.attendance.attendance.mark_attendance'
    
    headers = {
       'Authorization': 'token ecd3425cf79376d:f18b18b4ef03781'
    }
    
    param = {
        "attendance_date" : "2024-1-2",
        "status" : "Present",
        "employee" : "HR-EMP-00002"
    }
    # # Log information about the incoming request
    # print(f"Connection from {request.remote_addr}")

    response = requests.get(url, headers=headers)
    print(response)

    if response.status_code == 200:
        return response
    else:
        return f"Error: {response.status_code}"

@app.route('/api/employee_list', methods=['GET'])
def get_employee_list():
    token = f'{api_key}:{api_secret}'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/json'
    }
    url = f'{base_url}/api/resource/Employee' 
    response = requests.get(url, headers=headers)
    get_data = response.json()["data"]
    
    for i in range(len(get_data)): # get employee's erpNext Id
        if Employee.query.filter_by(employee_id = get_data[i]["name"]).first():
            continue
        url = f'{base_url}/api/resource/Employee/{get_data[i]["name"]}' 
        response = requests.get(url, headers=headers)
        employee_info = response.json()["data"]
        db.session.add(Employee(employee_id = employee_info["employee"], first_name = employee_info["first_name"], pay_per_hour = employee_info["ctc"]))
        db.session.commit()

    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == "__main__":
    app.run(debug = True)

