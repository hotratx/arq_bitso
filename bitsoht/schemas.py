from dataclasses import dataclass


@dataclass
class Ticker:
    exchange: str
    par: str
    price: str
    high: str
    low: str
    ask: str
    bid: str
    volume: str

    def __repr__(self) -> str:
        return f"{self.exchange}-{self.par}"


@dataclass
class User:
    id: int
    name: str
    bitso_key: str
    bitso_secret: str
