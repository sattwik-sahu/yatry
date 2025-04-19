from yatry.utils.models.tree import Tree
from yatry.utils.models import Place


def find_route(start: Tree[Place], end: Tree[Place]) -> list[Tree[Place]]:
    path = []
    end.make_root()
    # end.show()
    node = start
    while node is not end:
        path.append(node)
        node = node.parent  # type: ignore
    path.append(end)
    return path
