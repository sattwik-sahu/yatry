from typing import Self
from abc import ABC, abstractmethod


class Node[TValue](ABC):
    _value: TValue

    def __init__(self, value: TValue) -> None:
        self._value = value

    @property
    def value(self) -> TValue:
        return self._value

    @value.setter
    def value(self, value: TValue) -> TValue:
        self._value = value
        return self._value


class Tree[TValue](Node[TValue]):
    pass

