from pydantic import BaseModel

class Balance(BaseModel):
    balance: float
    referral: float
    hold: float
