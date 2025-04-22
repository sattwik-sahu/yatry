from typing import FrozenSet
from pprint import pprint


class SymmetricKeyDict[TKey, TValue](dict[tuple[TKey, ...], TValue]):
    """
    A dictionary-like container that maps unordered tuples of keys to values.

    This class behaves like a dictionary where each key is a tuple of hashable elements,
    but the order of elements in the key does not matter. Internally, the key is stored
    as a `frozenset` to enforce this symmetry. As a result, keys like `(1, 2, 3)` and
    `(3, 2, 1)` refer to the same entry in the dictionary.

    ### Note:
        Since `frozenset` is used as the key, duplicate elements are discarded.
        That is, keys like `(1, 2, 2)` and `(1, 2)` will be treated as the same key.

    ### Example:
    >>> d = SymmetricKeyDict[int, str]()
    >>> d[1, 2, 3] = "triangle"
    >>> d[3, 1, 2]
    'triangle'
    >>> d[2, 3] = "edge"
    >>> print(d)
    {(1, 2, 3) -> triangle, (2, 3) -> edge}

    Type:
        TKey: The type of individual key elements (must be hashable).
        TValue: The type of the values associated with each symmetric key.
    """

    _table: dict[FrozenSet[TKey], TValue]

    def __init__(self):
        self._table = dict[FrozenSet[TKey], TValue]()

    def __getitem__(self, key: tuple[TKey, ...]) -> TValue:
        return self._table[frozenset(key)]

    def __setitem__(self, key: tuple[TKey, ...], value: TValue) -> None:
        self._table[frozenset(key)] = value

    def __repr__(self) -> str:
        return (
            f"{{{', '.join([f'{tuple(k)} -> {v}' for k, v in self._table.items()])}}}"
        )


def main():
    # Create symm key dict
    symm_dict: SymmetricKeyDict[int, int] = SymmetricKeyDict[int, int]()
    symm_dict[2, 3] = 2
    symm_dict[3, 1] = 20
    pprint(symm_dict)
    print(symm_dict[3, 2])
    print(symm_dict[1, 3])


if __name__ == "__main__":
    main()
