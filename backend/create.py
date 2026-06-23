from database import engine, declarative_base
from models import product

declarative_base.metadata.create_all(bind=engine)

print("Products table created!")