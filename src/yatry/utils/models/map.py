from yatry.utils.models.tree import Tree
from yatry.utils.models import Passenger, Road
from yatry.utils.optim.route import find_route
from yatry.utils.data.locations import LOC, Location, find_location


class Map:
    _roads: list[Road]
    _tree: Tree[Location]

    def __init__(self, root: Location) -> None:
        self._roads = []
        self._tree = LOC[root]

    @property
    def root(self) -> Tree[Location]:
        return self._tree

    def add_road(self, loc_parent: Location, loc_child: Location, fare: float) -> None:
        LOC[loc_parent].add_child(child=LOC[loc_child])
        self._roads.append(Road(ends={loc_parent, loc_child}, fare=fare))

    def find_road(self, loc1: Location, loc2: Location) -> Road:
        return [road for road in self._roads if road.ends == {loc1, loc2}][0]

    def show(self) -> None:
        self._tree.show()

    def _find_route(self, loc_start: Location, loc_end: Location) -> list[Location]:
        start = LOC[loc_start]
        end = LOC[loc_end]
        route = find_route(start=start, end=end)
        return [find_location(name=place.value.name) for place in route]

    def get_fare(self, route: list[Location]) -> float:
        return sum(
            [
                self.find_road(loc1=loc_1, loc2=loc_2).fare
                for loc_1, loc_2 in zip(route[:-1], route[1:])
            ]
        )

    def get_route_fare(
        self, loc_start: Location, loc_end: Location
    ) -> tuple[list[Location], float]:
        route = self._find_route(loc_start=loc_start, loc_end=loc_end)
        fare = self.get_fare(route=route)
        return route, fare

    def get_passenger_route_fare(
        self, passenger: Passenger
    ) -> tuple[list[Location], float]:
        return self.get_route_fare(loc_start=passenger.src, loc_end=passenger.dst)
