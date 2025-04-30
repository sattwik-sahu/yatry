from yatry.utils.models.tree import Tree
from yatry.utils.models import Passenger
from yatry.utils.data.locations import Location
from yatry.utils.helpers.route import get_valid_shared_route
from yatry.utils.models.symm_dict import SymmetricKeyDict
import numpy as np
from numpy import typing as npt


type RoadRegistry = SymmetricKeyDict[Location, float]
type MapNode = Tree[Location]


class Map:
    """
    Implements a map with locations and roads.

    The map here is implemented as a tree instead of a graph to avoid multiple
    paths between locations to reduce complexity of optimization.

    Attributes:
        _roads (RoadRegistry): A symmetric dictionary with locations as keys
            and the fare as the value.
        _root (Tree[Location]): The root location of the map. This should be the
            primary point of focus in the region.
        _locations (dict[Location, MapNode]): A mapping between the `Location` enum
             and the corresponding nodes in the map.
    """

    _roads: RoadRegistry
    _root: Tree[Location]
    _locations: dict[Location, MapNode]

    def __init__(self, root: Location) -> None:
        """
        Initializes a Map object with `root` as the root location.

        Args:
            root (Location): The `Location` enum item of the primary
                point of focus of the map.
        """
        self._roads = SymmetricKeyDict[Location, float]()
        self._locations = dict[Location, MapNode]()
        self.register_location(location=root)
        self._root = self._locations[root]

    def register_location(self, location: Location) -> None:
        """
        Registers a location in the map.

        NOTE:
        Avoids duplicate entries by checking whether the location is
        already registed in the map.

        Args:
            location (Location): The `Location` enum item corresponding
                to the location to be registered.
        """
        if location not in self._locations:
            node: MapNode = Tree[Location](value=location)
            self._locations[location] = node

    @property
    def root(self) -> Tree[Location]:
        return self._root

    def add_road(self, loc_from: Location, loc_to: Location, fare: float) -> None:
        """
        Adds a road between two locations in the map.

        Parameters have `_from` and `_to` suffixes to indicate that the map
        is implemented as a *tree*. `loc_from` and `loc_to` must be such that
        the path `(root, loc_from, loc_to)` is present in the map's tree as
        decided by the user beforehand.

        Args:
            loc_from (Location): The location from which the road starts.
            loc_to (Location): The location to which the road goes.
        """
        self._locations[loc_from].add_child(child=self._locations[loc_to])
        self._roads[loc_from, loc_to] = fare

    def get_road_fare(self, loc_1: Location, loc_2: Location) -> float:
        """
        Gets the fare to go from `loc_1` to `loc_2` on the map. The ordering
        of the locations does not matter like `add_road`, as `self._roads`
        is implemented as a symmetric key dictionary.

        Args:
            loc_1 (Location): The `Location` at one end of the road.
            loc_2 (Location): The `Location` at the other end (LOL).
        """
        return self._roads[loc_1, loc_2]

    def show(self) -> None:
        self._root.show()

    def _find_route(self, loc_start: Location, loc_end: Location) -> list[Location]:
        """
        Finds a route between the two given locations in the map.

        Args:
            loc_start (Location): The source `Location` of the route.
            loc_end (Location): The destination `Location` of the route.

        Returns:
            list[Location]: The `list` of `Location`s indicating the different
                locations through which the route goes.
        """
        start = self._locations[loc_start]
        end = self._locations[loc_end]
        route: list[MapNode] = []
        end.make_root()
        node = start
        while node is not end:
            route.append(node)  # type: ignore
            node = node.parent  # type: ignore
        route.append(end)

        self._root.make_root()

        return [place.value for place in route]

    def get_fare_on_route(self, route: list[Location]) -> float:
        """
        Gets the fare born by travelling on a given `route`.

        Args:
            route (list[Location]): The route to calculate the travel
                fare on.

        Returns:
            float: The fare to travel on the given route.
        """
        return sum(
            [self._roads[loc_1, loc_2] for loc_1, loc_2 in zip(route[:-1], route[1:])]
        )

    def make_trip(
        self, loc_start: Location, loc_end: Location
    ) -> tuple[list[Location], float]:
        """
        Plans a trip from `loc_start` to `loc_end` and returns the route
        on the map tree and the fare born on that route.

        Args:
            loc_start (Location): The starting `Location` of the trip.
            loc_end (Location): The ending `Location` of the trip.

        Returns:
            tuple[list[Location], float]: Tuple of -
                - The route to be followed on the map.
                - The fare on that route.
        """
        route = self._find_route(loc_start=loc_start, loc_end=loc_end)
        fare = self.get_fare_on_route(route=route)
        return route, fare

    def get_passenger_route_fare(
        self, passenger: Passenger
    ) -> tuple[list[Location], float]:
        """
        Plans a trip for a given `Passenger`, and returns the route to travel
        on the map and the fare.

        Args:
            passenger (Passenger): The passenger to plan the trip for.

        Returns:
            tuple[list[Location], float]: Tuple of -
                - The route to be followed on the map.
                - The fare on that route.
        """
        return self.make_trip(loc_start=passenger.source, loc_end=passenger.destination)

    def _get_route_affinity(
        self, route1: list[Location], route2: list[Location]
    ) -> float:
        """
        Computes the route affinity between two passengers based on their individual routes.

        The affinity is calculated as the ratio of fare on the common prefix of both routes
        to the total fare of the first passenger's route.

        Args:
            passenger1 (Passenger): The first passenger.
            passenger2 (Passenger): The second passenger.

        Returns:
            float: A value between 0 and 1 indicating how much of passenger1's route
                overlaps with passenger2's route in terms of fare.
        """
        prefix = get_valid_shared_route(route1=route1, route2=route2)
        fare1 = self.get_fare_on_route(route=route1)
        fare_prefix = self.get_fare_on_route(route=prefix)
        return fare_prefix / fare1

    def get_passenger_route_affinity(
        self, passenger1: Passenger, passenger2: Passenger
    ) -> float:
        """
        Computes a matrix of route affinities for a list of passengers.

        Each entry (i, j) in the matrix represents the route affinity between
        passenger i and passenger j, as calculated using the fare-overlap metric.

        Args:
            passengers (list[Passenger]): A list of `Passenger` objects.

        Returns:
            np.ndarray: A 2D array of shape (N, N), where N is the number of passengers,
                containing the pairwise route affinities.
        """
        route1 = self._find_route(
            loc_start=passenger1.source, loc_end=passenger1.destination
        )
        route2 = self._find_route(
            loc_start=passenger2.source, loc_end=passenger2.destination
        )
        return self._get_route_affinity(route1=route1, route2=route2)

    def get_passenger_route_affinity_matrix(
        self, passengers: list[Passenger]
    ) -> npt.NDArray[np.float64]:
        """
        Computes the route affinity between two routes.

        The route affinity is defined as the fare of the longest shared prefix
        between the two routes divided by the fare of the first route.

        Args:
            route1 (list[Location]): The first route.
            route2 (list[Location]): The second route.

        Returns:
            float: A value in [0, 1] representing how much of `route1` is common
                with `route2` in terms of fare.
        """
        affs = np.zeros((len(passengers), len(passengers)), dtype=np.float64)
        for i, p_i in enumerate(passengers):
            for j, p_j in enumerate(passengers):
                affs[i, j] = self.get_passenger_route_affinity(
                    passenger1=p_i, passenger2=p_j
                )
        return affs
