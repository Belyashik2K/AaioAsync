import ssl
import certifi
import asyncio

from typing import Optional
from aiohttp import ClientSession, TCPConnector

from .exceptions import AaioBadRequest

class RequestsClient:

    def __init__(self) -> None:
        self._loop = asyncio.get_event_loop() 
        self._session: Optional[ClientSession] = None

    def _getsession(self):

        if isinstance(self._session, ClientSession) and not self._session.closed:
            return self._session

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)

        self._session = ClientSession(connector=connector)

        return self._session
    
    async def _request(self,
                method: str,
                url: str, 
                **kwargs) -> dict:
        
        session = self._getsession()

        async with session.request(method, url, **kwargs) as response:
            response = await response.json(content_type="application/json")

        await self._session.close()

        return await self._checkexception(response)

    async def _checkexception(self,
                    response: dict) -> dict:
        if response['type'] == 'error':
            raise AaioBadRequest(response['message'])
        return response
        
        
