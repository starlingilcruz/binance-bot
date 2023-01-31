from ..base import AbstractCollection

# Operation Collection Fields
# 1. Operation Id -> represents any class instance id
# 2. Scope
# 3. Created At


class OperationScope:
    # Operation - logs information about a running process
    Stratergy = 'Stratergy'
    Transaction = 'Transaction'
    Event = 'Event'


class OperationCollection(AbstractCollection):

    def __init__(self):
        super().__init__(path='operations')


    def add(self, id, scope: OperationScope, **kwargs):
        return self.insert_one(
                document={
                    scope: scope,
                    **kwargs
                }, 
                operation_id=id
            )