from sqlalchemy.orm import Session
from common import models

def query_orders(filters: dict, db: Session):
    query = db.query(models.Order).join(models.Customer)

    if "customer" in filters:
        # ✅ Case-insensitive, partial matching (dynamic)
        query = query.filter(models.Customer.name.ilike(f"%{filters['customer']}%"))

    if "product" in filters:
        query = query.filter(models.Order.product.ilike(f"%{filters['product']}%"))

    if "status" in filters:
        query = query.filter(models.Order.status.ilike(f"%{filters['status']}%"))

    return query.all()
