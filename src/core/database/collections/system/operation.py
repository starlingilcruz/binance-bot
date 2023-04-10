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


class OperationState:
    New = 'New' # initial state in the process lifecycle - just created
    Ready = 'Ready' # is waiting to be assigned the processor, so it can runs
    Suspended = 'Suspended' # Initially in the ready state in main memory but 
    # lack of memory forced them to be suspended
    Running = 'Running' # is being executed
    Blocked = 'Blocked' # is waiting for some event occur
    Terminated = 'Terminated' # is terminated once it finishes its execution 


class OperationCollection(AbstractCollection):

    def __init__(self):
        super().__init__(path='operations')


    def add(self, id, scope: OperationScope, state: OperationState, **kwargs):
        return self.insert_one(
                document={
                    scope: scope,
                    state: state,
                    **kwargs
                }, 
                operation_id=id
                # TODO add revision count
            )