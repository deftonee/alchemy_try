import sqlalchemy as sa

from data import fill_db
from models import create_tables
from queries import make_queries

engine = sa.create_engine("sqlite:///some.db")
create_tables(engine)
fill_db(engine)
make_queries(engine)
