from common import models

def get_schema_info():
    """
    Extract schema info dynamically from SQLAlchemy models.
    Returns dictionary of table -> list of columns.
    """
    return {
        "Customer": [c.name for c in models.Customer.__table__.columns],
        "Order": [c.name for c in models.Order.__table__.columns],
        "StatusMapping": [c.name for c in models.StatusMapping.__table__.columns],
    }
