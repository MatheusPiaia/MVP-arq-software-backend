import uuid
from app import db
from sqlalchemy import func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore
from datetime import datetime


class ConditionalItem(db.Model):
    __tablename__ = "conditional_items"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    conditional_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("conditionals.id"),
        nullable=False
        )
    product_stock_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("product_stock.id"),
        nullable=False
        )

    quantity = db.Column(db.Integer, default=1)

    final_action = db.Column(
        db.String(20),
        default="pending"
    )  # pending, returned, bought

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow)

    conditional = relationship("Conditional", back_populates="items")
    product_stock = relationship("ProductStock")
