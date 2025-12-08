from pydantic import BaseModel
from typing import List, Optional

class OrderBase(BaseModel):
    product: str
    status: str

class OrderResponse(OrderBase):
    id: int
    customer_id: int

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str

class CustomerResponse(CustomerBase):
    id: int
    orders: List[OrderResponse] = []

    class Config:
        orm_mode = True
