import requests
import pandas as pd

from bs4 import BeautifulSoup
from collections import Counter
from aa_backend_service.db.account_aggregator import AccountAggregatorCreate
from aa_backend_service.db import Session, engine
from aa_backend_service.services.aa import create_aa

get_session = Session(engine)
def get_db():
    try:
        yield get_session
    finally:
        get_session.close()

async def scrape_aa_availability_timeseries():
    try:
        url = "https://sahamati.org.in/fip-aa-mapping/"

        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {"id": "tablepress-44"})

        if not table:
            return
        headers = []
        for th in soup.find_all('thead')[0].find_all('th'):
            headers.append(th.text.strip())

        rows = []
        for tr in soup.find_all('tbody')[0].find_all('tr'):
            cells = tr.find_all('td')
            row = [cell.text.strip() for cell in cells]
            rows.append(row)

        df = pd.DataFrame(rows, columns=headers)

        # Storing the AA names
        account_aggregator = [aa for aa in headers[4:]]

        for aa in account_aggregator:
            data = [val for val in df[aa]]
            counter = Counter(data)

            unique_values_dict = dict(counter)
            
            aa_db_value: AccountAggregatorCreate = AccountAggregatorCreate(
                aa_name=aa, 
                live=unique_values_dict.get('Live', 0),
                testing_phase=unique_values_dict.get('Testing', 0),
                na=unique_values_dict.get('x', 0)
            )
            await create_aa(aa_db_value)

    except Exception as e:
        print(e)
