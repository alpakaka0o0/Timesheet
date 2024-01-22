from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Date, Time
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class Image(db.Model):
    id : Mapped[int] = mapped_column(primary_key = True)
    date: Mapped[Date]
    imglink: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(default=datetime.utcnow)
    
class Manager(db.Model):
    id : Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Employee(db.Model):
    id : Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable=False)
    managerId: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class Timesheet(db.Model):
    id : Mapped[int] = mapped_column(primary_key = True)
    employeeId: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    timeIn1: Mapped[datetime.time]
    timeOut1: Mapped[datetime.time]
    timeIn2: Mapped[datetime.time]
    timeOut2: Mapped[datetime.time]
    perPayHour: Mapped[int] = mapped_column(nullable=False)
    overTimePay: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

class Pay(db.Model):
    id : Mapped[int] = mapped_column(primary_key = True)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    employeeId: Mapped[int] = mapped_column(nullable=False)
    totalHour: Mapped[int] = mapped_column(nullable=False)
    totalPay: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)