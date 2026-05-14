from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    product: str
    status: str
    customer_id: int

    model_config = {"from_attributes": True}


class CustomerResponse(BaseModel):
    id: int
    name: str
    orders: list[OrderResponse] = []

    model_config = {"from_attributes": True}