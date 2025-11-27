import uuid
from app import db
from sqlalchemy import func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore
from datetime import datetime


class ProductStock(db.Model):
    __tablename__ = "product_stock"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("products.id"),
        nullable=False
        )

    size = db.Column(db.String(10), nullable=False)
    color = db.Column(db.String(30), nullable=False)

    quantity_available = db.Column(db.Integer, nullable=False, default=0)
    quantity_reserved = db.Column(db.Integer, nullable=False, default=0)

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )

    product = relationship("Product", back_populates="stock_items")
