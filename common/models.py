from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from common.db import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True)
    status = Column(String, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="orders")

class StatusMapping(Base):
    __tablename__ = "status_mapping"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)     # e.g. "PENDING"
    description = Column(String)                       # e.g. "Order placed, waiting to be processed"
