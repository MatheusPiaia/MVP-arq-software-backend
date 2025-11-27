import uuid
from app import db
from sqlalchemy import func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore


class Conditional(db.Model):
    __tablename__ = "conditionals"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    customer_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("customers.id"),
        nullable=False
        )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id"),
        nullable=False
        )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="open"
    )  # open, returned, completed

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
        )
    closed_at = db.Column(db.DateTime, nullable=True)

    customer = relationship("Customer")
    user = relationship("User")
    items = relationship("ConditionalItem", back_populates="conditional")
