from enum import Enum

class OrderType(Enum):
  LIMIT	= "LIMIT" # timeInForce, quantity, price
  MARKET = "MARKET" # quantity or quoteOrderQty
  STOP_LOSS = "STOP_LOSS" # quantity, stopPrice or trailingDelta
  STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT" # timeInForce, quantity, price, stopPrice or trailingDelta
  TAKE_PROFIT = "TAKE_PROFIT" # quantity, stopPrice or trailingDelta
  TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT" # timeInForce, quantity, price, stopPrice or trailingDelta
  LIMIT_MAKER = "LIMIT_MAKER" # quantity, price