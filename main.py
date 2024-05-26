from fastapi import FastAPI
from aa_backend_service.routers import account_aggregator
from fastapi.middleware.cors import CORSMiddleware

from aa_backend_service.cron_job import create_cron_job
from aa_backend_service.services.aa import create_dummy_aa_data

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(account_aggregator.router)

@app.get("/")
async def root():
    return "Welcome to AA Metrics"

if __name__ == "__main__":
    create_cron_job()
    # create_dummy_aa_data()