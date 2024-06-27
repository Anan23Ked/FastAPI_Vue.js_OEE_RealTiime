# import psycopg2
# from psycopg2 import pool
# from config import URL_Database
# from database.config import get_mongo_data, get_keys_from_mongo_data


# # Connection pool settings
# connection_pool = pool.SimpleConnectionPool(
#     minconn=1,
#     maxconn=10,
#     host=URL_Database
# )

# def create_postgres_table(keys):
#     conn = connection_pool.getconn()
#     try:
#         with conn.cursor() as cur:
#             columns = ', '.join([f'"{key}" TEXT' for key in keys])  # Use TEXT for simplicity, adjust types as needed
#             create_table_query = f"CREATE TABLE IF NOT EXISTS machine_data_mongodb ({columns})"
#             cur.execute(create_table_query)
#             conn.commit()
#             print("PostgreSQL table created successfully")
#     except psycopg2.Error as e:
#         print("Error creating PostgreSQL table:", e)
#         conn.rollback()
#     finally:
#         connection_pool.putconn(conn)

# def insert_into_postgres(data, keys):
#     print("Starting data insertion into PostgreSQL")
#     conn = connection_pool.getconn()
#     try:
#         with conn.cursor() as cur:
#             for document in data:
#                 _id = str(document['_id'])  # Convert ObjectId to string before insertion
#                 try:
#                     cur.execute("SELECT 1 FROM machine_data_mongodb WHERE _id = %s", (_id,))
#                     existing_document = cur.fetchone()
#                     if existing_document:
#                         print(f"Skipping insertion for document {_id}: Already exists in the database")
#                         continue  # Skip insertion for existing document

#                     column_names = ', '.join([f'"{key}"' for key in keys])
#                     column_values = ', '.join(['%s' for _ in keys])
#                     insert_query = f"INSERT INTO machine_data_mongodb ({column_names}) VALUES ({column_values})"
#                     values = [str(document.get(key, '')) for key in keys]  # Convert values to strings for simplicity
#                     cur.execute(insert_query, values)
#                     print("Document inserted successfully:", _id)
#                 except psycopg2.Error as e:
#                     print(f"Error inserting document {_id}: {e}")
#                     conn.rollback()
#             try:
#                 conn.commit()
#                 print("Transaction committed successfully")
#             except psycopg2.Error as e:
#                 print("Error committing transaction:", e)
#                 conn.rollback()
#         print("Inserted data into PostgreSQL")
#     except psycopg2.Error as e:
#         print("Error inserting data into PostgreSQL:", e)
#     finally:
#         connection_pool.putconn(conn)
#         print("Released PostgreSQL connection")


# def sync_data():
#     mongo_data = get_mongo_data()
#     if mongo_data:
#         keys = get_keys_from_mongo_data(mongo_data)
#         create_postgres_table(keys)
#         insert_into_postgres(mongo_data, keys)
#         print("Number of documents retrieved from MongoDB:", len(mongo_data))