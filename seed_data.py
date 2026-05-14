"""
Seed the database with sample customers, orders, and status codes.
This script is idempotent — running it more than once will not duplicate data.
"""

from faker import Faker
from common import models, db

fake = Faker()

STATUSES = [
    ("PENDING",    "Order placed, waiting to be processed"),
    ("PROCESSING", "Order is being prepared"),
    ("SHIPPED",    "Order has been shipped"),
    ("DELIVERED",  "Order delivered to customer"),
    ("CANCELLED",  "Order cancelled by customer"),
    ("RETURNED",   "Order returned"),
    ("ON_HOLD",    "Order is on hold"),
    ("FAILED",     "Payment failed"),
    ("REFUNDED",   "Refund processed"),
    ("COMPLETED",  "Order successfully completed"),
]


def seed():
    db.Base.metadata.create_all(bind=db.engine)

    with db.SessionLocal() as session:
        # Skip if already seeded
        if session.query(models.StatusMapping).count() > 0:
            print("Database already seeded — skipping.")
            return

        # Status codes
        for code, desc in STATUSES:
            session.add(models.StatusMapping(code=code, description=desc))
        session.commit()

        # ~149 random customers with 1–3 orders each
        status_codes = [s[0] for s in STATUSES]
        for _ in range(149):
            customer = models.Customer(name=fake.name())
            session.add(customer)
            session.flush()
            for _ in range(fake.random_int(min=1, max=3)):
                session.add(models.Order(
                    product=fake.word().capitalize(),
                    status=fake.random_element(status_codes),
                    customer_id=customer.id,
                ))

        # Guaranteed demo customer for testing
        bob = models.Customer(name="Bob Smith")
        session.add(bob)
        session.flush()
        session.add_all([
            models.Order(product="Phone",  status="PENDING", customer_id=bob.id),
            models.Order(product="Laptop", status="SHIPPED", customer_id=bob.id),
        ])

        session.commit()

    print("Database seeded successfully.")


if __name__ == "__main__":
    seed()