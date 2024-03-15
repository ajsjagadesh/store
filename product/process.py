from fastapi import APIRouter, FastAPI, HTTPException, Header, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key to sign JWT token
SECRET_KEY = "ajs-001-AB-001-1998-1997"


def get_token(authorization: str = Header(...)):
    scheme, token = authorization.split()
    if scheme.lower() != "bearer":
        return {
              "Error_code" : 401,
              "detail": "Invalid authentication scheme" }
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return { "user_name" : payload["sub"] }
    
    except JWTError:
        return {
              "Error_code" : 401,
              "detail": "Invalid token" }


   