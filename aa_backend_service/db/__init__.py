import os
from sqlmodel import create_engine, Session

db_username = os.environ['dashtics_username']
db_password = os.environ['dashtics_password']
db_endpoint = os.environ['dashtics_endpoint']
db_name = os.environ['dashtics_db_name']

DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_endpoint}/{db_name}"

engine = create_engine(
    DATABASE_URL,
    pool_size=10,         # Increase pool size
    max_overflow=20,      # Increase overflow limit
    pool_timeout=30,      # Set the pool timeout (default is 30 seconds)
    pool_recycle=1800     # Recycle connections after 30 minutes
)

def get_session() -> Session:
   return Session(engine)