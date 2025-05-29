from pydantic import BaseModel


class itemPayment(BaseModel):
    id: int
    title: str
    quantity: int
    currency: str
    unit_price: float
