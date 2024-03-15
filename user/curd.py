from sqlalchemy.orm import Session
from . import models, BaseModels
import bcrypt


def get_login_user(db: Session, user_cred: BaseModels.user_login):
    db_user = db.query(models.User_Reg).filter(models.User_Reg.email == user_cred.email).first()
    if db_user and bcrypt.checkpw(user_cred.password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        return db_user.user_name, user_cred.password, db_user.email
    return False
   



def get_user(db: Session, user_id: int):
    return db.query(models.User_Reg).filter(models.User_Reg.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User_Reg).filter(models.User_Reg.email == email).first()


def get_user_with_email_and_no(db: Session, email: str, mobile: str):
    return db.query(models.User_Reg).filter(models.User_Reg.email == email, models.User_Reg.mobile_number == mobile).first()


def get_user_by_mobile(db: Session, mobile: str):
    return db.query(models.User_Reg).filter(models.User_Reg.mobile_number == mobile).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User_Reg).offset(skip).limit(limit).all()


def create_user(db: Session, user: BaseModels.user_data):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User_Reg(user_name=user.user_name, 
                              email=user.email, 
                              hashed_password=hashed_password, 
                              mobile_number=user.mobile_number, 
                              address=user.address,
                              land_mark=user.land_mark,
                              pincode=user.pincode)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: BaseModels.user_data):
    db_user = db.query(models.User_Reg).filter(models.User_Reg.email == user.email).first()
    # If user not found, return None or raise an exception
    if not db_user:
        return None
    
    # Update the user's attributes with the new data
    if db_user.user_name != user.user_name:
        db_user.user_name = user.user_name
        print(db_user.user_name)

    # if db_user.email == user.email:
    #     db_user.email = user.email

    if db_user.mobile_number != user.mobile_number:
        db_user.mobile_number = user.mobile_number
        print(db_user.mobile_number)

    if  db_user.address != user.address:
        db_user.address = user.address
        print(db_user.address)

    if db_user.land_mark != user.land_mark:
        db_user.land_mark = user.land_mark
        print(db_user.land_mark )

    if  db_user.pincode != user.pincode:
        db_user.pincode = user.pincode
        print(db_user.pincode)
    
    # Commit the changes to the database
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, email: int):
    db_user = db.query(models.User_Reg).filter(models.User_Reg.email == email).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found"}