import os
from sqlmodel import create_engine, Session

db_username = os.environ['dashtics_username']
db_password = os.environ['dashtics_password']
db_endpoint = os.environ['dashtics_endpoint']
db_name = os.environ['dashtics_db_name']

db_password = 'SyW3e9SvRKt4m>Ze!Wlr+%U~[7Sk'

DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_endpoint}/{db_name}"

engine = create_engine(DATABASE_URL)

def get_session() -> Session:
   return Session(engine)