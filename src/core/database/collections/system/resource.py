from ..base import AbstractCollection


# class ResourceType:
#     Stratergy = 'Stratergy'


class ResourceStatus:
    Active = 'Active' # just created - initial status
    Blocked = 'Blocked' # I/O blocked - resumable
    Inactive = 'Inactive' # stopped - not accessible
    Deleted = 'Deleted' # object gc - removed from memory



class ResourceCollection(AbstractCollection):

    def __init__(self):
        super().__init__(path='resources')

    def add(
        self, id, type, status: ResourceStatus = ResourceStatus.Active, **kwargs
    ):
        return self.insert_one(
                document={
                    'resource_type': type,
                    'status': status,
                    'destroyed_at': None,
                    **kwargs
                }, 
                resource_id=id
            )

    def block(self, id):
        return self.update_one(
            query={ 'resource_id': id }, 
            document={ 'status': ResourceStatus.Blocked }
        )

    def deactivate(self, id):
        return self.update_one(
            query={ 'resource_id': id }, 
            document={ 'status': ResourceStatus.Inactive }
        )

    def destroy(self, id):
        return self.update_one(
            query={ 'resource_id': id }, 
            document={ 'status': ResourceStatus.Deleted }
        )


class ResourceConfigCollection(AbstractCollection):

    def __init__(self):
        super().__init__(path='resource_configs')

    def add(self, resource_id, **kwargs):
        return self.insert_one(
                document={ 'resource_id': resource_id, **kwargs }, 
                resource_id=resource_id
            )

    def upsert(self, **kwargs):
        assert kwargs.get('resource_id', None), """
                Resource Config Collection: resource_id must be passed
            """
        return self.insert_many(documents=[kwargs], id_key='resource_id')
