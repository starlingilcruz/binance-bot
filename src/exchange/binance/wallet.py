from functools import cache

from .misc.adapters import drop_zero_balance
from .misc.exceptions import AccountNotFound

@cache
def coins_info(client, **kwargs):
    return client.coin_info(**kwargs)

def get_account(client, **kwargs):
    return drop_zero_balance(client.account(**kwargs))

def get_asset_balance(client, asset):
    account = client.get_account()

    if not account:
      raise AccountNotFound

    balances = account.get("balances", [])

    balance = [b for b in balances if b.get("asset") == asset]

    return balance[0] if balance else None