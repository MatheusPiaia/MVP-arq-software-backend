from app import db
from sqlalchemy.dialects.postgresql import JSONB  # type: ignore
from sqlalchemy import func  # type: ignore


class ApiProductsCache(db.Model):
    __tablename__ = "api_products_cache"

    api_id = db.Column(db.Integer, primary_key=True)
    raw_json = db.Column(JSONB, nullable=False)
    fetched_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
        )
