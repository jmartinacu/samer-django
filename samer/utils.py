from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId
import boto3
from django.conf import settings


s3 = boto3.client('s3')


# QUEDA POR HACER EL MANEJO DE ERRORES

def upload_file(file: bytes, object_name: str):
    s3.upload_fileobj(
        file,
        settings.AWS_BUCKET_NAME,
        object_name
    )
    return (
        f'https://{settings.AWS_BUCKET_NAME}.'
        f's3.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{object_name}'
    )


def delete_file(object_name):
    s3.delete_object(settings.AWS_BUCKET_NAME, object_name)


def get_db_handle(db_name: str, connection_string: str):
    client = MongoClient(connection_string)
    db_handle = client[db_name]
    return db_handle, client


class MongoDBCollection:
    _id: ObjectId
    collection: Collection

    def __init__(self, db, collection_name):
        self.collection = db[collection_name]

    def insert_one(self, document: dict, *args, **kwargs):
        return self.collection.insert_one(document, *args, **kwargs)

    def find_one(self, query: dict, *args, **kwargs):
        return self.collection.find_one(query, *args, **kwargs)

    def find(self, query: dict, *args, **kwargs):
        return self.collection.find(query, *args, **kwargs)

    def update_one(self, query: dict, update, *args, **kwargs):
        return self.collection.update_one(query, update, *args, **kwargs)

    def delete_one(self, query: dict, *args, **kwargs):
        return self.collection.delete_one(query, *args, **kwargs)

    def count(self, query: dict, *args, **kwargs):
        return self.collection.count_documents(query, *args, **kwargs)


(db, client) = get_db_handle(settings.DB_NAME, settings.CONNECTION_STRING)
