from datetime import date, datetime, timedelta
import json
from typing import List, Optional

from fastapi import APIRouter,  HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, col, select
from sqlalchemy.sql import text

from aa_backend_service.db import get_session
from aa_backend_service.db.account_aggregator import AATrend, AccountAggregator, TimeSeriesResponse

router = APIRouter(
    prefix="/aa",
    tags=["aa"],
    responses={404: {"description": "Not found"}},
)
    
@router.get("/search/", response_model=List[str])
def search_account_aggregator(aa_name: Optional[str] = None, session: Session = Depends(get_session)):
    if aa_name is None:
        aa_name = ''
    statement = select(AccountAggregator.aa_name).distinct()
    if aa_name:
        # case-insensitive search using ILIKE
        statement = statement.where(col(AccountAggregator.aa_name).ilike(f"%{aa_name}%"))
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail="AccountAggregator not found")
    
    print("Result: ", results)
    
    return JSONResponse(status_code=200, content=results)

@router.get("/timeseries/", response_model=List[AccountAggregator], include_in_schema=False)
def get_timeseries_data(
    aa_name: Optional[str] = None,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    session: Session = Depends(get_session)
):
    # Default to the past week if no dates are provided
    if aa_name is None:
        raise HTTPException(status_code=400, detail="Please provide an AA Name")
    
    if start_date is None:
        start_date = datetime.today().date() - timedelta(days=7)
    if end_date is None:
        end_date = datetime.today().date()

    statement = select(AccountAggregator).where(AccountAggregator.date >= start_date, AccountAggregator.date <= end_date)

    if aa_name:
        statement = statement.where(AccountAggregator.aa_name == aa_name)

    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail="No data found for the specified parameters")
    
    # Convert ORM objects to Pydantic models
    response_data = [{
        "id": result.id,
        "aa_name": result.aa_name,
        "live": result.live,
        "testing_phase": result.testing_phase,
        "na": result.na
    } for result in results]

    return JSONResponse(status_code=200, content=response_data)

@router.get("/timeseries_graph/", response_model=TimeSeriesResponse, include_in_schema=False)
def get_timeseries_data(
    aa_name: Optional[str] = None,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    session: Session = Depends(get_session)
):
    # Default to the past week if no dates are provided
    if aa_name is None:
        raise HTTPException(status_code=400, detail="Please provide an AA Name")
    
    if start_date is None:
        start_date = datetime.today().date() - timedelta(days=7)
    if end_date is None:
        end_date = datetime.today().date()

    statement = select(AccountAggregator).where(AccountAggregator.date >= start_date, AccountAggregator.date <= end_date)

    if aa_name:
        statement = statement.where(AccountAggregator.aa_name == aa_name)

    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail="No data found for the specified parameters")
    
    response_data = {
        "aa_name": aa_name,
        "date": [result.date.strftime("%d-%m-%Y") for result in results],
        "na": [result.na for result in results],
        "testing_phase": [result.testing_phase for result in results],
        "live": [result.live for result in results]
    }

    return JSONResponse(status_code=200, content=response_data)

@router.get("/nivo_timeseries_graph/", response_model=AATrend)
def get_timeseries_data(
    aa_name: Optional[str] = None,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    session: Session = Depends(get_session)
):
    # Default to the past week if no dates are provided
    if aa_name is None:
        raise HTTPException(status_code=400, detail="Please provide an AA Name")
    
    if start_date is None:
        start_date = datetime.today().date() - timedelta(days=7)
    if end_date is None:
        end_date = datetime.today().date()

    statement = select(AccountAggregator).where(AccountAggregator.date >= start_date, AccountAggregator.date <= end_date)

    if aa_name:
        statement = statement.where(AccountAggregator.aa_name == aa_name)

    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=404, detail="No data found for the specified parameters")
    
    response_data = {
        "aa_name": aa_name,
        "data": [
            {
                "id": "na",
                "data": [{"x": result.date.strftime("%d-%m-%Y"), "y": result.na} for result in results]
            },
            {
                "id": "testing_phase",
                "data": [{"x": result.date.strftime("%d-%m-%Y"), "y": result.testing_phase} for result in results]
            },
            {
                "id": "live",
                "data": [{"x": result.date.strftime("%d-%m-%Y"), "y": result.live} for result in results]
            }
        ]
    }

    return JSONResponse(status_code=200, content=response_data)