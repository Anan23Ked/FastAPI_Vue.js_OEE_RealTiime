# # #check these comments for error

# # #in postgresql create col mobile and __v these column as bigint data as in mongodb mobile and __v are integers 


# # # in terminal run "pip install pymongo psycopg2 " 
# # # and "pip install pymongo psycopg2-pool"
# # # and "mongod --version"
# # # in  MongoDB connection settings change dbname and collection name as per ur database
# # # in PostgreSQL connection settings change dbname and user and password(of_user) as per ur database
# # # in def insert_into_postgres(data): 
# #     #same column name as postgesql   
# #     #cur.execute("SELECT 1 FROM 'your postgresql table name' WHERE id = %s", (_id,)) 
# #     #id is postgressql colname
# #     #_id is  default id given by mongodb

# #     #cur.execute("INSERT INTO your 'postgresql table name' (id, name, email, mobile,created, updated, v) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
# #     #default collumn names will in lower case and dont use keywords/reserved words as colname 
# #     #(id, document['name'], document['email'], document['mobile'], document['createdAt'], document['updatedAt'], document['_v'])) # document['name'] in this 'name' is from mongodb colllection not from postgresql
# #     # column name same as mongodb and correct _v to __v as double underscore will be removed
# # # in if name == "main": 
# #     # when copy paste double underscores are remove it should be name =="main":


# import psycopg2
# from psycopg2 import pool
# import pymongo
# from pymongo import MongoClient
# from bson import Code


# # MongoDB connection settings
# MONGO_HOST = 'localhost'
# # mongodb://Electrono:Elno%40560066@172.18.30.150:27018/%20authMechanism=DEFAULT&authSource=EFORCAST_CMTI?authSource=EFORCAST_CMTI
# MONGO_PORT = 27018
# MONGO_DB = 'EFORCAST_CMTI'
# MONGO_COLLECTION = 'Elno_MESData_new'

# # PostgreSQL connection settings
# POSTGRES_HOST = 'localhost'
# POSTGRES_PORT = 5432
# POSTGRES_DB = 'OEE'
# POSTGRES_USER = 'admin2'
# POSTGRES_PASSWORD = '1234'   #users password should be given not db

# # Connection pool settings
# connection_pool = pool.SimpleConnectionPool(
#     minconn=1,
#     maxconn=10,
#     host=POSTGRES_HOST,
#     port=POSTGRES_PORT,
#     dbname=POSTGRES_DB,
#     user=POSTGRES_USER,
#     password=POSTGRES_PASSWORD
# )

# # MongoDB data retrieval function
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



# # def get_keys(db, collection):
# #     client = MongoClient()
# #     db = client[db]
# #     map = Code("function() { for (var key in this) { emit(key, null); } }")
# #     reduce = Code("function(key, stuff) { return null; }")
# #     result = db[collection].map_reduce(map, reduce, "myresults")
# #     return result.distinct('_id')

# def get_keys_from_mongo_data(data):
#     keys = set()
#     for document in data:
#         keys.update(document.keys())
#     return list(keys)


# def insert_into_postgres(data):
#     print("Starting data insertion into PostgreSQL")
#     print(len(data))
#     conn = connection_pool.getconn()
#     try:
#         with conn.cursor() as cur:
#             for document in data:
#                 _id = str(document['_id'])  # Convert ObjectId to string before insertion
#                 try:
#                     # Check if document with the same _id already exists
#                     cur.execute("SELECT 1 FROM machine_data_mongodb WHERE id = %s", (_id,)) #same column name as postgesql
#                     existing_document = cur.fetchone()
#                     if existing_document:
#                         print(f"Skipping insertion for document {_id}: Already exists in the database")
#                         continue  # Skip insertion for existing document
#                     print("Inserting document:", _id)
#                     cur.execute("INSERT INTO machine_data_mongodb (id,createdDate,L1Name,plant,line,partNumber,machineName,startTime,EndTime,hour ,shift,actual,target,totalTime,availableTime,scheduledDowntime,updateDate,actualCycleTime,avaability,productionTime,cycle,cycleTime,fttLoss,fttComment,fttColor,oee,quality,targetNoDown,downTime,alram,totalLoss,totalSlowRunning,totalMicroStoppage,totalIdleTime,totalCycleTime,start,End,status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %d, %s, %d, %d,%d,  %d, %d, %s, %d, %f,%d, %d, %d, %f,%s, %s,%f,%d, %d, %d, %d, %d, %d, %d, %d, %s,%s,%b)", #default collumn names will in lower case and dont use keywords/reserved words as colname 
#                                 (id, document[createdDate],document[L1Name], document[plant], document[line], document[partNumber],document[machineName],document[startTime],document[EndTime],document[hour ],document[shift],document[actual],document[target],document[totalTime],document[availableTime],document[scheduledDowntime],document[updateDate],document[actualCycleTime],document[avaability],document[productionTime],document[cycle],document[cycleTime],document[fttLoss],document[fttComment],document[fttColor],document[oee],document[quality],document[targetNoDown],document[downTime],document[alram],document[totalLoss],document[totalSlowRunning],document[totalMicroStoppage],document[totalIdleTime],document[totalCycleTime],document[start],document[End],document[status], document['__v'])) #column name same as mongodb and correct _v to __v as double underscore will be removed
#                     print("Document inserted successfully:", _id)
#                 except psycopg2.Error as e:
#                     print(f"Error inserting document {_id}: {e}")
#                     conn.rollback()  # Rollback the transaction for the current document
#             try:
#     # Data insertion process
#                 conn.commit()  # Commit the transaction
#                 print("Transaction committed successfully")
#             except psycopg2.Error as e:
#                 print("Error committing transaction:", e)
#                 conn.rollback()  # Rollback the transaction if an error occurs



#         print("Inserted data into PostgreSQL")
#     except psycopg2.Error as e:
#         print("Error inserting data into PostgreSQL:", e)
#     finally:
#         connection_pool.putconn(conn)
#         print("Released PostgreSQL connection")


# # Data synchronization function
# def sync_data():
#     mongo_data = get_mongo_data()
#     print("Number of documents retrieved from MongoDB:", len(mongo_data))  # Print statement to display the number of documents retrieved
#     if mongo_data:
#         insert_into_postgres(mongo_data)

# # Main function
# if __name__ == "__main__": # when copy paste double underscores are remove it should be _name =="main":
#     sync_data()
#     # get_keys(MONGO_DB ,MONGO_COLLECTION )

# # # def get_mongo_data():
# # #     try:
# # #         client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
# # #         db = client[MONGO_DB]
# # #         collection = db[MONGO_COLLECTION]
# # #         print("Connected to MongoDB")
# # #         return list(collection.find())
# # #     except Exception as e:
# # #         print(f"Not connected to MongoDB: {e}")
# # #         return None

# # # # Function to get unique keys from the MongoDB documents
# # # def get_keys_from_mongo_data(data):
# # #     keys = set()
# # #     for document in data:
# # #         keys.update(document.keys())
# # #     return list(keys)

# # # # Function to create a PostgreSQL table with dynamic columns based on MongoDB keys
# # # def create_postgres_table(keys):
# # #     conn = connection_pool.getconn()
# # #     try:
# # #         with conn.cursor() as cur:
# # #             columns = ', '.join([f'"{key}" TEXT' for key in keys])  # Use TEXT for simplicity, adjust types as needed
# # #             create_table_query = f"CREATE TABLE IF NOT EXISTS machine_data_mongodb ({columns})"
# # #             cur.execute(create_table_query)
# # #             conn.commit()
# # #             print("PostgreSQL table created successfully")
# # #     except psycopg2.Error as e:
# # #         print("Error creating PostgreSQL table:", e)
# # #         conn.rollback()
# # #     finally:
# # #         connection_pool.putconn(conn)

# # # # Function to insert documents into the PostgreSQL table
# # # def insert_into_postgres(data, keys):
# # #     print("Starting data insertion into PostgreSQL")
# # #     conn = connection_pool.getconn()
# # #     try:
# # #         with conn.cursor() as cur:
# # #             for document in data:
# # #                 _id = str(document['_id'])  # Convert ObjectId to string before insertion
# # #                 try:
# # #                     cur.execute("SELECT 1 FROM machine_data_mongodb WHERE _id = %s", (_id,))
# # #                     existing_document = cur.fetchone()
# # #                     if existing_document:
# # #                         print(f"Skipping insertion for document {_id}: Already exists in the database")
# # #                         continue  # Skip insertion for existing document

# # #                     column_names = ', '.join([f'"{key}"' for key in keys])
# # #                     column_values = ', '.join(['%s' for _ in keys])
# # #                     insert_query = f"INSERT INTO machine_data_mongodb ({column_names}) VALUES ({column_values})"
# # #                     values = [str(document.get(key, '')) for key in keys]  # Convert values to strings for simplicity
# # #                     cur.execute(insert_query, values)
# # #                     print("Document inserted successfully:", _id)
# # #                 except psycopg2.Error as e:
# # #                     print(f"Error inserting document {_id}: {e}")
# # #                     conn.rollback()
# # #             try:
# # #                 conn.commit()
# # #                 print("Transaction committed successfully")
# # #             except psycopg2.Error as e:
# # #                 print("Error committing transaction:", e)
# # #                 conn.rollback()
# # #         print("Inserted data into PostgreSQL")
# # #     except psycopg2.Error as e:
# # #         print("Error inserting data into PostgreSQL:", e)
# # #     finally:
# # #         connection_pool.putconn(conn)
# # #         print("Released PostgreSQL connection")

# # # # Data synchronization function
# # # def sync_data():
# # #     mongo_data = get_mongo_data()
# # #     if mongo_data:
# # #         keys = get_keys_from_mongo_data(mongo_data)
# # #         create_postgres_table(keys)
# # #         insert_into_postgres(mongo_data, keys)
# # #         print("Number of documents retrieved from MongoDB:", len(mongo_data))

# # # # Main function
# # # if __name__ == "__main__":
# # #     sync_data()



# # def sync_data():
# #     mongo_data = get_mongo_data()
# #     if mongo_data:
# #         keys = get_keys_from_mongo_data(mongo_data)
# #         create_postgres_table(keys)
# #         insert_into_postgres(mongo_data, keys)
# #         print("Number of documents retrieved from MongoDB:", len(mongo_data))


#check these comments for error

#in postgresql create col mobile and __v these column as bigint data as in mongodb mobile and __v are integers 


# in terminal run "pip install pymongo psycopg2 " 
# and "pip install pymongo psycopg2-pool"
# and "mongod --version"
# in  MongoDB connection settings change dbname and collection name as per ur database
# in PostgreSQL connection settings change dbname and user and password(of_user) as per ur database
# in def insert_into_postgres(data): 
    #same column name as postgesql   
    #cur.execute("SELECT 1 FROM 'your postgresql table name' WHERE id = %s", (_id,)) 
    #id is postgressql colname
    #_id is  default id given by mongodb

    #cur.execute("INSERT INTO your 'postgresql table name' (id, name, email, mobile,created, updated, v) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
    #default collumn names will in lower case and dont use keywords/reserved words as colname 
    #(id, document['name'], document['email'], document['mobile'], document['createdAt'], document['updatedAt'], document['_v'])) # document['name'] in this 'name' is from mongodb colllection not from postgresql
    # column name same as mongodb and correct _v to __v as double underscore will be removed
# in if name == "main": 
    # when copy paste double underscores are remove it should be name =="main":


import psycopg2
from psycopg2 import pool
import pymongo

# MongoDB connection settings
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'OEE1'
MONGO_COLLECTION = 'users'

# PostgreSQL connection settings
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_DB = 'OEE2'
POSTGRES_USER = 'admin2'
POSTGRES_PASSWORD = 'admin2'   #users password should be given not db

# Connection pool settings
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)

# MongoDB data retrieval function
def get_mongo_data():
    try:
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        print("Connected to MongoDB")
        return list(collection.find())
    except Exception as e:
        print(f"Not connected to MongoDB: {e}")
        return None



def insert_into_postgres(data):
    print("Starting data insertion into PostgreSQL")
    print(len(data))
    conn = connection_pool.getconn()
    try:
        with conn.cursor() as cur:
            for document in data:
                _id = str(document['_id'])  # Convert ObjectId to string before insertion
                try:
                    # Check if document with the same _id already exists
                    cur.execute("SELECT 1 FROM machine_data_mongodb WHERE id = %s", (_id,)) #same column name as postgesql
                    existing_document = cur.fetchone()
                    if existing_document:
                        print(f"Skipping insertion for document {_id}: Already exists in the database")
                        continue  # Skip insertion for existing document
                    print("Inserting document:", _id)
                    cur.execute("INSERT INTO machine_data_mongodb (id, name, email, mobile,created, updated, v) VALUES (%s, %s, %s, %s, %s, %s, %s)", #default collumn names will in lower case and dont use keywords/reserved words as colname 
                                (id, document['name'], document['email'], document['mobile'], document['createdAt'], document['updatedAt'], document['__v'])) #column name same as mongodb and correct _v to __v as double underscore will be removed
                    print("Document inserted successfully:", _id)
                except psycopg2.Error as e:
                    print(f"Error inserting document {_id}: {e}")
                    conn.rollback()  # Rollback the transaction for the current document
            try:
    # Data insertion process
                conn.commit()  # Commit the transaction
                print("Transaction committed successfully")
            except psycopg2.Error as e:
                print("Error committing transaction:", e)
                conn.rollback()  # Rollback the transaction if an error occurs



        print("Inserted data into PostgreSQL")
    except psycopg2.Error as e:
        print("Error inserting data into PostgreSQL:", e)
    finally:
        connection_pool.putconn(conn)
        print("Released PostgreSQL connection")


# Data synchronization function
def sync_data():
    mongo_data = get_mongo_data()
    print("Number of documents retrieved from MongoDB:", len(mongo_data))  # Print statement to display the number of documents retrieved
    if mongo_data:
        insert_into_postgres(mongo_data)

# Main function
if _name_ == "_main": # when copy paste double underscores are remove it should be _name =="main":
    sync_data()