import uuid
from app import db
from sqlalchemy import func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    api_id = db.Column(db.Integer, nullable=True)  # ID do FakeStoreAPI
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(120))
    image_url = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
        )

    stock_items = relationship(
        "ProductStock",
        back_populates="product",
        lazy="dynamic"
        )
