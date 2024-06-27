from fastapi import Depends
from sqlalchemy.orm import Session
from database.config import SessionLocal, get_db
from database.models import MongoDBDataMES

# , 
def oee_calculation(machineClicked:str, db:Session=Depends(get_db)):

    # selected_machine =wjhere date == selected date
    # sync calender date and  stored postgres date
    
    db = SessionLocal()
    machine = db.query(MongoDBDataMES).filter(MongoDBDataMES.machineName==machineClicked,
                                              MongoDBDataMES.createdDate ==  "2024-06-01 00:00:00").all()
    # print("machine data in terminal output=", machine)
    availability = sum(item.availability for item in machine)
    quality = sum(item.quality for item in machine)
    performance = sum(item.actual for item in machine) / sum(item.target for item in machine)
    oee = (availability * quality )+performance
   
    return {"oee": oee}

# mongodb://Electrono:Elno%40560066@172.18.30.150:27018/%20authMechanism=DEFAULT&authSource=EFORCAST_CMTI?authSource=EFORCAST_CMTI
# mongodb://CMTI:CMTI1234@172.18.30.150:27017/?authSource=MTLINKi