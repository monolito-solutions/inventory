from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USERNAME = "inventory_user"
DB_PASSWORD = "inventory_pwd"
DB_HOSTNAME = "localhost"
DB_NAME = "inventory"

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    return db

def get_base_metadata():
    return Base.metadata

def initialize_base():
    from modules.inventory.infrastructure.dtos import InventoryDTO
    return Base