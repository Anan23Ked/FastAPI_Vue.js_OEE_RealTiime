from fastapi import Depends, HTTPException
from database.models import User
from database.config import get_db
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from auth import oauth2_scheme
import secrets
import logging
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


# Creating a passlib context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate a strong, randomly generated secret key for JWT token
SECRET_KEY = secrets.token_urlsafe(32)

# Algorithm for JWT token
ALGORITHM = "HS256"

# Token expiration time (e.g., 30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Function to verify the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to authenticate user
def authenticate_user(username: str, password: str, db:Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to decode JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# @Session
def create_user(username: str, password: str,  email: str, category: str, db:Session):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create the user with is_admin set to False
    user = User(
        username=username,
        password=hashed_password,
        email=email,
        category=category,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Function to check if user is admin
def is_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="User does not have admin privileges")


# @Session
def delete_user(user_id: int,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()  # Commit the transaction after deletion
