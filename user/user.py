from fastapi import APIRouter, FastAPI, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

from .BaseModels import user_login, user_reg, user_data, remove_user
from connect import SessionLocal, engine
from . import curd
from .models import User_Reg
from .process import create_access_token

from auth import Token, User, authenticate_user, create_access_token, get_current_active_user, fake_users_db, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter, FastAPI, HTTPException, Header, Depends, status
# Token expiration time (in minutes)
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Secret key to sign JWT token
# SECRET_KEY = "ajs-001-AB-001-1998-1997"

user = FastAPI()
router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@user.post("/token")
async def login_for_access_token( form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(SessionLocal(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# Login route
@user.post("/login")
def login(user_login : user_login, db: Session = Depends(get_db)):
    login_result = curd.get_login_user(db, user_login)
    if login_result:
        USERNAME, PASSWORD, EMAIL = login_result
        if user_login.email == EMAIL and user_login.password == PASSWORD:
            # Create JWT token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": USERNAME}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Incorrect username or password")
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
# new_user route
@user.post("/user", response_model=user_reg)
def create_user(user_data : user_data, db: Session = Depends(get_db)):
    email_check = curd.get_user_by_email(db, email=user_data.email)
    mobile_no_check = curd.get_user_by_mobile(db, mobile=user_data.mobile_number)
    if email_check:
        raise HTTPException(status_code=400, detail="Email already registered")
    if mobile_no_check:
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    
    return curd.create_user(db=db, user=user_data)


@user.delete("/user", response_model=user_reg)
def delete_user(user_details : remove_user, db: Session = Depends(get_db)):
    user = curd.get_user_with_email_and_no(db, email=user_details.email, mobile=user_details.mobile_number)
    if user:
        curd.delete_user(db, email=user_details.email)
        return user 
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
    
@user.put("/user", response_model=user_reg)
def update_user(user_details : user_data, db: Session = Depends(get_db)):
    user = curd.update_user(db, user_details)
    if user:
        return user 
    else:
        raise HTTPException(status_code=404, detail="User not found")

user.include_router(router)






