from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Boolean, Time

db = SQLAlchemy()


class Image(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    imglink = Column(String(500), unique=True, nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow)
    
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    week_starting_date = db.Column(db.DateTime, nullable=False)
    pay_per_hour = db.Column(db.Integer, nullable=False)
    over_time_pay = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Timecheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timesheet_id = db.Column(db.Integer, db.ForeignKey('timesheet.id'), nullable=False)
    date = db.Column(db.DateTime)
    in_time = db.Column(db.DateTime)
    out_time = db.Column(db.DateTime)
    late_entry = db.Column(db.Boolean, nullable=False)
    early_exit = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Pay(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    employee_id = Column(String(255), ForeignKey(Employee.employee_id),nullable=False)
    total_hour = Column(Integer, nullable=False)
    total_pay= Column(Integer, nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
