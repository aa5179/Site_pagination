from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from database import Session_local, engine, declarative_base
from models import product

import json
import base64

declarative_base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()


def encode_cursor(updated_at, id, snapshot_time):
    cursor = {
        "updated_at": updated_at.isoformat(),
        "id": id,
        "snapshot_time": snapshot_time.isoformat()
    }

    return base64.b64encode(
        json.dumps(cursor).encode()
    ).decode()


def decode_cursor(cursor):
    decoded = base64.b64decode(
        cursor.encode()
    ).decode()

    return json.loads(decoded)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Product API!"}
@app.get("/products")
def get_products(
    limit: int = Query(
        default=20,
        ge=1,
        le=100
    ),
    cursor: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(product)



    if category:
        query = query.filter(
            product.category == category
        )

    query = query.order_by(
        product.updated_at.desc(),
        product.id.desc()
    )

    if cursor:
        cursor_data = decode_cursor(cursor)

        snapshot_time = datetime.fromisoformat(
            cursor_data["snapshot_time"]
    )

        cursor_updated_at = datetime.fromisoformat(
            cursor_data["updated_at"]
    )

        cursor_id = cursor_data["id"]

    else:
        snapshot_time = datetime.utcnow()

    query = query.filter(
    product.updated_at <= snapshot_time
    )
    products = query.limit(limit).all()

    next_cursor = None

    if products:
        last_product = products[-1]

        next_cursor = encode_cursor(
            last_product.updated_at,
            last_product.id,
            snapshot_time
        )

    return {
        "snapshot_time": snapshot_time.isoformat(),
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "created_at": (
                    p.created_at.isoformat()
                    if p.created_at
                    else None
                ),
                "updated_at": (
                    p.updated_at.isoformat()
                    if p.updated_at
                    else None
                )
            }
            for p in products
        ],
        "next_cursor": next_cursor
    }