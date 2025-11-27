import uuid
from app import db
from sqlalchemy import func  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
        )
    is_active = db.Column(db.Boolean, default=True)

    role = relationship("Role", back_populates="users")
