from yatry.utils.models.map import Map
from yatry.utils.data.locations import Location


BHOPAL = Map(root=Location.IISERB)
BHOPAL.add_road(loc_parent=Location.IISERB, loc_child=Location.GREEN_BAY, fare=100)
BHOPAL.add_road(loc_parent=Location.IISERB, loc_child=Location.SHIVHARE, fare=100)
BHOPAL.add_road(loc_parent=Location.GREEN_BAY, loc_child=Location.AIRPORT, fare=50)
BHOPAL.add_road(loc_parent=Location.AIRPORT, loc_child=Location.DMART, fare=50)
BHOPAL.add_road(loc_parent=Location.DMART, loc_child=Location.LAL_GHATI, fare=50)
BHOPAL.add_road(loc_parent=Location.SHIVHARE, loc_child=Location.CHIRAYU, fare=50)
BHOPAL.add_road(loc_parent=Location.CHIRAYU, loc_child=Location.BAIRAGARH, fare=50)
BHOPAL.add_road(loc_parent=Location.LAL_GHATI, loc_child=Location.UPPER_LAKE, fare=50)
BHOPAL.add_road(loc_parent=Location.UPPER_LAKE, loc_child=Location.MOTI_MASJID, fare=50)
BHOPAL.add_road(loc_parent=Location.MOTI_MASJID, loc_child=Location.RANI_DB, fare=100)
BHOPAL.add_road(loc_parent=Location.RANI_DB, loc_child=Location.AIIMS, fare=50)
BHOPAL.add_road(loc_parent=Location.AIIMS, loc_child=Location.AASHIMA, fare=50)
BHOPAL.add_road(loc_parent=Location.LAL_GHATI, loc_child=Location.BHOPAL_JN, fare=150)
BHOPAL.add_road(loc_parent=Location.BHOPAL_JN, loc_child=Location.PPL_MALL, fare=100)
