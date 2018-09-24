import sqlalchemy as sa

from data import insert, select, update
from models import create_tables

engine = sa.create_engine("sqlite:///some.db")
# create_tables(engine)
# insert(engine)
# select(engine)
update(engine)

