from yatry.utils.models.tree import Tree
from yatry.utils.models import Place, Road
from typing_extensions import override
from typing import Self
from yatry.utils.optim.path import find_path


class Map:
    _roads: list[Road]
    _tree: Tree[Place]

    def __init__(self, root: Place = Place(name="IISER Bhopal")) -> None:
        self._roads = []
        self._tree = Tree[Place](value=root)

    def add_road(self, parent: Tree[Place], child: Tree[Place], fare: float) -> None:
        parent.add_child(child=child)
        self._roads.append(Road(ends={parent.value, child.value}, fare=fare))

    def find_road(self, place1: Place, place2: Place) -> Road:
        return [road for road in self._roads if road.ends == {place1, place2}][0]


if __name__ == "__main__":
    iiserb = Place(name="IISER")
    bhopal = Map(root=iiserb)
    iiserb = bhopal._tree
    green_bay = Tree[Place](value=Place(name="Green Bay"))
    lal_ghati = Tree[Place](value=Place(name="Lalghati"))
    bairagarh = Tree[Place](value=Place(name="Bairagarh"))
    shivhare = Tree[Place](value=Place(name="Shivhare"))

    bhopal.add_road(parent=iiserb, child=green_bay, fare=100)
    bhopal.add_road(parent=green_bay, child=lal_ghati, fare=150)
    bhopal.add_road(parent=iiserb, child=shivhare, fare=100)
    bhopal.add_road(parent=shivhare, child=bairagarh, fare=100)

    iiserb.show()

    my_path = find_path(start=iiserb, end=lal_ghati)
    cost = 0
    for place, next_place in zip(my_path[:-1], my_path[1:]):
        cost += bhopal.find_road(place1=place.value, place2=next_place.value).fare
    print(f"Total fare = {cost}")
