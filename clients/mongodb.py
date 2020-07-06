""" This module provides a MongoDB object that serves a connection to various collections """

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
    
    ''' A MongoDB client that interfaces to different MongoCollection instances,
        allowing for easy access into the database.
    '''
    
    def __init__(self):
        
        MONGO_URI = "mongodb+srv://{}:{}@{}".format(os.environ["MONGO_USERNAME"],os.environ["MONGO_PASSWORD"],os.environ["MONGO_HOST"])

        mongo_client = pymongo.MongoClient(MONGO_URI, ssl_cert_reqs=ssl.CERT_NONE)
        self.mongo_client = mongo_client
        
        # collections
        self.transactions = MongoCollection(self.mongo_client, "transactions")
        self.customers = MongoCollection(self.mongo_client, "customers")
    
    def __enter__(self) -> "MongoDB":
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mongo_client.__exit__(exc_type, exc_val, exc_tb)


class MongoCollection:
    
    ''' This class controls the interaction in MongoDB. '''
    
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

    
    def find_by_id(self, id: Union[str, ObjectId]):
        ''' return a single object matching :id:. '''
        
        return self.find_one({"_id": ObjectId(id)})

