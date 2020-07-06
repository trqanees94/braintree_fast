""" This module provides a MongoDB object that binds various collections to their respective python object type. """

'''
    MongoCredentials

    trqanees94
    keepitsimple

    client = pymongo.MongoClient("mongodb+srv://trqanees94:<password>@cluster0.jnhwe.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.test

'''

# clients
import os, pymongo
from pymongo import MongoClient

# data types
from bson import ObjectId
from bson.codec_options import TypeCodec, TypeRegistry
from bson.decimal128 import Decimal128
from decimal import Decimal

# typing
from typing import List, Union

# utils
from time import sleep, time

#certificate verification
import ssl


class MongoDB:
    
    ''' A MongoDB client that binds class attributes to MongoCollection instances,
        allowing for easy encoding/decoding of python objects into the database.
    '''
    
    def __init__(self):
        
        MONGO_URI = "mongodb+srv://{}:{}@{}".format(os.environ["MONGO_USERNAME"],os.environ["MONGO_PASSWORD"],os.environ["MONGO_HOST"])

        mongo_client = pymongo.MongoClient(MONGO_URI, ssl_cert_reqs=ssl.CERT_NONE)
        self.mongo_client = mongo_client
        
        # bind collections
        self.transactions = MongoCollection(self.mongo_client, "transactions")
        self.customers = MongoCollection(self.mongo_client, "customers")
    
    def __enter__(self) -> "MongoDB":
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mongo_client.__exit__(exc_type, exc_val, exc_tb)


class MongoCollection:
    
    ''' This class controls encoding/decoding python objects as BSON data in MongoDB. '''
    
    def __init__(self, mongo_client: pymongo.MongoClient, name: str):
        
        self.collection = mongo_client["fast"][name]
        self.collection.test_database
    
    def insert_one(self, data):
        ''' insert a single object into the collection. '''
        
        return None if not self.collection.insert_one(data) else data
    
    def find(self, *args, **kwargs) -> List:
        ''' return an array of objects from the collection. '''
        
        # return [self.object_type.from_bson(result) for result in self.collection.find(*args, **kwargs)]
        
        return [result for result in self.collection.find()]

    def find_one(self, *args, **kwargs):
        ''' return a single object from the collection. '''
        
        result = self.collection.find_one(*args, **kwargs)
        return None if not result else result

    def count(self, *args, **kwargs):
        ''' return number of objects in collection. '''
        
        result = self.collection.count()
        #new documentation for count()

        return None if not result else result
    
    def find_by_id(self, id: Union[str, ObjectId]):
        ''' return a single object matching :id:. '''
        
        return self.find_one({"_id": ObjectId(id)})
    
    # def find_by_ids(self, ids: List[Union[str, ObjectId]]) -> List:
    #     ''' return an array of objects matching the provided :ids: array. '''
        
    #     ids = [ObjectId(id) for id in ids]
    #     return sorted(self.find({"_id": {"$in": ids}}), key=lambda obj: ids.index(obj.id))
    
    # def await_update(self, id: ObjectId, timeout: int = 15):
    #     ''' wait for object with :id: to be updated in the database (or timeout). '''

    #     timeout = time() + timeout
    #     with self.collection.watch([{"$match": {"$and": [{"documentKey._id": ObjectId(id)}, {"operationType": "update"}]}}], full_document="updateLookup") as stream:
    #         while stream.alive:
    #             change = stream.try_next()
    #             if change is not None:
    #                 return self.object_type.from_bson(change["fullDocument"])
    #             elif timeout < time():
    #                 raise TimeoutError()
    #             elif stream.alive:
    #                 sleep(0.1)

