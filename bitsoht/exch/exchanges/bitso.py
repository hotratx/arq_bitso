import asyncio
from bitsoht.exceptions import TickerNotExist
from bitsoht.exch.base import BaseConnection
from bitsoht.schemas import Ticker


class Bitso(BaseConnection):
    exchange_name = "bitso"
    _external_names = {}

    def __init__(self):
        self.pairs = ['btc/usd', 'eth/brl']
        self._handle_names_to_external()

    def _handle_names_to_external(self):
        for par in self.pairs:
            name_out = self._original_par(par)
            self._external_names.update({par: name_out})

    def _original_par(self, par: str) -> str:
        return par.replace('/', '_')

    def url_create(self, par: str) -> str:
        """Monta a url para cada par"""
        return f"https://api.bitso.com/v3/ticker/?book={self._external_names.get(par)}"

    def handle_ticker(self, data: dict):
        """Handle data if OK, the return Ticker instance
        """
        data = data['payload']
        try:
            ticker = Ticker(
                exchange=self.exchange_name,
                par=data['book'],
                price=data['last'],
                high=data['high'],
                low=data['low'],
                ask=data['ask'],
                bid=data['bid'],
                volume=data['volume']
            )
            return ticker
        except Exception as e:
            print(f'Ocorreu um erro: {e}')


if __name__ == "__main__":
    bt = Bitso()
    loop = asyncio.get_event_loop()
    tasks = []
    tasks.append(asyncio.ensure_future(bt.ticker()))
    response = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
    print(f'RESPONSE: {response}')
