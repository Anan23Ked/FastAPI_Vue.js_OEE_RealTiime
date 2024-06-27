# original


import threading
# from fastapi import Depends
# import pymongo
# import sqlalchemy

from sqlalchemy.orm import Session
from database.config import MONGO_COLLECTION, MONGO_DB, Mongo_URL, get_db, get_mongo_data, metadata
# from database.models import insertData
from database.dataCollector.insert import insertData

# insertion
def migrate_data(document,db: Session, table):
    mongo_data = get_mongo_data()
    
    if mongo_data:
        # for new_document in mongo_data:
        #     db.execute(table.insert().values({k: v for k, v in new_document.items() if k != '_id'}))
        #     db.commit()
        #     print("Updated data inserted")
        table_created = False
        table = None
        for document in mongo_data:
            if not table_created:
                for i in range(len(MONGO_COLLECTION)):
                    MONGO_COLLECTION[i] = document.get('collection', 'default')
                table = insertData(document, db)
                # table = created_tables
                print("table type", type(table))
                table_created = True
            
            db.execute(table.insert().values({k: v for k, v in document.items() if k != '_id'}))
            db.commit()
            print("updated data inserted")

# new data pass
def handle_new_data(change, db, table):
    document = change['fullDocument']
    for i in range(len(MONGO_COLLECTION)):
        MONGO_COLLECTION[i] = change['ns']['coll']
    
    migrate_data(document, db, table)

# Watch for changes in MongoDB
def watch_mongo_changes(db_new):
    try:
         for i in range(len(MONGO_COLLECTION)):
            collection = db_new[ MONGO_COLLECTION[i] ]
            print("Hi collection",MONGO_COLLECTION[i])
            with collection.watch() as stream:
                for change in stream:
                    if change['operationType'] == 'insert':
                        # db_session = next(get_db())
                        table_name = f"MTLINKi_{MONGO_COLLECTION[i]}"
                        table = metadata.tables.get(table_name)
                        if not table:
                            document = change['fullDocument']
                            table = insertData(document, db_new)
                        handle_new_data(change, db_new, table)
                        db_new.close()
    except Exception as e:
        print(f"Error watching MongoDB: {e}")

# def watch_mongo_changes():
#     client = pymongo.MongoClient(Mongo_URL)
#     db = client[MONGO_DB]
#     try:
#         for collection_name in MONGO_COLLECTION:
#             collection = db[collection_name]
#             print("Watching collection:", collection_name)
#             with collection.watch() as stream:
#                 for change in stream:
#                     if change['operationType'] == 'insert':
#                         db_session = next(get_db())
#                         table_name = f"MTLINKi_{collection_name}"
#                         table = metadata.tables.get(table_name)
#                         # if not table:
#                         #     document = change['fullDocument']
#                             # table = insertData(document, db_session)
#                         handle_new_data(change, db_session, table)
#                         # db_session.close()
#     except Exception as e:
#         print(f"Error watching MongoDB: {e}")


def start_change_stream_listener():
    db_new = next(get_db())
    watcher_thread = threading.Thread(target=watch_mongo_changes, args=(db_new))
    watcher_thread.daemon = True
    watcher_thread.start()
