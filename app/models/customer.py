import uuid
from app import db
from sqlalchemy import func  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40))
    address = db.Column(db.String(255))
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
        )
