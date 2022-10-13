from bitsoht.exch.handle_exc import Exchanges


class Manager:
    def exchanges(self, exchanges: list[str]):
        self._exch = Exchanges(exchanges)

    def get_tickers(self):
        tickers = self._exch.get_tickers()
        return tickers


if __name__ == '__main__':
    manager = Manager()
    manager.exchanges(['bitso'])
    resp = manager.get_tickers()
    print(f'RESP: {resp}')
