from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from database import declarative_base

class product(declarative_base):
    __tablename__ = "products"

    __table_args__=(
        Index(
            "idx_updated_id",
            "updated_at",
            "id"
        ),
        Index(
            "idx_category_updated_id",
            "category",
            "updated_at",
            "id"
        )
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)       
    category = Column(String)
    price = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
