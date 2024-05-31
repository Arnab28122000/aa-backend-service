from fastapi import FastAPI
from aa_backend_service.routers import account_aggregator
from fastapi.middleware.cors import CORSMiddleware

import subprocess
import sys


from aa_backend_service.cron_job import create_cron_job
from aa_backend_service.services.aa import create_dummy_aa_data

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://aa-ui.vercel.app",
    "https://setu-ui.dashtics.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_tests():
    result = subprocess.run([sys.executable, '-m', 'pytest'], check=False)
    return result.returncode


app.include_router(account_aggregator.router)

@app.get("/", include_in_schema=False)
async def root():
    return "Welcome to AA Metrics"

def start_application():
    # Here you could start your application if necessary
    # For example, you could start a server or set up any required state
    pass

def run_tests():
    # Run the tests using pytest
    result = subprocess.run([sys.executable, '-m', 'pytest'], check=False)
    return result.returncode

if __name__ == "__main__":
    # start_application()
    # try:
    #     exit_code = run_tests()
    #     sys.exit(exit_code)
    # except Exception as e:
    #     print(e)
    create_dummy_aa_data()