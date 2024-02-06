from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Boolean, Time

db = SQLAlchemy()

class Image(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    imglink = Column(String(500), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Employee(db.Model):
    id = Column(Integer, primary_key=True)
    employee_id = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Timesheet(db.Model):
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    week_starting_date = Column(DateTime, nullable=False)
    pay_per_hour = Column(Integer, nullable=False)
    over_time_pay = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Timecheck(db.Model):
    id = Column(Integer, primary_key=True)
    timesheet_id = Column(Integer, ForeignKey('timesheet.id'), nullable=False)
    date = Column(DateTime)
    in_time = Column(DateTime)
    out_time = Column(DateTime)
    late_entry = Column(Boolean, nullable=False)
    early_exit = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Pay(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    total_hour = Column(Integer, nullable=False)
    total_pay = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
