from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

pymysql.install_as_MySQLdb()

SQLALCHEMY_DATABASE_URL = 'mysql://root:@127.0.0.1:3306/store'
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine( SQLALCHEMY_DATABASE_URL )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
