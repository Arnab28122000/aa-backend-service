import os
from openai import OpenAI
from pinecone import Pinecone
from pinecone import ServerlessSpec
from datetime import date, datetime, timedelta
import json
from typing import List, Optional

from fastapi import APIRouter,  HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlmodel import Session, col, select
from sqlalchemy.sql import text

from aa_backend_service.db import get_session
from aa_backend_service.db.account_aggregator import AATrend, AccountAggregator, TimeSeriesResponse

# Initialize OpenAI
open_ai_key = os.environ['OPENAI_KEY']
pinecone_key = os.environ['PINECONE_API']
MODEL = "text-embedding-3-large"

# Initialize Pinecone
# pinecone.init(api_key=pinecone_key, environment='gcp-starter')

pc = Pinecone(api_key=pinecone_key)
client = OpenAI(api_key=open_ai_key)

cloud = 'aws'
region = 'us-east-1'

spec = ServerlessSpec(cloud=cloud, region=region)

router = APIRouter(
    prefix="/aa",
    tags=["aa"],
    responses={404: {"description": "Not found"}},
)

def dict_to_string(input_dict):
    csv_string = ",".join([f"{key}: {value}" for key, value in input_dict.items()])
    return csv_string
    
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

@router.get("/aa_qa", response_model=List[str])
def search_account_aggregator(prompt: Optional[str] = None, session: Session = Depends(get_session)):
    if prompt is None or prompt == '':
        raise HTTPException(status_code=403, detail="Please provide a prompt")
    try:
        embed_model = "text-embedding-3-large"
        query = ''

        query = prompt + query

        res = client.embeddings.create(
            input=[prompt],
            model=embed_model
        )
        index_name = 'setu-aa'
        # connect to index
        index = pc.Index(index_name)
        xq = res.data[0].embedding

        res = index.query(vector=xq, top_k=20, include_metadata=True)
        limit = 4097

        contexts = [
        x['metadata']['context'] for x in res['matches']
        ]

        # build our prompt with the retrieved contexts included
        prompt_start = (
            "Answer the question based on the context below.\n\n"+
            "Context:\n"
        )
        prompt_end = (
            f"\n\nQuestion: {query}\nAnswer:"
        )
        # append contexts until hitting limit
        for i in range(1, len(contexts)):
            if len("\n\n---\n\n".join(contexts[:i])) >= limit:
                prompt = (
                    prompt_start +
                    "\n\n---\n\n".join(contexts[:i-1]) +
                    prompt_end
                )
                break
            elif i == len(contexts)-1:
                prompt = (
                    prompt_start +
                    "\n\n---\n\n".join(contexts) +
                    prompt_end
                )

        # now query text-davinci-003
        res = client.chat.completions.create(
            model='gpt-3.5-turbo',
            temperature=0,  # Adjust temperature as needed
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = json.loads(res.choices[0].message.content)
        return JSONResponse(status_code=200, content=answer)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
