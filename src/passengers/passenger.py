import random

from utils.constants import GROUND_FLOOR, MAX_GROUP_SIZE


class Passenger:
    def __init__(self, destination_floor: int) -> None:
        self._destination_floor = destination_floor

    def wants_to_get_off_at(self, floor: int) -> bool:
        return self._destination_floor == floor

    def destination_floor(self) -> int:
        return self._destination_floor


class PassengersGroup:
    def __init__(
        self,
        origin_floor: int,
        passengers: list[Passenger]
    ) -> None:
        self._origin_floor = origin_floor
        self._passengers = list(passengers)

    def origin_floor(self) -> int:
        return self._origin_floor

    def amount(self) -> int:
        return len(self._passengers)

    def has_passengers_waiting(self) -> bool:
        return self.amount() > 0

    def take_up_to(self, available_spots: int) -> list[Passenger]:
        boarding_passengers = self._passengers[:available_spots]
        self._passengers = self._passengers[available_spots:]
        return boarding_passengers


class PassengersGroupFactory:
    def __init__(
        self,
        random_generator: random.Random,
        max_group_size: int = MAX_GROUP_SIZE,
    ) -> None:
        self._random_generator = random_generator
        self._max_group_size = max_group_size

    def create_group(
        self,
        origin_floor: int,
        top_floor: int
    ) -> PassengersGroup:
        group_size = self._random_generator.randint(1, self._max_group_size)
        passengers = [
            self._create_passenger(
                origin_floor=origin_floor,
                top_floor=top_floor
            )
            for _passenger in range(group_size)
        ]
        return PassengersGroup(
            origin_floor=origin_floor,
            passengers=passengers
        )

    def _create_passenger(
        self,
        origin_floor: int,
        top_floor: int
    ) -> Passenger:
        destination_floor = self._pick_destination_floor(
            origin_floor=origin_floor,
            top_floor=top_floor
        )
        return Passenger(destination_floor)

    def _pick_destination_floor(
        self,
        origin_floor: int,
        top_floor: int
    ) -> int:
        if origin_floor == GROUND_FLOOR:
            return self._pick_floor_above_ground(top_floor=top_floor)
        return self._pick_floor_for_descending_passenger(
            origin_floor=origin_floor
        )

    def _pick_floor_above_ground(self, top_floor: int) -> int:
        return self._random_generator.randint(1, top_floor)

    def _pick_floor_for_descending_passenger(
        self,
        origin_floor: int,
    ) -> int:
        is_first_floor = origin_floor == 1
        destination_is_not_ground = self._random_generator.random() <= 0.5
        wants_ground_floor = is_first_floor or destination_is_not_ground
        if wants_ground_floor:
            return GROUND_FLOOR
        return self._random_generator.randint(1, origin_floor - 1)
