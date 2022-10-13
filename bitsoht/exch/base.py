import asyncio
import aiohttp
from abc import ABC, abstractmethod
from typing import Callable, List, Union
from aiohttp import ClientSession
from bitsoht.exceptions import Fetch_Status_Error, Too_Many_Requests, Timeout
from bitsoht.schemas import Ticker, User


class BaseConnection(ABC):
    """Class generic to extend exchanges class
    If exchange get all, CRIPTOS = 'all'
    """
    exchange_name: str
    pairs: list

    @abstractmethod
    def url_create(self, cripto: str) -> str:
        pass

    @abstractmethod
    def handle_ticker(self, data, par: str) -> List[Ticker] | Ticker:
        pass

    @abstractmethod
    def get_balance(self, user: User):
        pass

    async def ticker(self):
        tasks = []
        session_timeout = aiohttp.ClientTimeout(total=60, connect=8)
        async with ClientSession(timeout=session_timeout) as session:
            # tasks = list(map(self._fetch, self.pairs))
            for par in self.pairs:
                task = self._fetch(
                        session,
                        par,
                        self.handle_ticker,
                        self.url_create(par),
                    )
                tasks.append(task)
            response = asyncio.gather(*tasks, return_exceptions=True)
            return await response

    async def _fetch(
        self,
        session: ClientSession,
        par: str,
        handle: Callable,
        url: str,
    ) -> Union[Ticker, List[Ticker]]:
        timeout = aiohttp.ClientTimeout(total=5)
        try:
            async with session.get(url, timeout=timeout) as response:
                if not response.status == 200:
                    await self._handle_error(response, par)
                data = await response.json()
                return handle(data, par)
        except asyncio.TimeoutError as e:
            raise Timeout(f'timeout par: {par} - {e}')

    async def _handle_error(self, response, par: str):
        if response.status == 429:
            raise Too_Many_Requests(f'error many requests - {self.exchange_name} - {par}')
        raise Fetch_Status_Error(f'error request status: {response.status} - {self.exchange_name} - {par}')
