from sqlalchemy.orm import sessionmaker, declarative_base;
from sqlalchemy import create_engine;
import os;
from dotenv import load_dotenv;

load_dotenv();
Database_URL = os.getenv("DATABASE_URL")
engine = create_engine(Database_URL)
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()


