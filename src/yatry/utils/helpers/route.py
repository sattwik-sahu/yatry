from yatry.utils.models.map import Map
from yatry.utils.models import Place


def main():
    iiserb = Map.create_place(Place(name="IISER"))
    bhopal = Map(root=iiserb)
    # green_bay = Tree[Place](value=Place(name="Green Bay"))
    # lal_ghati = Tree[Place](value=Place(name="Lalghati"))
    # bairagarh = Tree[Place](value=Place(name="Bairagarh"))
    # shivhare = Tree[Place](value=Place(name="Shivhare"))

    green_bay = Map.create_place(place=Place("Green Bay"))
    lal_ghati = Map.create_place(place=Place("Lal Ghati"))
    airport = Map.create_place(place=Place("Airport"))
    bairagarh = Map.create_place(place=Place("Bairagarh"))
    shivhare = Map.create_place(place=Place("Shivhare"))
    chirayu = Map.create_place(place=Place("Chirayu Hospital"))
    upper_lake = Map.create_place(place=Place("Upper Lake"))
    kohefiza = Map.create_place(place=Place("Kohefiza"))

    bhopal.add_road(place1=iiserb, place2=green_bay, fare=100)
    bhopal.add_road(place1=green_bay, place2=airport, fare=30)
    bhopal.add_road(place1=airport, place2=lal_ghati, fare=120)
    bhopal.add_road(place1=iiserb, place2=shivhare, fare=100)
    bhopal.add_road(place1=shivhare, place2=chirayu, fare=50)
    bhopal.add_road(place1=chirayu, place2=bairagarh, fare=70)
    bhopal.add_road(place1=lal_ghati, place2=kohefiza, fare=80)
    bhopal.add_road(place1=lal_ghati, place2=upper_lake, fare=50)

    iiserb.show()


if __name__ == "__main__":
    main()
