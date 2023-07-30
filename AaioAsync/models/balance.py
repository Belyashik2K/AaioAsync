from pydantic import BaseModel

class Balance(BaseModel):

    balance: float
    referal: float
    hold: float
