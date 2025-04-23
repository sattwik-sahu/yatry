from yatry.utils.models.map import Map
from yatry.utils.data.locations import Location


# Initialize map of Bhopal with root location as IISER
BHOPAL = Map(root=Location.IISERB)

# Register all locations in the map
for location in Location:
    BHOPAL.register_location(location=location)

# Add the roads between locations and their fares by rickshaw
BHOPAL.add_road(loc_from=Location.IISERB, loc_to=Location.GREEN_BAY, fare=100)
BHOPAL.add_road(loc_from=Location.IISERB, loc_to=Location.SHIVHARE, fare=100)
BHOPAL.add_road(loc_from=Location.GREEN_BAY, loc_to=Location.AIRPORT, fare=50)
BHOPAL.add_road(loc_from=Location.AIRPORT, loc_to=Location.DMART, fare=50)
BHOPAL.add_road(loc_from=Location.DMART, loc_to=Location.LAL_GHATI, fare=50)
BHOPAL.add_road(loc_from=Location.SHIVHARE, loc_to=Location.CHIRAYU, fare=50)
BHOPAL.add_road(loc_from=Location.CHIRAYU, loc_to=Location.BAIRAGARH, fare=50)
BHOPAL.add_road(loc_from=Location.LAL_GHATI, loc_to=Location.UPPER_LAKE, fare=50)
BHOPAL.add_road(loc_from=Location.UPPER_LAKE, loc_to=Location.MOTI_MASJID, fare=50)
BHOPAL.add_road(loc_from=Location.MOTI_MASJID, loc_to=Location.RANI_DB, fare=100)
BHOPAL.add_road(loc_from=Location.RANI_DB, loc_to=Location.AIIMS, fare=50)
BHOPAL.add_road(loc_from=Location.AIIMS, loc_to=Location.AASHIMA, fare=50)
BHOPAL.add_road(loc_from=Location.LAL_GHATI, loc_to=Location.BHOPAL_JN, fare=150)
BHOPAL.add_road(loc_from=Location.BHOPAL_JN, loc_to=Location.PPL_MALL, fare=100)
