from ..base import AbstractCollection


class ResourceType:
    Stratergy = 'Stratergy'


class ResourceStatus:
    Active = 'Active'
    Blocked = 'Blocked'
    Inactive = 'Inactive'


class ResourceCollection(AbstractCollection):

    def __init__(self):
        super().__init__(path='resources')


    def add(self, id, rtype: ResourceType, status: ResourceStatus, **kwargs):
        return self.insert_one(
                document={
                    'resource_type': rtype,
                    'status': status,
                    'destroyed_at': None,
                    **kwargs
                }, 
                operation_id=id
            )

    def destroy(self, id):
        return self.update_one(
            query={ 'operation_id': id }, 
            document={ 'status': ResourceStatus.Inactive }
        )