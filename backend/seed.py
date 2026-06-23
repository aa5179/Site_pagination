from faker import Faker
from random import choice, uniform
from datetime import datetime
from database import Session_local
from models import product

fake=Faker()

categories = ['Electronics', 'Clothing', 'Comics', 'Home & Kitchen', 'Sports', 'Marvel Figurines']

db=Session_local()

batch=[]

for i in range(200000):
    product_data= product(
        name=fake.word(),
        category=choice(categories),
        price=round(uniform(100,1000),2),
        created_at=fake.date_time_this_year(),
        updated_at=fake.date_time_this_year()
    )
    batch.append(product_data)

    if len(batch) == 200000:
        db.bulk_save_objects(batch)
        db.commit()
        db.close()
 
print("Done, hogaya yayyy")
