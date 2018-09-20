import random

from faker import Faker
from sqlalchemy.orm import sessionmaker
from models import (
    Candidate, GenderEnum, Position, PositionDetails, Employee, StaffCatEnum)

CANDIDATE_NUMBER = 100
POSITION_NUMBER = 30


def fill_db(engine):
    fake = Faker('ru_RU')
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in range(CANDIDATE_NUMBER):
        session.add(Candidate(id=i,
                              fio=fake.name(),
                              gender=random.choice(list(GenderEnum)),
                              birth=fake.date_this_decade(),
                              deputat=fake.pybool()))

    for i in range(POSITION_NUMBER):
        session.add(Position(id=i,
                             name=fake.job()))
        session.add(PositionDetails(id=i,
                                    staff_cat=random.choice(list(StaffCatEnum)),
                                    salary=fake.pyint(),
                                    position_id=i))

    for i in range(CANDIDATE_NUMBER * 2):
        session.add(Employee(id=i,
                             tab_num=fake.isbn10(),
                             candidate_id=(fake.pyint() % CANDIDATE_NUMBER),
                             position_id=(fake.pyint() % POSITION_NUMBER)))
    session.commit()



