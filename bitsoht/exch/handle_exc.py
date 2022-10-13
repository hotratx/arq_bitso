import asyncio
from typing import List
from itertools import chain
from bitsoht.exch.base import BaseConnection
from bitsoht.schemas import Ticker


class Exchanges:
    _handlers: dict[str, BaseConnection] = {}
    _tasks_tickers: List = []

    def __init__(self, exch_init: List):
        self.exch_init = exch_init
        self.sub()

    def _publish(self, exchange):
        try:
            retval = self._handlers[exchange]
        except KeyError as e:
            raise NotImplementedError(f"{e}")
        return retval

    def sub(self):
        for exch_cls in BaseConnection.__subclasses__():
            if exch_cls.exchange_name in self.exch_init:
                fn = exch_cls()
                self._handlers[fn.exchange_name] = fn
                self._tasks_tickers.append(asyncio.ensure_future(fn.ticker()))

    def get_tickers(self) -> List[Ticker]:
        """Faz a chamada para execução das corotinas armazenadas em self._tasks_tickers
        :return lista de Tickers de todas exchanges
        """
        return self._run_fetch(self._tasks_tickers)

    def _run_fetch(self, tasks: List[asyncio.Future]) -> List:
        """Executa as corotinas das instâncias (fn)"""
        loop = asyncio.get_event_loop()
        resp = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        resp = list(chain.from_iterable(resp))
        datas = []
        erros = []
        # separa os erros da busca pelos dados nas apis
        for data in resp:
            if isinstance(data, list):
                for x in data:
                    if isinstance(x, Exception):
                        erros.append(x)
                    else:
                        datas.append(x)
            else:
                if isinstance(data, Exception):
                    erros.append(data)
                else:
                    datas.append(data)
        if erros:
            pass
        return datas
