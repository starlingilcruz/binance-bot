# adapters for returning values

def drop_zero_balance(account):
    assert "balances" in account, "Balances missing in account data"

    account.update({
      'balances': [
          n for n in account.get('balances', []) 
          if float(n.get('free')) > 0
        ] 
    })

    return account