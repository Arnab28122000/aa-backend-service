import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from aa_backend_service.routers import account_aggregator


app = FastAPI()
app.include_router(account_aggregator.router)

client = TestClient(app)

def test_search_no_results():
    response = client.get("/aa/search/?aa_name=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "AccountAggregator not found"}

def test_search_setu_aa():
    response = client.get("/aa/search/?aa_name=Setu AA")
    assert response.status_code == 200
    assert response.json() == ["Setu AA"]

def test_search_aa():
    response = client.get("/aa/search/?aa_name=aa")
    assert response.status_code == 200
    assert response.json() == ["Protean SurakshAA", "Saafe", "Setu AA"]
