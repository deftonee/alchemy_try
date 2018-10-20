import enum
import os
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    fullname = sa.Column(sa.String)
    password = sa.Column(sa.String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


class GenderEnum(enum.Enum):
    male = 1
    female = 2
    another = 3


class StaffCatEnum(enum.Enum):
    first = 1
    second = 2
    third = 3


class Candidate(Base):
    __tablename__ = 'candidate'
    id = sa.Column(sa.Integer, primary_key=True)
    fio = sa.Column(sa.String)
    gender = sa.Column(sa.Enum(GenderEnum))
    birth = sa.Column(sa.Date)
    deputat = sa.Column(sa.Boolean)
    employee = relationship("Employee", back_populates="candidate")


class Position(Base):
    __tablename__ = 'position'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    details = relationship("PositionDetails",
                           uselist=False, back_populates="position",
                           lazy='joined')


class Employee(Base):
    __tablename__ = 'employee'
    id = sa.Column(sa.Integer, primary_key=True)
    tab_num = sa.Column(sa.String, index=True)
    candidate_id = sa.Column(sa.ForeignKey(Candidate.id))
    position_id = sa.Column(sa.ForeignKey(Position.id))
    candidate = relationship("Candidate", back_populates="employee")


class PositionDetails(Base):
    __tablename__ = 'position_details'
    id = sa.Column(sa.Integer, primary_key=True)
    staff_cat = sa.Column(sa.Enum(StaffCatEnum), nullable=False)
    salary = sa.Column(sa.Integer, nullable=False)
    position_id = sa.Column(sa.Integer, sa.ForeignKey('position.id'))
    position = relationship("Position", uselist=False, back_populates="details")


def create_tables(engine):
    if os.path.exists("some.db"):
        os.remove("some.db")
    Base.metadata.create_all(engine)

