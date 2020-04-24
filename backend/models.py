import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Enum, Date, Time, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship


database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class Swimmer(db.Model):
    __tablename__ = 'swimmers'

    id = Column(Integer, primary_key=True)
    gender = Column(Enum('F', 'M', 'X', name='gender'), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)

    results = relationship('Result')


class Meet(db.Model):
    __tablename__ = 'meets'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    city = Column(String)
    country = Column(String)

    results = relationship('Result')


class Result(db.Model):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    swimmer_id = Column(Integer, ForeignKey('swimmers.id'), nullable=False)
    meet_id = Column(Integer, ForeignKey('meets.id'), nullable=False)

    course = Column(Enum('LCM', 'SCM', 'SCY', name='course'), nullable=False)
    distance = Column(Integer, CheckConstraint('distance IN (25, 50, 100, 200, 400, 800, 1500)'), nullable=False)
    stroke = Column(Enum('Back', 'Breast', 'Fly', 'Free', 'IM', name='stroke'), nullable=False)
    time = Column(Time, nullable=False)

    swimmer = db.relationship('Swimmer')
    meet = db.relationship('Meet')

