from yatry.utils.data.locations import Location


def get_longest_prefix(
    route1: list[Location], route2: list[Location]
) -> list[Location]:
    prefix = []
    inx = 0
    while route1[inx] == route2[inx]:
        prefix.append(route1[inx])
        inx += 1
    return prefix
