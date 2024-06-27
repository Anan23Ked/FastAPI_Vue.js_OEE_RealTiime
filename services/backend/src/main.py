
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.models import MongoDBDataMES, User
from database.config import MONGO_COLLECTION, engine, SessionLocal, Base
from passlib.context import CryptContext
from routes.routes import router
from routes import items
from alembic import command
from alembic.config import Config as AlembicConfig
import logging
from sqlalchemy.orm import Session

# from database.dataCollector.insert import insertData
from database.config import get_db, get_mongo_data
from operations.oee import oee_calculation 
# from database.dataCollector.migrate import migrate_data, start_change_stream_listener
from database.MTLINKi.mtlinki import MTLINKiData,tableCreation


app = FastAPI()

app.include_router(router)
app.include_router(items.router)


def run_migrations():
    alembic_cfg = AlembicConfig("alembic.ini")
    command.upgrade(alembic_cfg, "head")

logger = logging.getLogger(__name__)
# Create the database tables
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # start_change_stream_listener()
    create_admin()

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

origins=[
    "http://localhost:8080",
    "http://localhost:8081",
    'http://localhost:5173',
    "http://localhost:5173/",
    "https://localhost"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers = ["*"],
    
)


def create_admin():
    db = SessionLocal()
    try:
        logger.info("Checking for existing admin user")
        admin = db.query(User).filter(User.is_admin == True).first()
        if not admin:
            logger.info("No admin user found, creating one")
            hashed_password = pwd_context.hash("password")  # Hash the default password
            admin = User(
                username="admin",
                password=hashed_password,
                email="admin@example.com",
                category = "OEE",
                is_admin=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            logger.info("Admin user created successfully")
        else:
            logger.info("Admin user already exists")
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        raise HTTPException(status_code=500, detail = str(e))
    finally:
        db.close()
    
@app.get("/")
def root():
    print("root")
    return {"msg":"Hello from backend"}

# @app.get("/migrate")
# def migrate_endpoint(db: Session = Depends(get_db)):
#     db = SessionLocal()
#     # table = insertData(document, db)
#     insertData(document, db)
#     new_document= insertData(new_document, db)
#     created_tables = insertData()
#     migrate_data(new_document,db,created_tables)
    

#     return {"message": "Migration complete"}

@app.get("/migrateee")
def migrateData_end():
    mongo_data = get_mongo_data()
    if not mongo_data:
        return {"message": "No data retrieved from MongoDB"}
    else:
        created_tables={}
        for collection in MONGO_COLLECTION:
            created_tables = tableCreation(collection)
            if f"MTLINKi_{collection}" in created_tables:
        
                MTLINKiData(created_tables)
     

# @app.get("/migrate")
# def migrate_endpoint(db: Session = Depends(get_db)):
#     mongo_data = get_mongo_data()
#     if not mongo_data:
#         return {"message": "No data retrieved from MongoDB"}

#     created_tables = {}
#     for collection_name, documents in mongo_data.items():
#         for document in documents:
#             # Add collection name to document to be used in insertData
#             document['collection_name'] = collection_name
#             created_tables = insertData(document, db)
#             migrate_data(document, db, created_tables[f"MTLINKi_{collection_name}"])
#             # start_change_stream_listener()
#     return {"message": "Migration complete"}

# @app.get("/machine/{machineClicked}")
# def get_machine(machineClicked: str):
#     db = SessionLocal()
#     # write query here
#     try:
#         machine = db.query(MongoDBDataMES).filter(MongoDBDataMES.machineName== machineClicked,
#                                                 MongoDBDataMES.createdDate == "2024-06-01 00:00:00").all()
#         # logging.info("mcv450 machine-",machine)
#     # print("machine detail", machine)
#     # machine = next((m for m in machines if m["id"] == machine_id), None)
#         if machine is None:
#             raise HTTPException(status_code=404, detail="Machine not found")
#         logging.info(f"mcv450 machine is: {machine}")
#         print("mcv450 machine detail", machine)
    
#         oee_res = oee_calculation(machine, db)
#         return oee_res
#     finally:
#         db.close()


@app.get("/machine/{machineClicked}")
def get_machine(machineClicked : str):
    oee_res = oee_calculation(machineClicked)
    # print(oee_res)
    # return{"clicked machine from backend is" : oee_res}
    return{"machine clicked from main backend": machineClicked, "oee result frtom backend": oee_res}





# @app.get("/mongodb")
# def get_mongo_data(client:mongo_dependency):
#     try:
#         mongodb = client[MONGO_DB]
#         collection = mongodb[MONGO_COLLECTION]
#         data = list(collection.find())
#         return {"mongo hello", data}
#     except Exception as e:
#         raise HTTPException(status_code = 500, details = f"Error retrieving data from mongodb: {e}")

# db = SessionLocal()
# new_machine = Machine(machine_id = "5", machine_name="machine5", is_selected=True) 
# db.add(new_machine)
# db.commit()
# db.refresh(new_machine)
# print(new_machine.machine_name) 

# @app.get("/unique-keys/")
# def get_unique_keys(db: Session = Depends(get_db)):
#     # Use SQLAlchemy to get distinct keys
#     query = db.query(MongoDBDataMES.key).distinct()
#     keys = [row.key for row in query.all()]
#     return keys@app.get("/sync")


# @app.get("/sync")
# def sync():
#     sync_data()
#     return {"message": "Data synchronization completed"}




