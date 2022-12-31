from core.database.connection import get_database

database = get_database('default')


class AbstractCollection:

    # Processed = completed
    # Non processed = pending

    def __init__(self, path):

        if not len(path):
          raise "No collection path provided"

        self.collection = database[path]

    def find_one(self, **kwargs):
        return self.collection.find_one(kwargs)

    def find(self, kwargs):
        return self.collection.find(kwargs)

    def insert_one(self, document, **kwargs):
        for k, v in kwargs.items():
            document.update({k:v})
        return self.collection.insert_one(document)

    def insert_many(self, documents, **kwargs):
        # Insert if not exists
        id_key = kwargs.get('id_key', None)

        if id_key:
            inserted = []
            for document in documents:
                args = {}
                args[id_key] = document.get(id_key)
                if not self.collection.find_one(args):
                    inserted.append(
                        self.insert_one(document, filled=False, processing=False)
                    )
            return inserted

        return self.collection.insert_many(documents)
    
    def update_one(self, query, document):
        return self.collection.update_one(query, {'$set': document})

    def update_many(self, documents, values, **kwargs):
        id_key = kwargs.get('id_key', None)

        if not id_key:
            raise Exception("No id_key provided")

        result = []

        for document in documents:
            args = {}
            args[id_key] = document.get(id_key)
            print(args)
            print(values)
            result.append(self.update_one(query=args, document=values))
        return result
        # return self.collection.update_many(query, {'$set': documents})