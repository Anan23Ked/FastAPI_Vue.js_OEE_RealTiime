# run every 5 seconds
# check for changes wrt to time
import threading
from sqlalchemy import Column, Integer, Float, Boolean, String, Table
from database.config import MONGO_COLLECTION, SessionLocal, get_mongo_data
from database.config import metadata, engine, get_db

db=SessionLocal()

def MTLINKiData(created_tables):
    # while True:
    # for collection in MONGO_COLLECTION:
    #     if f"MTLINKi_{collection}" in created_tables:
    #         continue
    #     else: 
    #         tableCreation(collection)

    #     watcher_thread = threading.Thread(target=changeLookup, args=(collection, created_tables[f"MTLINKi_{collection}"] ))
    #     watcher_thread.daemon = True
    #     watcher_thread.start()
    # return {"done"}



    mongo_data = get_mongo_data()
    if mongo_data:
        for collection in mongo_data.items():
            if collection.collection_name not in created_tables:
                print("push to table creation")
                tableCreation(collection)
            else:
                watcher_thread = threading.Thread(target = changeLookup, args=(collection,created_tables ))
                watcher_thread.daemon= True
                watcher_thread.start()

   
def tableCreation(collection):
    created_tables = {}
    table_name = f"MTLINKi_{collection}"
    print("Table name", table_name)

    columns=[Column('id', Integer, primary_key = True, autoincrement = True)]
    for key, value in collection.items():
        if key == '_id' :
            continue
        if isinstance(value, int):
                column_type = Integer
        elif isinstance(value, float):
            column_type = Float
        elif isinstance(value, bool):
            column_type = Boolean
        else:
            column_type = String 
        columns.append(Column(key, column_type))

    table = Table(table_name, metadata, *columns)
    created_tables[table_name] = table
    metadata.create_all(bind=engine)   # Create table in db
    metadata.reflect(bind=engine)
   

    if db.query(table).first()== None:
        insert(collection, created_tables)

    print("tablecreation done")
    return created_tables, table


def insert(collection, table):
    db.execute(table.insert().values({k: v for k, v in collection.items() if k != '_id'}))
    db.commit()
    print("insertion of colllection done")
    
def insert_document(change_event_document, collection,table):
    db.execute(table.insert().values({k:v for k, v in change_event_document.items() if k == key for key in collection.items()}))
    db.commit()
    print(" change_event_document inserted")
    return

def changeLookup(collection, table):
    try:
        with collection.watch() as stream: #collection.watch() opens a change stream for surrent collection
            for change in stream:
                if change['operationType'] == 'insert':
                    change_event_document = change['fullDocument']
                    # table = metadata.tables.get(table_name)
                    insert_document(change_event_document, collection, table)
                    print("changeLookup")
    except Exception as e:
        print("Error at change Lookup", {e})


# def start_change_stream_listener():
#     db_new = next(get_db())
#     watcher_thread = threading.Thread(target=watch_mongo_changes, args=(db_new))
#     watcher_thread.daemon = True
#     watcher_thread.start()