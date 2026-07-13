from passengers.passenger import PassengersGroup
from utils.constants import GROUND_FLOOR


class Building:
    def __init__(self, total_floors: int) -> None:
        self._total_floors = total_floors
        self._external_calls = {}

    def ground_floor(self) -> int:
        return GROUND_FLOOR

    def top_floor(self) -> int:
        return self._total_floors - 1

    def call_floor(self, group: PassengersGroup) -> None:
        self._external_calls[group.origin_floor()] = group

    def remove_called_floor(self, floor: int) -> None:
        self._external_calls.pop(floor, None)

    def all_calls(self) -> list[int]:
        return list(self._external_calls.values())

    def is_called_at(self, floor: int) -> bool:
        return floor in self._external_calls

    def group_waiting_at(self, floor: int) -> PassengersGroup | None:
        return self._external_calls.get(floor)
