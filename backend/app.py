from flask import Flask
from flask_restx import Api, Resource
import requests

from models import db, Employee, Pay, Timesheet, Image, Timecheck

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def users():
    #users 데이터를 Json 형식으로 반환한다.
    return {"members": [{"id" : 1, "name" : "jihyun"},
                        {"id" : 2, "name" : "jerry"}]}

@app.route('/checkin', methods=['GET'])
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


if __name__ == "__main__":
    app.run(debug = True)

