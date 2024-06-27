from sqlalchemy import Column, Integer, Float, Boolean, String, Table
from sqlalchemy.orm import Session
from database.config import metadata, engine
# from database.dataCollector.migrate import start_change_stream_listener

def insertData(new_document, db: Session):
    created_tables = {}
    collection_name = new_document.get('collection_name')  # Assuming collection name is passed in document
    table_name = f"MTLINKi_{collection_name}"
    print("Table name", table_name)

    if table_name not in metadata.tables:
        columns = [Column('id', Integer, primary_key=True, autoincrement=True)]
        for key, value in new_document.items():
            if key == '_id' or key == 'collection_name':
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
        metadata.create_all(bind=engine)   # Create table in db
        metadata.reflect(bind=engine)
        created_tables[table_name] = table
    else:
        created_tables[table_name] = metadata.tables[table_name]

    # migrate_data(document, db, created_tables[table_name])
    # start_change_stream_listener()
    return created_tables
