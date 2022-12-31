from enum import Enum


class OrderType(Enum):
  LIMIT	= "LIMIT" # timeInForce, quantity, price
  MARKET = "MARKET" # quantity or quoteOrderQty
  STOP_LOSS = "STOP_LOSS" # quantity, stopPrice or trailingDelta
  STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT" # timeInForce, quantity, price, stopPrice or trailingDelta
  TAKE_PROFIT = "TAKE_PROFIT" # quantity, stopPrice or trailingDelta
  TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT" # timeInForce, quantity, price, stopPrice or trailingDelta
  LIMIT_MAKER = "LIMIT_MAKER" # quantity, price


class EventType(Enum):
    FILL_ORDER = 'FILL_ORDER'
    PREPARE_PLACE_ORDER = 'PREPARE_PLACE_ORDER'
    PLACE_ORDER = 'PLACE_ORDER'
    CANCEL_ORDER = 'CANCEL_ORDER'

    ORDER_FILLED = 'ORDER_FILLED'
    ORDER_COMPLETED = 'ORDER_COMPLETED' # means that no ohter counterpart order will be placed
    ORDER_CANCELLED = 'ORDER_CANCELLED'
    ORDER_PLACED = 'ORDER_PLACED'
    
    RUNNER_INITIALIZED = 'RUNNER_INITIALIZED'
    RUNNER_STOPED = 'RUNNER_STOPED'
    