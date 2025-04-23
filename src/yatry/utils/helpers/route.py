from yatry.utils.data.locations import Location


def get_longest_prefix(
    route1: list[Location], route2: list[Location]
) -> list[Location]:
    prefix = []
    for route1_loc, route2_loc in zip(route1, route2):
        if route1_loc is route2_loc:
            prefix.append(route1_loc)
        else:
            break
    return prefix
