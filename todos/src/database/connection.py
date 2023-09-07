import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from _config import MYSQL_URL

DATABASE_URL = MYSQL_URL

engine = create_engine(DATABASE_URL)
# engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionFactory()


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
