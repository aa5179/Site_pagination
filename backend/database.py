from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine= create_engine(DATABASE_URL)

Session_local=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine 
)

declarative_base = declarative_base()

