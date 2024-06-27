from fastapi import Depends
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import pymongo
from typing import Annotated, List


# Postgres
URL_Database = "postgresql://postgres:1234@localhost:5432/OEE"

# engine object that connects to the database
engine = create_engine(URL_Database)

# creates SQLAlchemy Session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# help routes acces database session
db_dependency = Annotated[Session, Depends(get_db)]

# container object that stores elements of a database such as table, colums, datatype...
metadata = MetaData()   


# Mongodb
# MONGO_HOST = 'localhost'
# MONGO_PORT = 27017
MONGO_DB = 'MTLINKi'
MONGO_COLLECTION = ['L1_Pool','L1_Pool_Opened','L1Signal_Pool_Active','L1Signal_Pool']
# MONGO_COLLECTION_Active = 'L1_Pool_Opened'
# MONGO_COLLECTION_L1Signal_Pool_Active = 'L1_Pool_Opened'
Mongo_URL = "mongodb://CMTI:CMTI1234@172.18.30.150:27017/?authSource=MTLINKi"

# connects to mongodb and checks if specified collection exists
# def get_mongo_data():
#     try:
#         client = pymongo.MongoClient(Mongo_URL)
#         db = client[MONGO_DB]
#         for i in range(len(MONGO_COLLECTION)):
#             # collection_name stores collect
#             collection_name = db[ MONGO_COLLECTION[i] ]
#             print("Connected to MongoDB")
#             return list(collection_name.find())
#     except Exception as e:
#         print(f"Not connected to MongoDB: {e}")
#         return None

def get_mongo_data():
    try:
        client = pymongo.MongoClient(Mongo_URL)
        db = client[MONGO_DB]
        data = {}
        for collection_name in MONGO_COLLECTION:
            #access specific collection within database
            collection = db[collection_name]
            data[collection_name] = list(collection.find())
        print("Connected collectyion type", type(collection))
        print("data from config", type(data))
        # print("data[0] from config", data[0])
        print("data collection value from config", type(data[collection_name]))
        print("collection type from config", type(collection.find()))
        return data, collection
    except Exception as e:
        print(f"Not connected to MongoDB: {e}")
        return None

# def get_mongo_data():
#     try:
#         client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
#         db = client[MONGO_DB]
#         collection = db[MONGO_COLLECTION]
#         print("Connected to MongoDB")
#         return list(collection.find())
#     except Exception as e:
#         print(f"Not connected to MongoDB: {e}")
#         return None

