

# import DateTime
from datetime import datetime
from pydantic import BaseModel
from typing import List

class ParametersBase(BaseModel):
    availability : float
    performance : float 
    quality:int

class StatusBase(BaseModel):
    is_running :bool
    running_hours: float
    is_off : bool
    off_hours: float = 0.0
    is_idle:bool
    idle_hours: float = 0.0
    is_maintenance : bool
    maintenance_hours: float = 0.0

class MachineBase(BaseModel):
    machine_id:str
    machine_name:str
    is_selected : bool
    status_records: List[StatusBase]
    oee_records :List[ParametersBase]

class UserBase(BaseModel):
    username:str
    password = str
    email = str
    category =str
    is_admin=bool

class ReasonCodesBase(BaseModel):
    id: str
    reasonName : str
    reasonColor: str
    unit:int
    value :int
    comment : str

class MongoDBDataMESBase(BaseModel):
    id: str
    createdDate :datetime
    L1Name : str
    plant : str
    line: str
    partNumber: str
    machineName: str
    startTime:datetime
    EndTime:datetime
    hour:int
    shift: str
    actual:int
    target:int
    totalTime:int
    availableTime:int
    scheduledDowntime:int
    updateDate:datetime
    actualCycleTime:int
    availability: float
    productionTime:int
    cycle:int
    cycleTime:int
    fttLoss: float
    fttComment: str
    fttColor: str
    oee: float
    quality:int
    targetNoDown:int
    downTime:int
    alram:int
    totalLoss:int
    totalSlowRunning:int
    totalMicroStoppage:int
    totalIdleTime:int
    totalCycleTime:int
    start:datetime
    End:datetime
    status:bool
    reasoncodes = List[ReasonCodesBase]


