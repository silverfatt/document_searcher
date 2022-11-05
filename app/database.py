import os

import sqlalchemy
from sqlalchemy import create_engine, Column, ARRAY, Integer, Text, DateTime, String
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base

DB_URL = f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}" \
         f"@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"

db_engine = create_engine(DB_URL)
Base = declarative_base()


class Document(Base):
    __tablename__ = "document"

    doc_id = Column(Integer, primary_key=True)
    rubrics = Column(ARRAY(String))
    text = Column(Text)
    created_date = Column(DateTime)


def prepare_db(engine):
    try:
        if not sqlalchemy.inspect(engine).get_table_names():
            Base.metadata.create_all(engine)
    except OperationalError:
        print("Wrong database info. Check DB_USER, DB_PASSWORD, DB_NAME and DB_HOST variables.")
        print(f"Current URL:{DB_URL}")
        exit(1)
