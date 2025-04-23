from yatry.utils.data.locations import Location
from yatry.utils.models.tree import Tree


def find_route(start: Tree[Location], end: Tree[Location]) -> list[Tree[Location]]:
    path = []
    end.make_root()
    node = start
    while node is not end:
        path.append(node)
        node = node.parent  # type: ignore
    path.append(end)
    return path
