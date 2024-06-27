
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from auth import oauth2_scheme,OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.config import get_db
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.users import create_user, delete_user, is_admin, authenticate_user, create_access_token, decode_access_token
from operations.oee import oee_calculation



router = APIRouter(prefix="/SMW", tags=["OEE"])

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/SMW/login")

@router.post("/users/")
async def create_new_user(username: str, password: str, email: str, category: str, db:Session = Depends(get_db)):
    try:
        create_user(username, password, email, category)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Set token expiration time
    access_token_expires = timedelta(minutes=30)
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "is_admin": user.is_admin, "message": "Login successful"}

@router.delete("/users/{user_id}")
async def remove_user(user_id: int, token: str = Depends(is_admin), db:Session = Depends(get_db)):
    try:
        delete_user(user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @router.get("/home{machine_id}", response_model=MachineBase)
# def get_machine(machine_id:str, db:Session=Depends(get_db)):
#     db_machine = db.query(Machine).filter(machine_id == machine_id)[0]
#     if db_machine is None:
#         raise HTTPException(status_code=404, detail="Machine not found")
#     return {db_machine}

@router.get("/machine/{machineClicked}")
def get_machine(machineClicked : str):
    oee_res = oee_calculation(machineClicked)
    # print(oee_res)
    # return{"clicked machine from backend is" : oee_res}
    return{"machine clicked frombackend": machineClicked, "oee result frtom backend": oee_res}

