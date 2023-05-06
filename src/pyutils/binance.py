from web_apis.binance.sessions import SignedBinanceSession
from web_apis.binance.queries import AccountSnapshotQuery

from pyutils.auth import get_secrets


# TODO: very similar to joplin. make abstract?
def create_signed_session():
    secrets = get_secrets("binance_secrets.json")
    return SignedBinanceSession(**secrets)


def get_account_balance_details(session):
    query = AccountSnapshotQuery()
    req = session.get(query)
    data = req.json()

    # get most recent snapshot
    snapshot = data["snapshotVos"][-1]

    return {asset["asset"]: asset["free"] for asset in snapshot["data"]["balances"]}


# TODO: get average price of buying
# TODO: get eur estimation
# TODO: get total deposit
# TODO: plot losses/gains (deposit - current eur balance)
# TODO: create bar plot with current losses for each coin
