
def account_balance(self):
    account = self.account()

    if not account:
        raise "Not account retrieved"

    balances = account.get('balances', None)

    return [b for b in balances if float(b.get('free', 0)) > 0]