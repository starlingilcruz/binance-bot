
from core.events import EventEmitter
from core.system.resource import Resource
from core.trade import TradeType


class Stratergy(Resource):
    """ Base strategies class """

    trade_type = None

    requires_update = False # needs to update from exchange
    

    def __init__(self, symbol, client, collection):
        self.symbol = symbol
        self.client = client
        self.collection = collection
        self.event = EventEmitter()
        assert self.trade_type is not None, 'Stratergy must define a trade type'

    def __call__(self):
        print("*** Running stratergy ***")
        # TODO add async calls

        # Pull all existing orders on the exchange and store in db
        self.sync_from_exchange()
        # Prepare variables, models, function for execution
        self.pre_execute()
        # Scalping processing - price action base 
        self.execute()

    def sync_from_exchange(self):
        if not self.requires_update:
            return None
        # fetch data from exchange

    def pre_execute(self):
        if self.requires_update:
            raise Exception('Requires update')
        # prepare required variables for the model trading execution
        # variables
        # ML models
        # python dynamic functions
        # raise NotImplementedError

    def execute(self):
        if self.requires_update:
            raise Exception('Requires update')
        # initial process run
        raise NotImplementedError

    def monitor(self):
        pass

    @staticmethod
    def run_all(ttype: TradeType = None):
        # TODO run all async
        instances = Stratergy.get_instances(ttype)

        if not instances:
            # TODO derive from base exception
           raise "No stratergy instances where found"

        for stratergy in instances:
            stratergy()