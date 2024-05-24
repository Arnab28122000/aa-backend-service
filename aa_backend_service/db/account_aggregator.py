from datetime import date
from typing import List
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from aa_backend_service.db import get_session

session = get_session()

class AccountAggregator(SQLModel, table=True):
    __tablename__ = "account_aggregator"
    id: str = Field(default=None, primary_key=True)
    aa_name: str = Field(index=True)
    live: int
    testing_phase: int
    na: int
    date: date

    def save_to_db(self):
        session.add(self)
        session.commit()

class AccountAggregatorCreate(SQLModel):
    aa_name: str
    live: int
    testing_phase: int
    na: int

class TimeSeriesResponse(BaseModel):
    aa_name: str
    date: List[str]
    na: List[int]
    testing_phase: List[int]
    live: List[int]