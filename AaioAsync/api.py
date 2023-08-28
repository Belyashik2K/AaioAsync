from hashlib import sha256
from urllib.parse import urlencode
from typing import Optional, Union

from .requests import RequestsClient
from .models.balance import Balance
from .models.order import Order, OrderMethodInfo
from .models.withdrawal import CreateWithdrawal, WithdrawalInfo, WithdrawalMethodInfo

class AaioAsync(RequestsClient):
    
    API_HOST = "https://aaio.io"

    def __init__(
            self,
            apikey: str,
            shopid: Optional[str] = None,
            secretkey: Optional[str] = None,
            ) -> None:
        '''
        Initialize Aaio API client
        :param apikey: Your API Key
        :param shopid: Your Shop ID
        :param secretkey: Your Secretkey №1
        '''
        super().__init__()
        self.__apikey = apikey
        self._shop = shopid
        self.__secretkey = secretkey

        self.headers = {
            'Accept': 'application/json',
            'X-Api-Key': self.__apikey
        }

        self.method = 'POST'
    
    async def generatepaymenturl(
        self,
        amount: float,
        order_id: Union[int, str],
        currency: Optional[str] = 'RUB',
        method: Optional[str] = None,
        desc: Optional[str] = None,
        email: Optional[str] = None,
        lang: Optional[str] = None,
        referal: Optional[str] = None,
        us_key: Optional[str] = None
    ) -> str:
        
        """Generate payment url.

        Docs: https://wiki.aaio.io/priem-platezhei/sozdanie-zakaza

        :param amount: Order amount.
        :param order_id: Order number, which unique in your system, up to 16 characters, without spaces (aA-zZ, 0-9, :, -, _, [, ] , |)
        :param currency: Currency. Default to 'RUB' (RUB, UAH, EUR, USD)
        :param method: Payment Aaio system code name
        :param desc: Order description
        :param email: Buyer mail
        :param lang: Interface language. Default to 'ru' (ru, en)
        :param referal: Referral code
        :param us_key: Parameter that you want to get in the notification"""

        if not self.__secretkey or not self._shop:
            raise Exception('Не указан SecretKey или ShopID')

        params = {
            'merchant_id': self._shop,
            'amount': amount,
            'order_id': order_id.strip(),
            'currency': currency,
            'method': method,
            'desc': desc,
            'email': email,
            'lang': lang,
            'referal': referal,
            'us_key': us_key
        }

        for key, value in params.copy().items():
            if value is None:
                del params[key]

        paramsforsing = ':'.join(map(
            str,
            [self._shop, amount, currency, self.__secretkey, order_id])
        )

        sign = sha256(paramsforsing.encode('utf-8')).hexdigest()

        params['sign'] = sign
        
        return f"{self.API_HOST}/merchant/pay?" + urlencode(params)
    
    async def getbalance(self) -> Balance:

        """Get available, referal and hold balance.
        
        Docs: https://wiki.aaio.io/api/poluchenie-balansa"""

        url = f'{self.API_HOST}/api/balance'

        response = await self._request(self.method, url, headers=self.headers)

        return Balance(**response)

    async def getorderinfo(self,
                    order_id: Union[int, str]
                    ) -> Order:
        
        """Get information about an order by OrderID.
        
        Docs: https://wiki.aaio.io/api/informaciya-o-zakaze
        
        :param order_id: OrderID (in your system)"""
        
        if not self._shop:
            raise Exception('Не указан ShopID.')

        url = f'{self.API_HOST}/api/info-pay'
                
        params = {
            'merchant_id': self._shop,
            'order_id': order_id
        }
        
        for key, value in params.copy().items():
            if value is None:
                del params[key]

        response = await self._request(self.method, url, data=params, headers=self.headers)

        return Order(**response)
    
    async def withdrawalmethods(self,
                                method: Optional[str] = None
                                ) -> Union[dict, WithdrawalMethodInfo]:
        
        """Get available methods for withdrawal.
        
        If method is None -> return dict with all methods.
        
        If a specific method -> return info about only this method.
        
        Docs: https://wiki.aaio.io/api/dostupnye-metody-dlya-vyvoda-sredstv
        
        :param method: Specific method. Default is None"""

        url = f'{self.API_HOST}/api/methods-payoff'

        response = await self._request(self.method, url, headers=self.headers)

        if method is not None:
            return WithdrawalMethodInfo(**response['list'][method])
        return response['list']
    
    async def ordermethods(self,
                           method: Optional[str] = None
                           ) -> Union[dict, OrderMethodInfo]:
        
        """Get available methods for order.
        
        If method is None -> return dict with all methods.
        
        If a specific method -> return info about only this method.
        
        Docs: https://wiki.aaio.io/api/dostupnye-metody-dlya-sozdaniya-zakaza
        
        :param method: Specific method. Default is None"""

        url = f'{self.API_HOST}/api/methods-pay'

        params = {
            'merchant_id': self._shop
        }

        response = await self._request(self.method, url, data=params, headers=self.headers)

        if method is not None:
            return OrderMethodInfo.model_validate(response['list'][method])
        return response['list']
    
    async def getwithdrawalinfo(self,
                                my_id: Union[int, str],
                                ) -> WithdrawalInfo:
        
        """Get information about a withdrawal by WithdrawalID.
        
        Docs: https://wiki.aaio.io/api/informaciya-o-zayavke-na-vyvod-sredstv
        
        :param my_id: WithdrawalID (in your system)"""

        url = f'{self.API_HOST}/api/info-payoff'

        params = {
            'my_id': my_id
        }

        response = await self._request(self.method, url, data=params, headers=self.headers)

        return WithdrawalInfo(**response)
    
    async def createwithdrawal(self,
                        my_id: Union[int, str],
                        method: str,
                        amount: float,
                        wallet: str,
                        commission_type: Optional[int] = 0
                        ) -> CreateWithdrawal:
        
        """Create withdrawal.
        
        Docs: https://wiki.aaio.io/api/vyvod-sredstv

        :param my_id: WithdrawalID (in your system)
        :param method: Specific method for withdrawal
        :param amount: Withdrawal amount
        :param wallet: Wallet or number for withdrawal (Without +, " ", and separators)
        :param commission_type: Withdrawal commission type. Default to 0 (from the payment amount)"""

        url = f'{self.API_HOST}/api/create-payoff'

        params = {
            'my_id': my_id,
            'method': method,
            'amount': amount,
            'wallet': wallet,
            'commission_type': commission_type,
        }

        response = await self._request(self.method, url, data=params, headers=self.headers)

        return CreateWithdrawal(**response)