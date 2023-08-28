# AaioAsync
> Fully async python wrapper for Aaio.io API
## Installing

    pip install AaioAsync
## Code example
```python
import asyncio

from AaioAsync import AaioAsync

aaio = AaioAsync("API Key", "Shop ID", "Secretkey №1")

async def main():

    balance = await aaio.getbalance()

    print('Доступно >>> ', balance.balance)
    print('В холде >>> ', balance.hold)
    print('Реферальный >>> ', balance.referral)

    info = await aaio.getorderinfo('HelloAaio')

    print('ID >>> ', info.order_id)
    print('Сумма >>> ', info.amount)
    print('Дата >>> ', info.date)
    print('Валюта >>>', info.currency)

asyncio.run(main())
```
## Output
```Python

Доступно >>>  122783.43
В холде >>>  10267.3   
Реферальный >>>  3245.92

ID >>>  HelloAaio
Сумма >>>  7510.0
Дата >>>  2023-07-29 23:21:20
Валюта >>> RUB

```

## Docs
> Go to https://wiki.aaio.io/ for more information about working with acquiring
