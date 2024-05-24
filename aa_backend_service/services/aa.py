import uuid
import random
from datetime import datetime, timedelta

from aa_backend_service.db.account_aggregator import AccountAggregatorCreate, AccountAggregator
from aa_backend_service.db import Session, engine

get_session = Session(engine)
def get_db():
    try:
        yield get_session
    finally:
        get_session.close()

async def create_aa(account: AccountAggregatorCreate):
    _id = str(uuid.uuid1())
    aa_db_value: AccountAggregator = AccountAggregator(
        id=_id, 
        aa_name=account.aa_name, 
        live=account.live,
        testing_phase=account.testing_phase,
        na=account.na,
        date=datetime.today().strftime('%Y-%m-%d')
    )
    get_session.add(aa_db_value)
    get_session.commit()
    get_session.close()

def create_dummy_aa_data():
    today = datetime.today()
    aa_list = ['Anumati', 'CAMS', 'CRIF', 'Digio', 'Finvu', 'INK', 'NADL', 'Onemoney', 'PhonePe', 'Protean SurakshAA', 'Setu AA', 'Saafe', 'TallyEdge', 'Yodlee']
    for i in range(10):
        date = today - timedelta(days=i)
        formatted_date = date.strftime('%Y-%m-%d')
        for aa in aa_list:
            _id = str(uuid.uuid1())
            aa_db_value: AccountAggregator = AccountAggregator(
                id=_id, 
                aa_name=aa, 
                live=random.randint(0, 100),
                testing_phase=random.randint(0, 100),
                na=random.randint(0, 100),
                date=formatted_date
            )
            print("AA value: ", aa_db_value)
            get_session.add(aa_db_value)
            get_session.commit()
            get_session.close()
