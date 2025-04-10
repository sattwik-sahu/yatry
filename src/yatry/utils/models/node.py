from typing import TypeVar
from uuid import UUID, uuid4


TValue = TypeVar("TValue")


class Node[TValue]:
    """
    A node in a particular data structure.
    """

    _id: UUID
    _value: TValue

    def __init__(self, value: TValue) -> None:
        self._id = uuid4()
        self._value = value

    def __repr__(self) -> str:
        return f"{{{self._value}}}"

    @property
    def value(self) -> TValue:
        return self._value

    @value.setter
    def value(self, value: TValue) -> None:
        self._value = value


def main():
    node = Node[int](value=10)
    print(node)


if __name__ == "__main__":
    main()
