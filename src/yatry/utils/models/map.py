from yatry.utils.models.tree import Tree
from yatry.utils.models import Place, Road
from yatry.utils.optim.route import find_route


class Map:
    _roads: list[Road]
    _tree: Tree[Place]

    def __init__(self, root: Tree[Place]) -> None:
        self._roads = []
        self._tree = root

    @property
    def root(self) -> Tree[Place]:
        return self._tree

    def add_road(self, place1: Tree[Place], place2: Tree[Place], fare: float) -> None:
        place1.add_child(child=place2)
        self._roads.append(Road(ends={place1.value, place2.value}, fare=fare))

    def find_road(self, place1: Place, place2: Place) -> Road:
        return [road for road in self._roads if road.ends == {place1, place2}][0]

    def show(self) -> None:
        self._tree.show()

    @staticmethod
    def create_place(place: Place) -> Tree[Place]:
        return Tree[Place](value=place)


if __name__ == "__main__":
    iiserb = Map.create_place(Place(name="IISER"))
    bhopal = Map(root=iiserb)
    # green_bay = Tree[Place](value=Place(name="Green Bay"))
    # lal_ghati = Tree[Place](value=Place(name="Lalghati"))
    # bairagarh = Tree[Place](value=Place(name="Bairagarh"))
    # shivhare = Tree[Place](value=Place(name="Shivhare"))

    green_bay = Map.create_place(place=Place("Green Bay"))
    lal_ghati = Map.create_place(place=Place("Lal Ghati"))
    airport = Map.create_place(place=Place("Airport"))
    dmart = Map.create_place(place=Place("Dmart"))
    bairagarh = Map.create_place(place=Place("Bairagarh"))
    shivhare = Map.create_place(place=Place("Shivhare"))
    chirayu = Map.create_place(place=Place("Chirayu Hospital"))
    upper_lake = Map.create_place(place=Place("Upper Lake"))
    moti_masjid = Map.create_place(place=Place("Moti Masjid"))
    rani_db = Map.create_place(place=Place("Rani Kamlapati / DB Mall"))
    aiims= Map.create_place(place=Place("AIIMS Bhopal"))
    aashima = Map.create_place(place=Place("Aashima Mall"))
    bhopal_jn = Map.create_place(place=Place("Bhopal Junction"))
    ppl_mall = Map.create_place(place=Place("People's Mall"))
    #kohefiza = Map.create_place(place=Place("Kohefiza")) #Lal Ghati and Kohefiza are merged (distance<1km)

    bhopal.add_road(place1=iiserb, place2=green_bay, fare=100)
    bhopal.add_road(place1=iiserb, place2=shivhare, fare=100)
    bhopal.add_road(place1=green_bay, place2=airport, fare=50)
    bhopal.add_road(place1=airport, place2=dmart, fare=50)
    bhopal.add_road(place1=dmart, place2=lal_ghati, fare=50)
    bhopal.add_road(place1=shivhare, place2=chirayu, fare=50)
    bhopal.add_road(place1=chirayu, place2=bairagarh, fare=50)
    bhopal.add_road(place1=lal_ghati, place2=upper_lake, fare=50)
    bhopal.add_road(place1=upper_lake, place2=moti_masjid, fare=50)
    bhopal.add_road(place1=moti_masjid, place2=rani_db, fare=100)
    bhopal.add_road(place1=rani_db, place2=aiims, fare=50)
    bhopal.add_road(place1=aiims, place2=aashima, fare=50)
    bhopal.add_road(place1=lal_ghati, place2=bhopal_jn, fare=150)
    bhopal.add_road(place1=bhopal_jn, place2=ppl_mall, fare=100)

    iiserb.show()

    my_route = find_route(start=iiserb, end=chirayu)
    print([place.value.name for place in my_route])
    cost = 0
    for place, next_place in zip(my_route[:-1], my_route[1:]):
        fare = bhopal.find_road(place1=place.value, place2=next_place.value).fare
        print(place.value.name, next_place.value.name, fare)
        cost += fare
    print(f"Total fare = {cost}")
