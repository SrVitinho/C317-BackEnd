import mysql.connector
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from keys import dbKey

# will need change for production
URL_DATABASE = 'mysql+pymysql://root:' + dbKey + '@localhost:3306/C317'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
