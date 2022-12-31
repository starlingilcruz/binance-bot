
from .base import AbstractCollection


## Order life cycle
# 1. filled = False
# 2. proccessinng = True
# 3. filled = True


class OrderCollection(AbstractCollection):
    # 1. Is an abstract collection object that defines hight level functions 
    # that later are tracked by an object inspector to look for the function definitions.

    # 2. That object function definitions allows to control the collection at highest level
    # also, create customizable functions dinamically.

    def __init__(self):
        super().__init__(path='orders')
    
    def filled(self, **kwargs):
        return self.find({ 'filled': True })

    def non_filled(self, x):
        return self.find({ 'filled': False, 'processing': False })
        # return self.collection.find()

    def cancelled(self, **kwargs):
        return self.find({ 'cancelled': True })

    def mark_as_filled(self, order_id):
        return self.update_one(query={ 'orderId': order_id }, document={ 'filled': True })

    def mark_batch_as_processing(self, orders):
        return self.update_many(
            documents=orders, 
            values={ 'processing': True },
            id_key='orderId'
        )

    def mark_processing_as_completed(self):
        return self.collection.update_many(
            { 'processing': True },
            {
                "$set": {
                  "processing": False,
                  "filled": True
                } 
            }
        )