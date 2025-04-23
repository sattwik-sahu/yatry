from typing import Self, Sized
from yatry.utils.models.node import Node


class Tree[TValue](Node[TValue], Sized):
    """
    A tree data structure.
    """

    _parent: Self | None
    _children: list[Self]

    def __init__(self, value: TValue) -> None:
        super().__init__(value=value)
        self._parent = None
        self._children = []

    @property
    def parent(self) -> Self | None:
        return self._parent

    @parent.setter
    def parent(self, parent: Self) -> None:
        self._parent = parent
        if self._parent is not None and self not in self._parent.children:
            self._parent.add_child(child=self)

    @property
    def children(self) -> list[Self]:
        return self._children

    def add_child(self, child: Self) -> None:
        if child not in self._children:
            self._children.append(child)
            if child._parent is not self:
                child._parent = self  # avoid triggering parent setter again

    # @property
    # def parent(self) -> Self | None:
    #     return self._parent

    # @parent.setter
    # def parent(self, parent: Self) -> None:
    #     if self._parent is not parent:
    #         self._parent = parent
    #         if self not in parent._children:
    #             parent._children.append(self)

    def __repr__(self) -> str:
        if not self._children:
            return super().__repr__()
        else:
            return f"[{super().__repr__()} >> ({len(self._children)})]"

    def __len__(self) -> int:
        if self.children:
            return 1 + sum([len(child) for child in self._children])
        else:
            return 1

    def show(self, indent: int = 0) -> None:
        print(f"{'--' * indent} {self._value}")
        for child in self._children:
            child.show(indent=indent + 1)

    def remove_child(self, child: Self) -> None:
        if child in self._children:
            self._children.remove(child)

    def make_root(self, visited: list[Self] = []) -> None:
        # print(f"Making {self.value} as root")
        if self not in visited:
            visited.append(self)
            # print(visited)
        else:
            return
        if self._parent is not None:
            self._parent.remove_child(child=self)
            if self._parent.parent is not None:
                self._parent.make_root(visited=visited)
            self.add_child(child=self._parent)
