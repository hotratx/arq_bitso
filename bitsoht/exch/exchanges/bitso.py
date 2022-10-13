import asyncio
from bitsoht.exceptions import TickerNotExist
from bitsoht.exch.base import BaseConnection
from bitsoht.schemas import Ticker, User
import requests
import hmac
import hashlib
import json
import time


class Bitso(BaseConnection):
    exchange_name = "bitso"
    _external_names = {}

    def __init__(self):
        self.pairs = ['btc/usd', 'eth/brl']
        self._handle_names_to_external()

    def _request(self, user: User, method, request_path, payload={}) -> requests.Response:
        auth_header = self._signature(user, method, request_path, payload)
        print(f'AUTH_HEADER: {auth_header}')

        match method:
            case "GET":
                print('VAI GET')
                response = requests.get("https://api.bitso.com" + request_path, headers={"Authorization": auth_header})
            case "POST":
                response = requests.post("https://api.bitso.com" + request_path, json=payload, headers={"Authorization": auth_header})
            case _:
                raise Exception(f'Method: {method} not allowed')
        return response

    def _signature(self, user: User, method, request_path, payload={}):
        methods = ["POST", "GET", "PUT", "DELETE"]

        if method not in methods:
            raise Exception(f"method {method} not allowed")

        nonce = str(int(round(time.time() * 1000)))

        message = nonce + method + request_path
        if (method == "POST"):
            message += json.dumps(payload)

        signature = hmac.new(user.bitso_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        auth_header = f'Bitso {user.bitso_key}:{nonce}:{signature}'
        return auth_header

    def _handle_names_to_external(self):
        for par in self.pairs:
            name_out = self._par_original(par)
            self._external_names.update({par: name_out})

    def _par_original(self, par: str) -> str:
        return par.replace('/', '_')

    def url_create(self, par: str) -> str:
        """Monta a url para cada par"""
        return f"https://api.bitso.com/v3/ticker/?book={self._external_names.get(par)}"

    def handle_ticker(self, data: dict, par: str):
        data = data['payload']
        try:
            ticker = Ticker(
                exchange=self.exchange_name,
                par=par,
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

    def get_balance(self, user: User):
        print(f'CHEGOU O USER: {user}')
        method = "GET"
        request_path = "/v3/balance/"

        response = self._request(user, method, request_path)

        if response.status_code != 200:
            raise Exception(f"Get balance id not completed: {response.json()}")
        return response.json()


if __name__ == "__main__":
    bt = Bitso()
    loop = asyncio.get_event_loop()
    tasks = []
    tasks.append(asyncio.ensure_future(bt.ticker()))
    response = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
    print(f'RESPONSE: {response}')
