import random
import sqlalchemy as sa

from datetime import date
from faker import Faker
from sqlalchemy.orm import sessionmaker

from models import (
    Candidate, GenderEnum, Position, PositionDetails, Employee, StaffCatEnum)

CANDIDATE_NUMBER = 100
POSITION_NUMBER = 30


def print_orm_result(query, session):
    print(query)
    print(tuple(query))


def print_core_result(query, session):
    print(query)
    result = session.execute(query)
    try:
        print('(%s)' % ', '.join((str(tuple(x.values())) for x in result)))
    except:
        pass


def insert(engine):
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


def select(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    print('===================================================================')

    query = session.query(
        Candidate.fio, PositionDetails.salary
    ).join(
        Employee
    ).join(
        Position
    ).join(
        PositionDetails
    ).filter(
        sa.or_(Candidate.deputat == sa.true(),
               Candidate.birth < date(2013, 1, 1))
    ).order_by(Employee.tab_num)

    print_orm_result(query, session)

    join = sa.join(
        Employee, Candidate, Candidate.id == Employee.candidate_id
    ).join(
        Position, Position.id == Employee.position_id
    ).join(
        PositionDetails, Position.id == PositionDetails.position_id
    )

    query = sa.select(
        (Candidate.fio, PositionDetails.salary),
        sa.or_(Candidate.deputat == sa.true(),
               Candidate.birth < date(2013, 1, 1)),
        from_obj=join,
        order_by=Employee.tab_num
    )

    print_core_result(query, session)

    print('===================================================================')

    query = session.query(
        sa.func.strftime('%Y', Candidate.birth).label('birth_year'),
        sa.func.count().label('c'),
        sa.bindparam("one", 1)
    ).group_by('birth_year').having(sa.func.count() > 10)

    print_orm_result(query, session)

    query = sa.select((
            sa.func.strftime('%Y', Candidate.birth).label('birth_year'),
            sa.func.count().label('c'),
            1
        )
    ).group_by('birth_year').having(sa.func.count() > 10)

    print_core_result(query, session)

    print('===================================================================')


def update(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    subquery = session.query(
        sa.func.max(sa.func.length(Position.name))
    ).limit(1)

    query = session.query(Position).filter(
        sa.func.length(Position.name) == subquery
    )

    print_orm_result(query, session)

    for p in query:
        p.details.salary += 100

    subquery = sa.select((sa.func.min(PositionDetails.id), ))

    query = sa.update(
        PositionDetails
    ).values(
        {PositionDetails.salary: PositionDetails.salary + 100}
    ).where(
        PositionDetails.id == subquery
    )

    print_core_result(query, session)

    print('===================================================================')

    query = sa.update(
        Candidate
    ).values(
        {Candidate.fio: sa.func.upper(Candidate.fio)}
    )

    print_core_result(query, session)

    session.commit()
