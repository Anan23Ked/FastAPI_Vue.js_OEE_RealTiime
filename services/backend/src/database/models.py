
from sqlalchemy import Table,Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database.config import MONGO_COLLECTION, Base, get_mongo_data, metadata, engine
from database.dataCollector.migrate import migrate_data

class Machine(Base):
    __tablename__ = 'machine'
    machine_id = Column(String, primary_key=True, index=True)
    machine_name = Column(String, index=True)
    is_selected = Column(Boolean, default=False)

    # Relationship to OEE and Status
    oee_records = relationship("Parameters", back_populates="machine")
    status_records = relationship("Status", back_populates="machine")

class Parameters(Base):
    __tablename__ = 'parameters'
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, ForeignKey("machine.machine_id"))
    availability = Column(Float)
    performance = Column(Float)
    quality = Column(Integer)

    machine = relationship("Machine", back_populates="oee_records")

class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, ForeignKey("machine.machine_id"))
    is_running = Column(Boolean)
    running_hours = Column(Float, default=0.0)
    is_off = Column(Boolean)
    off_hours = Column(Float, default=0.0)
    is_idle = Column(Boolean)
    idle_hours = Column(Float, default=0.0)
    is_maintenance = Column(Boolean)
    maintenance_hours = Column(Float, default=0.0)

    machine = relationship("Machine", back_populates="status_records")

class User(Base):
    __tablename__="user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True) 
    password = Column(String(200))
    email = Column(String(100))
    category = Column(String(20))
    is_admin=Column(Boolean)

# class Test2(Base):
#     __tablename__="test2"
#     id = Column(Integer, primary_key=True, index=True)
#     name= Column(Integer)

# class ReasonCodes(Base):
#     __tablename__="reasoncodes"
#     id = Column(Integer, primary_key=True, index=True)
#     reasonName = Column(String)
#     reasonColor = Column(String)
#     unit = Column(Integer)
#     value = Column(Integer)
#     comment  = Column(String)

#     mongoDBMachine = relationship('MongoDBDataMES', back_populates='reasoncodes')

class MongoDBDataMES(Base):
    __tablename__="mongoDBDataMES"
    id=Column(String, primary_key=True, index= True)
    createdDate =Column(DateTime)
    L1Name = Column(String)
    plant = Column(String)
    line= Column(String)
    partNumber= Column(String)
    machineName= Column(String)
    startTime=Column(DateTime)
    EndTime=Column(DateTime)
    hour = Column(Integer)
    shift= Column(String)
    actual= Column(Integer)
    target= Column(Integer)
    totalTime= Column(Integer)
    availableTime= Column(Integer)
    scheduledDowntime= Column(Integer)
    updateDate=Column(DateTime)
    actualCycleTime= Column(Integer)
    availability= Column(Float)
    productionTime= Column(Integer)
    cycle= Column(Integer)
    cycleTime= Column(Integer)
    fttLoss= Column(Float)
    fttComment= Column(String)
    fttColor= Column(String)
    oee= Column(Float)
    quality= Column(Integer)
    targetNoDown= Column(Integer)
    downTime= Column(Integer)
    alram= Column(Integer)
    totalLoss= Column(Integer)
    totalSlowRunning= Column(Integer)
    totalMicroStoppage= Column(Integer)
    totalIdleTime= Column(Integer)
    totalCycleTime= Column(Integer)
    start=Column(DateTime)
    End=Column(DateTime)
    status = Column(Boolean)
# ftch
    # reasoncode_id = Column(Integer, ForeignKey('reasoncodes.id'))

    # reasoncodes = relationship("ReasonCodes", back_populates="mongoDBMachine")
# ReasonCodes.mongoDBMachine = relationship('MongoDBDataMES', order_by=MongoDBDataMES.id, back_populates='reasoncodes')

# def MTLINKistatus(document, db):
#     columns = [Column('id', Integer, primary_key= "True", autoincrement = True)]
#     for key, value  in document.items():
#         if key =='_id':
#             continue
#         if isinstance(value, int):
#             column_type = Integer
#         elif isinstance(value, float):
#             column_type = Float
#         elif isinstance(value, bool):
#             column_type = Boolean
#         else:
#             column_type = String
#         columns.append(Column(key, column_type))

#     table = Table('MTLINKi_status',  metadata, *columns)
#     metadata.create_all(bind=db.get_bind())
#     return table

# def MTLINKistatus_Opened(document, db):
#     columns = [Column('id', Integer, primary_key= "True", autoincrement = True)]
#     for key, value  in document.items():
#         if key =='_id':
#             continue
#         if isinstance(value, int):
#             column_type = Integer
#         elif isinstance(value, float):
#             column_type = Float
#         elif isinstance(value, bool):
#             column_type = Boolean
#         else:
#             column_type = String
#         columns.append(Column(key, column_type))

#     table = Table('MTLINKistatus_Opened',  metadata, *columns)
#     metadata.create_all(bind=db.get_bind())
#     return table
    

# def MTLINKi_L1Signal_Pool_Active(document, db):
#     columns = [Column('id', Integer, primary_key= "True", autoincrement = True)]
#     for key, value  in document.items():
#         if key =='_id':
#             continue
#         if isinstance(value, int):
#             column_type = Integer
#         elif isinstance(value, float):
#             column_type = Float
#         elif isinstance(value, bool):
#             column_type = Boolean
#         else:
#             column_type = String
#         columns.append(Column(key, column_type))

#     table = Table('MTLINKi_L1Signal_Pool_Active',  metadata, *columns)
#     metadata.create_all(bind=db.get_bind())
#     return table
   
# table  creation
# def insertData(document,db):
    # created_tables = {}
    # for i in range(len(MONGO_COLLECTION)):
    #     table_name = f"MTLINKi_{MONGO_COLLECTION[i]}"
    #     print("Table name", table_name)
    #     print("Lenfgth0", len(MONGO_COLLECTION))
    #     # print("metadata.tables", metadata.tables)

    #     if table_name not in metadata.tables:
    #         # mongo_data = get_mongo_data()
    #         # if document in mongo_data:
    #         columns = [Column('id', Integer, primary_key= True, autoincrement = True)]
    #         for key, value  in document.items():
    #             if key =='_id':
    #                 continue
    #             if isinstance(value, int):
    #                 column_type = Integer
    #             elif isinstance(value, float):
    #                 column_type = Float
    #             elif isinstance(value, bool):
    #                 column_type = Boolean
    #             else:
    #                 column_type = String
    #             columns.append(Column(key, column_type))

    #         table = Table(table_name,  metadata, *columns)
    #         metadata.create_all(bind=engine)   #create table in db
    #         metadata.reflect(bind=engine)
    #         # metadata.tables.append(table_name)
    #         created_tables[table_name] = table
    #     else:       
    #         print("Type of metadata table", type(metadata.tables[table_name]))
    #         # print("meta added table", metadata.tables[table_name])
    #         created_tables[table_name] = metadata.tables[table_name]
            
    #     migrate_data(document, db, created_tables[table_name])
    #     return created_tables