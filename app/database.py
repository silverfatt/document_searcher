import os

import sqlalchemy
from sqlalchemy import create_engine, Column, ARRAY, Integer, Text, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_host = os.environ['DB_HOST']
engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{db_host}/{db_name}")
Base = declarative_base()


class Document(Base):
    __tablename__ = "document"

    doc_id = Column(Integer, primary_key=True)
    rubrics = Column(ARRAY(String))
    text = Column(Text)
    created_date = Column(DateTime)


def prepare_db():
    if sqlalchemy.inspect(engine).get_table_names() == []:
        Base.metadata.create_all(engine)


print(f"postgresql+psycopg2://{username}:{password}@{db_host}/{db_name}")
