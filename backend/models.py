from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Column

db = SQLAlchemy()

class Image(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    imglink = Column(String(500), unique=True, nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow)
    
class Manager(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow)


class Employee(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    managerId = Column(Integer,nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow)

class Timesheet(db.Model):
    id = Column(Integer, primary_key=True)
    employeeId = Column(Integer,nullable=False)
    date = Column(DateTime)
    timeIn1 = Column(DateTime)
    timeOut1 = Column(DateTime)
    timeIn2 = Column(DateTime)
    timeOut2 = Column(DateTime)
    perPayHour = Column(Integer, nullable=False)
    overTimePay = Column(Integer, nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Pay(db.Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    employeeId = Column(Integer,nullable=False)
    totalHour = Column(Integer, nullable=False)
    totalPay= Column(Integer, nullable=False)
    created_at = Column(DateTime, default = datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
