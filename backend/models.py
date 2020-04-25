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

    results = relationship('Result', cascade = 'all, delete-orphan')

    def format(self):
        return {
            'id': self.id,
            'gender': self.gender,
            'first name': self.first_name,
            'last name': self.last_name,
            'year of birth': self.birth_year
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Meet(db.Model):
    __tablename__ = 'meets'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    city = Column(String)
    country = Column(String)

    results = relationship('Result', cascade = 'all, delete-orphan')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'start date': self.start_date,
            'end date': self.end_date,
            'city': self.city,
            'country': self.country
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

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

    def format(self):
        return {
            'id': self.id,
            'swimmer id': self.swimmer_id,
            'meet_id': self.meet_id,
            'course': self.course,
            'distance': self.distance,
            'stroke': self.stroke,
            'time': self.time.strftime("%-M:%S.%f")[:-4]
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()