from common import models


def get_schema_info() -> dict:
    """Return column names for each model — used to guide the LLM's filter extraction."""
    return {
        "Customer": [c.name for c in models.Customer.__table__.columns],
        "Order": [c.name for c in models.Order.__table__.columns],
        "StatusMapping": [c.name for c in models.StatusMapping.__table__.columns],
    }