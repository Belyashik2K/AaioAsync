from pydantic import BaseModel

from typing import Union

class Order(BaseModel):
    id: str
    order_id: Union[str, int]
    merchant_id: str
    merchant_domain: str
    method: str = None
    amount: float
    currency: str
    profit: float = None
    commission: float = None
    commission_client: float = None
    commission_type: str
    email: str = None
    status: str
    date: str
    expired_date: str
    complete_date: str = None
    us_vars: list

class OrderMethodCurrencies(BaseModel):
    RUB: float
    UAH: float
    USD: float
    EUR: float

class OrderMethodInfo(BaseModel):
    min: OrderMethodCurrencies
    max: OrderMethodCurrencies
    commission_percent: float


