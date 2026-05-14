from sqlalchemy.orm import Session
from common import models


def query_orders(filters: dict, db: Session) -> list:
    """Query orders from the database using optional filters."""
    query = db.query(models.Order).join(models.Customer)

    if customer := filters.get("customer"):
        query = query.filter(models.Customer.name.ilike(f"%{customer}%"))

    if product := filters.get("product"):
        query = query.filter(models.Order.product.ilike(f"%{product}%"))

    if status := filters.get("status"):
        query = query.filter(models.Order.status.ilike(f"%{status}%"))

    return query.all()