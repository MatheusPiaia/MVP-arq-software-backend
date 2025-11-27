from app import db
from sqlalchemy.orm import relationship  # type: ignore


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    users = relationship("User", back_populates="role")
