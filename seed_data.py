from faker import Faker
from common import models, db

fake = Faker()

# Status codes
statuses = [
    ("PENDING", "Order placed, waiting to be processed"),
    ("PROCESSING", "Order is being prepared"),
    ("SHIPPED", "Order has been shipped"),
    ("DELIVERED", "Order delivered to customer"),
    ("CANCELLED", "Order cancelled by customer"),
    ("RETURNED", "Order returned"),
    ("ON_HOLD", "Order is on hold"),
    ("FAILED", "Payment failed"),
    ("REFUNDED", "Refund processed"),
    ("COMPLETED", "Order successfully completed")
]

with db.SessionLocal() as session:
    # 1. Insert StatusMapping
    for code, desc in statuses:
        session.add(models.StatusMapping(code=code, description=desc))
    session.commit()

    # 2. Insert ~149 random customers + orders
    for _ in range(149):
        customer = models.Customer(name=fake.name())
        session.add(customer)
        session.flush()  # so we can use customer.id

        for _ in range(fake.random_int(min=1, max=3)):
            order = models.Order(
                product=fake.word().capitalize(),
                status=fake.random_element([s[0] for s in statuses]),
                customer_id=customer.id
            )
            session.add(order)

    # 3. Add guaranteed demo customer Bob Smith
    bob = models.Customer(name="Bob Smith")
    session.add(bob)
    session.flush()

    session.add_all([
        models.Order(product="Phone", status="PENDING", customer_id=bob.id),
        models.Order(product="Laptop", status="SHIPPED", customer_id=bob.id),
    ])

    session.commit()
    session.close()

print("✅ Database seeded with statuses, customers, orders, and demo Bob Smith.")
