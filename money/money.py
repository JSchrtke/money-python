from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict


class Expression(ABC):
    @abstractmethod
    def reduce(self, bank: Bank, target_currency: str) -> Money:
        pass

    @abstractmethod
    def __add__(self, addend: Expression) -> Expression:
        pass

    @abstractmethod
    def __mul__(self, multiplier: int) -> Expression:
        pass


class Money(Expression):
    def __init__(self, amount: int, currency: str) -> None:
        self._amount = amount
        self.currency = currency

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self._amount == other._amount and self.currency == other.currency

    def __mul__(self, multiplier: int) -> Expression:
        return Money(self._amount * multiplier, self.currency)

    def __add__(self, addend: Expression) -> Expression:
        return Sum(self, addend)

    def reduce(self, bank: Bank, target_currrency: str) -> Money:
        rate = bank.rate(self.currency, target_currrency)
        return Money(self._amount // rate, target_currrency)

    @staticmethod
    def dollar(amount: int) -> Money:
        return Money(amount, "USD")

    @staticmethod
    def franc(amount: int) -> Money:
        return Money(amount, "CHF")


class Sum(Expression):
    def __init__(self, augend: Expression, addend: Expression):
        self.augend = augend
        self.addend = addend

    def reduce(self, bank: Bank, target_currency: str) -> Money:
        reduced_augend = self.augend.reduce(bank, target_currency)
        reduced_addend = self.addend.reduce(bank, target_currency)
        amount = reduced_augend._amount + reduced_addend._amount
        return Money(amount, target_currency)

    def __add__(self, addend: Expression) -> Expression:
        return Sum(self, addend)

    def __mul__(self, multiplier: int) -> Expression:
        return Sum(self.augend * multiplier, self.addend * multiplier)


class Bank:
    def __init__(self):
        self.__rates: Dict = {}

    def add_rate(self, from_currency: str, to_currency: str, rate: int) -> None:
        new_rate = {(from_currency, to_currency): rate}
        self.__rates.update(new_rate)

    def reduce(self, source: Expression, target_currency: str) -> Money:
        return source.reduce(self, target_currency)

    def rate(self, from_currency: str, to_currency: str) -> int:
        if from_currency == to_currency:
            return 1
        return self.__rates[(from_currency, to_currency)]
