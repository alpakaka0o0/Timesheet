from flask import Flask, jsonify, request, send_file
from models import db, Employee, Pay, Timesheet, Image, Timecheck
from resources import payroll_ns, upload_ns, modi_ns
from flask_restx import Api, Resource, Namespace
from flask_cors import CORS
import os


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

@app.route('/users')
def users():
    #users 데이터를 Json 형식으로 반환한다.
    return {"members": [{"id" : 1, "name" : "jihyun"},
                        {"id" : 2, "name" : "jerry"}]}


if __name__ == '__main__':
    app.run(debug=True)