from pydantic import BaseModel, EmailStr

class user_reg(BaseModel):
    user_name: str
    email: EmailStr
    mobile_number: str
    address: str
    pincode: int
    land_mark: str

class user_data(user_reg):
     password: str 

class user_login(BaseModel):
    email: EmailStr
    password: str

class remove_user(BaseModel):
    user_name: str
    mobile_number: str
    email: EmailStr

 
 
