from functools import cache

@cache
def coins_info(self, **kwargs):
    return self.coin_info(**kwargs)