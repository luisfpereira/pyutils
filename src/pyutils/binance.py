import json

from web_apis.binance.sessions import SignedBinanceSession
from web_apis.binance.queries import AccountSnapshotQuery

from pyutils import get_home_path


# TODO: very similar to joplin. make abstract?
def create_signed_session():
    secrets = get_secrets()
    return SignedBinanceSession(**secrets)


def get_account_balance_details(session):
    query = AccountSnapshotQuery()
    req = session.get(query)
    data = req.json()

    # get most recent snapshot
    snapshot = data['snapshotVos'][-1]

    return {asset['asset']: asset['free'] for asset in snapshot['data']['balances']}


# TODO: get average price of buying
# TODO: get eur estimation
# TODO: get total deposit
# TODO: plot losses/gains (deposit - current eur balance)
# TODO: create bar plot with current losses for each coin


def get_auth_filepath():
    return get_home_path() / 'binance_secrets.json'


def get_secrets():
    filepath = get_auth_filepath()
    with open(filepath, 'r') as file:
        data = json.load(file)

    return data
