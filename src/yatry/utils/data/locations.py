from enum import Enum
from yatry.utils.models.tree import Tree


class Location(Enum):
    IISERB = "IISER Bhopal"
    GREEN_BAY = "Green Bay"
    LAL_GHATI = "Lal Ghati"
    AIRPORT = "Airport"
    DMART = "DMart"
    BAIRAGARH = "Bairagarh"
    SHIVHARE = "Shivhare"
    CHIRAYU = "Chirayu Hospital"
    UPPER_LAKE = "Upper Lake"
    MOTI_MASJID = "Moti Masjid"
    RANI_DB = "Rani Kamlapati / DB Mall"
    AIIMS = "AIIMS Bhopal"
    AASHIMA = "Aashima Mall"
    BHOPAL_JN = "Bhopal Junction"
    PPL_MALL = "People's Mall"


LOC: dict[Location, Tree[Location]] = {
    loc: Tree[Location](value=loc) for loc in Location
}


def find_location(name: str) -> Location:
    return [loc for loc in Location if loc.name == name][0]
