from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, TIMESTAMP
from sqlalchemy.orm import relationship

from connect import Base


class User_Reg(Base):
    __tablename__ = "user_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    mobile_number = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    address = Column(String, nullable=False)
    land_mark = Column(String)
    pincode = Column(Integer, nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)