from setuptools import setup

version = '0.1.10'

setup(name='AaioAsync',
      version=version,

      author='Belyashik2K',
      author_email='lovelybelyashik@gmail.com',

      license='Apache License, Version 2.0',

      long_description="""# AaioAsync
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
""",
      long_description_content_type='text/markdown',

      description='Fully async python wrapper for Aaio.io API',
      url='https://github.com/Belyashik2K/AaioAsync',
      packages=['AaioAsync', 'AaioAsync/exceptions', 'AaioAsync/models'],
      install_requires=['certifi', 'aiohttp', 'pydantic'],
      zip_safe=False)
