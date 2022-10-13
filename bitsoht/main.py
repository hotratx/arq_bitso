from bitsoht.exch.handle_exc import Exchanges
from bitsoht.schemas import User


class Manager:
    def exchanges(self, exchanges: list[str]):
        self._exch = Exchanges(exchanges)

    def get_tickers(self):
        tickers = self._exch.get_tickers()
        return tickers

    def get_balance(self, user: User, exchange: str):
        balance = self._exch.get_balance(user, exchange)
        return balance


if __name__ == '__main__':
    user = User(id=1, name="Frank", bitso_key="GKpgLnihNZ", bitso_secret="k0ZZ1TZMMYT0QzGxOYz22wmcEEYdVD2G2TGWhTmy")
    manager = Manager()
    manager.exchanges(['bitso'])
    resp = manager.get_tickers()
    balance = manager.get_balance(user, 'bitso')
    print(f'RESP: {resp}')
