"""
  Binance spot market filter definition.

  Lot - refers to the amount of the order, otherwise known as quantity

  Notional - the value in the base asset calculated by price * quantity

  Base Asset - refers to the asset that is the quantity of a symbol. For the symbol BTCUSDT, BTC would be the base asset.

  Quote Asset - refers to the asset that is the price of a symbol. For the symbol BTCUSDT, USDT would be the quote asset.

  Symbol - a pair of assets that are traded on Binance
"""

# Filters define trading rules on a symbol or an exchange. Filters come in two forms: symbol filters and exchange filters.

from abc import abstractmethod
from functools import cached_property

from binance.helpers import round_step_size
from decimal import Decimal

from .utils import get_valid_range, apply_intervals_filter

# TODO come back to define the rule interface
class RuleInterface:
    """ Rules defines limits and conditions an order can be placed """

    @abstractmethod
    def is_valid(self, value):
        pass

    @abstractmethod
    def get_min_max_price(self, value):
        pass

    @abstractmethod
    def get_min_max_quantity(self, value):
        pass
    

class Rule(RuleInterface):

    def __init__(self, client = None, symbol = None, symbol_info = None):
        assert (client and symbol) or symbol_info, "Must pass a client and symbol for search or symbol_info"
        self.client = client
        self.symbol_info = symbol_info.get('filters', None)

        if not self.symbol_info:
            self.symbol_info = self.get_symbol_info(symbol)
    
    @cached_property
    def get_symbol_info(self, symbol):
        return self.client.get_symbol_info(symbol)
        
    def get_symbol_price_range(self):
        for f in self.symbol_info:
           if f['filterType'] == 'PRICE_FILTER':
              yield (
                  Decimal(f['minPrice']), 
                  Decimal(f['maxPrice']), 
                  Decimal(f['tickSize'])
              )

    def get_symbol_qty_range(self):
        for f in self.symbol_info:
           if f['filterType'] == 'LOT_SIZE':
              yield (
                  Decimal(f['minQty']), 
                  Decimal(f['maxQty']), 
                  Decimal(f['stepSize'])
              )

    def get_symbol_min_notional(self, filters):
        for f in self.symbol_info:
            if f['filterType'] == 'MIN_NOTIONAL':
              yield Decimal(f['minNotional'])


    def is_valid(self, value):
        return super().is_valid(value)


    def get_min_max_quantity(self, target_qty):
        min_qty, max_qty, step_size = next(
            self.get_symbol_qty_range()
        )

        return get_valid_range(
          value=target_qty,
          min_value=min_qty,
          max_value=max_qty,
          portion_size=step_size
        )

    def get_min_max_price(self, target_price):
        min_price, max_price, tick_size = next(
            self.get_symbol_price_range()
        )

        return get_valid_range(
          value=target_price,
          min_value=min_price,
          max_value=max_price,
          portion_size=tick_size
        )