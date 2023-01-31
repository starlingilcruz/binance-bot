from datetime import datetime

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
        document.update({ 'created_at': datetime.utcnow() })
        for k, v in kwargs.items():
            document.update({k:v})
        return self.collection.insert_one(document)

    # TODO upsert_many
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

        documents = [
            d.update({ 'created_at': datetime.utcnow() }) for d in documents
        ]
        return self.collection.insert_many(documents)
    
    def update_one(self, query, document):
        return self.collection.update_one(query, {'$set': document})

    def update_many(self, documents, values, **kwargs):
        id_key = kwargs.get('id_key', None)

        # TODO raise custom exception
        assert id_key, "No id_key provided"

        results = []
        for document in documents:
            _id = document.get(id_key)
            # TODO raise custom exception
            assert _id, "Invalid id_key"
            query = {}
            query[id_key] = _id
            results.append(self.update_one(query=query, document=values))
        return results
        # return self.collection.update_many(query, {'$set': documents})