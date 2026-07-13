import time

from building.building import Building
from cabin.cabin import Cabin
from enums.direction import Direction
from lift.scheduler import LiftScheduler
from passengers.passenger import Passenger, PassengersGroup
from utils.constants import INITIAL_FLOOR


class Lift:
    def __init__(
        self,
        building: Building,
        cabin: Cabin,
        scheduler: LiftScheduler,
        current_floor: int = INITIAL_FLOOR,
    ) -> None:
        self._building = building
        self._cabin = cabin
        self._scheduler = scheduler
        self._current_floor = current_floor

    def current_floor(self) -> int:
        return self._current_floor

    def ground_floor(self) -> int:
        return self._building.ground_floor()

    def top_floor(self) -> int:
        return self._building.top_floor()

    def target_floor(self) -> int | None:
        return self._scheduler.target_floor()

    def is_idle(self) -> bool:
        return self._scheduler.is_idle()

    def has_reached_target(self) -> bool:
        return self._current_floor == self.target_floor()

    def recalculate_target(self, direction: Direction) -> None:
        self._scheduler.next_stop(
            current_floor=self._current_floor,
            direction=direction
        )

    def preview_direction(self, direction: Direction) -> Direction:
        return self._scheduler.preview_direction(
            current_floor=self._current_floor,
            direction=direction
        )

    def move_one_floor_towards(
        self,
        target_floor: int,
        pause_seconds: int
    ) -> None:
        self._current_floor += self._step_towards(target_floor=target_floor)
        time.sleep(pause_seconds)

    def unboard_passengers(self) -> list[Passenger]:
        return self._cabin.unboard(
            floor=self._current_floor
        )

    def call_is_compatible_with(self, direction: Direction) -> bool:
        waiting_group = self._building.group_waiting_at(
            floor=self._current_floor
        )
        if waiting_group is None:
            return False
        return self.call_direction_here() == direction

    def call_direction_here(self) -> Direction:
        if self._current_floor == self.ground_floor():
            return Direction.UP
        return Direction.DOWN

    def board_waiting_passengers(self) -> list[Passenger]:
        waiting_group = self._building.group_waiting_at(
            floor=self._current_floor
        )
        if waiting_group is None:
            return []
        return self._board_group(waiting_group=waiting_group)

    def _board_group(self, waiting_group: PassengersGroup) -> list[Passenger]:
        boarding_passengers = waiting_group.take_up_to(
            available_spots=self._cabin.available_spots()
        )
        self._cabin.board(passengers=boarding_passengers)
        self._remove_call_if_group_is_empty(group=waiting_group)
        return boarding_passengers

    def _remove_call_if_group_is_empty(self, group: PassengersGroup) -> None:
        if not group.has_passengers_waiting():
            self._building.remove_called_floor(floor=self._current_floor)

    def remaining_passengers_waiting(self) -> int:
        waiting_group = self._building.group_waiting_at(
            floor=self._current_floor
        )
        if waiting_group is None:
            return 0
        return waiting_group.amount()

    def _step_towards(self, target_floor: int) -> int:
        if target_floor > self._current_floor:
            return 1
        if target_floor < self._current_floor:
            return -1
        return 0
