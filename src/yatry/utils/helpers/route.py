from yatry.utils.models.map import Map
from yatry.utils.models import Passenger
from yatry.utils.data.locations import Location
import numpy as np


def get_passenger_route_fare(
    map: Map, passenger: Passenger
) -> tuple[list[Location], float]:
    return map.get_route_fare(loc_start=passenger.src, loc_end=passenger.dst)


def get_longest_prefix(
    route1: list[Location], route2: list[Location]
) -> list[Location]:
    prefix = []
    inx = 0
    while route1[inx] == route2[inx]:
        prefix.append(route1[inx])
        inx += 1
    return prefix


def get_route_affinity(
    map: Map, route1: list[Location], route2: list[Location]
) -> float:
    prefix = get_longest_prefix(route1=route1, route2=route2)
    fare1 = map.get_fare(route=route1)
    fare_prefix = map.get_fare(route=prefix)
    return fare_prefix / fare1


def get_passenger_route_affinity(
    map: Map, passenger1: Passenger, passenger2: Passenger
) -> float:
    route1 = map._find_route(loc_start=passenger1.src, loc_end=passenger1.dst)
    route2 = map._find_route(loc_start=passenger2.src, loc_end=passenger2.dst)
    return get_route_affinity(map=map, route1=route1, route2=route2)


def get_passenger_route_affinity_matrix(
    map: Map, passengers: list[Passenger]
) -> np.ndarray:
    affs = np.zeros((len(passengers), len(passengers)), dtype=np.float64)
    for i, p1 in enumerate(passengers):
        for j, p2 in enumerate(passengers):
            affs[i, j] = get_passenger_route_affinity(
                map=map, passenger1=p1, passenger2=p2
            )
    return affs
