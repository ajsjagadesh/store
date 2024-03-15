from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key to sign JWT token
SECRET_KEY = "ajs-001-AB-001-1998-1997"

# Token creation function
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt