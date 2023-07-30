from pydantic import BaseModel

from typing import Union

class CreateWithdrawal(BaseModel):
    id: str
    my_id: Union[str, int]
    method: str
    wallet: str
    amount: float
    amount_down: float
    commission: float
    commission_type: int
    status: str

class WithdrawalInfo(BaseModel):
    id: str
    my_id: Union[str, int]
    method: str
    wallet: str
    amount: float
    amount_down: float
    commission: float
    commission_type: int
    status: str
    cancel_message: str = None
    date: str
    complete_date: str = None

class WithdrawalMethodInfo(BaseModel):
    min: float
    max: float
    commission_percent: float
    commission_sum: float