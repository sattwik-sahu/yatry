from dataclasses import dataclass
from yatry.utils.data.locations import Location
from datetime import datetime


@dataclass
class Passenger:
    name: str
    source: Location
    destination: Location
    dep_time_range: tuple[datetime, datetime]

    def get_dep_time_range_num(self) -> tuple[float, float]:
        t_start, t_end = self.dep_time_range
        return t_start.timestamp(), t_end.timestamp()


def main():
    p = Passenger(
        name="Sattwik",
        source=Location.IISERB,
        destination=Location.GREEN_BAY,
        dep_time_range=(datetime.now(), datetime.now()),
    )


if __name__ == "__main__":
    main()
