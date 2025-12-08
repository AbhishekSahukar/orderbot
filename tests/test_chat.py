import sys, os
import pytest
from fastapi.testclient import TestClient

# Ensure root project is on PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api.main import app
from common import db, models

client = TestClient(app)


@pytest.fixture(scope="module")
def session():
    """Provide a database session for tests."""
    with db.SessionLocal() as session:
        yield session


def test_root():
    """Check if root endpoint is alive."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Order Status Chatbot API is running 🚀"


def test_chat_query_bob():
    """Integration test for Bob's orders through chatbot."""
    response = client.post("/api/chat/query", json={"query": "What is the status of Bob's orders?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert "Bob" in data["answer"] or "order" in data["answer"]


def test_bob_orders_in_db(session):
    """Direct DB test: Bob should have at least 2 orders (Phone + Laptop)."""
    bob = session.query(models.Customer).filter(models.Customer.name == "Bob Smith").first()
    assert bob is not None, "Bob Smith should exist in DB"

    orders = session.query(models.Order).filter(models.Order.customer_id == bob.id).all()
    assert len(orders) >= 2, "Bob should have at least 2 orders"
    product_names = [o.product for o in orders]
    assert "Phone" in product_names
    assert "Laptop" in product_names
