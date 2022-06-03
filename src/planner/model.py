import datetime
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
import enum


db = SQLAlchemy()


class Shift(str, enum.Enum):
    DAY = 'DAY'
    LATE = 'LATE'
    NIGHT = 'NIGHT'


@dataclass
class Worker(db.Model):
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


@dataclass
class Allocation(db.Model):
    id: int
    date: datetime.datetime
    shift: Shift
    worker: Worker

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    shift = db.Column(db.Enum(Shift), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=False)
    worker = db.relationship('Worker', backref=db.backref('allocations', lazy=True, cascade='all, delete-orphan'))

