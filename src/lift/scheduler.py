from logging import debug

from building.building import Building
from cabin.cabin import Cabin
from enums.direction import Direction


class LiftScheduler:
    def __init__(self, building: Building, cabin: Cabin) -> None:
        self._building = building
        self._cabin = cabin
        self._target_floor: int | None = None

    def target_floor(self) -> int | None:
        return self._target_floor

    def is_idle(self) -> bool:
        return self._target_floor is None

    def next_stop(self, current_floor: int, direction: Direction) -> None:
        pending_stops = self._pending_stops()
        self._target_floor = self._choose_target(
            pending_stops=pending_stops,
            current_floor=current_floor,
            direction=direction
        )
        debug(f"[next_stop] CALLED FLOORS: {pending_stops}")
        debug(f"[next_stop] TARGET: {self._target_floor}")

    def preview_direction(
        self,
        current_floor: int,
        direction: Direction
    ) -> Direction:
        pending_stops = self._pending_stops()
        target = self._choose_target(
            pending_stops=pending_stops,
            current_floor=current_floor,
            direction=direction
        )
        return self._direction_towards(
            current_floor=current_floor,
            target_floor=target
        )

    def _direction_towards(
        self,
        current_floor: int,
        target_floor: int | None
    ) -> Direction:
        if target_floor is None:
            return Direction.IDLE
        if target_floor > current_floor:
            return Direction.UP
        if target_floor < current_floor:
            return Direction.DOWN
        return self._call_direction(floor=current_floor)

    def _choose_target(
        self,
        pending_stops: list[int],
        current_floor: int,
        direction: Direction
    ) -> int | None:
        if self._current_floor_is_ready(
            pending_stops=pending_stops,
            current_floor=current_floor,
            direction=direction
        ):
            return current_floor
        if direction == Direction.UP:
            return self._target_preferring(
                pending_stops=pending_stops,
                current_floor=current_floor,
                primary_direction=Direction.UP,
                secondary_direction=Direction.DOWN
            )
        if direction == Direction.DOWN:
            return self._target_preferring(
                pending_stops=pending_stops,
                current_floor=current_floor,
                primary_direction=Direction.DOWN,
                secondary_direction=Direction.UP
            )
        return self._target_when_idle(
            pending_stops=pending_stops,
            current_floor=current_floor
        )

    def _current_floor_is_ready(
        self,
        pending_stops: list[int],
        current_floor: int,
        direction: Direction
    ) -> bool:
        if current_floor not in pending_stops:
            return False
        if current_floor in self._cabin.get_destinations():
            return True
        if self._cabin.is_full():
            return False
        if direction == Direction.IDLE:
            return True
        if self._call_direction(floor=current_floor) == direction:
            return True
        return not self._floors_towards(
            pending_stops=pending_stops,
            current_floor=current_floor,
            direction=direction
        )

    def _target_when_idle(
        self,
        pending_stops: list[int],
        current_floor: int
    ) -> int | None:
        nearest_floor = self._closest_among(
            floors=pending_stops,
            current_floor=current_floor
        )
        if nearest_floor is None:
            return None
        if nearest_floor > current_floor:
            direction = Direction.UP
            return self._target_for_side(
                pending_stops=pending_stops,
                current_floor=current_floor,
                direction=direction
            )
        direction = Direction.DOWN
        return self._target_for_side(
            pending_stops=pending_stops,
            current_floor=current_floor,
            direction=direction
        )

    def _target_preferring(
        self,
        pending_stops: list[int],
        current_floor: int,
        primary_direction: Direction,
        secondary_direction: Direction,
    ) -> int | None:
        primary_target = self._target_for_side(
            pending_stops=pending_stops,
            current_floor=current_floor,
            direction=primary_direction
        )
        if primary_target is not None:
            return primary_target
        return self._target_for_side(
            pending_stops=pending_stops,
            current_floor=current_floor,
            direction=secondary_direction
        )

    def _target_for_side(
        self,
        pending_stops: list[int],
        current_floor: int,
        direction: Direction
    ) -> int | None:
        floors_on_this_side = self._floors_towards(
            pending_stops=pending_stops,
            current_floor=current_floor,
            direction=direction
        )
        compatible_floors = self._compatible_floors(
            floors=floors_on_this_side,
            direction=direction
        )
        if compatible_floors:
            return self._closest_among(
                floors=compatible_floors,
                current_floor=current_floor
            )
        if floors_on_this_side:
            return self._farthest_among(
                floors=floors_on_this_side,
                current_floor=current_floor
            )
        return None

    def _compatible_floors(
        self,
        floors: list[int],
        direction: Direction
    ) -> list[int]:
        cabin_destinations = self._cabin.get_destinations()
        return [
            floor
            for floor in floors
            if floor in cabin_destinations
            or self._call_direction(floor=floor) == direction
        ]

    def _call_direction(self, floor: int) -> Direction:
        if floor == self._building.ground_floor():
            return Direction.UP
        return Direction.DOWN

    def _floors_towards(
        self,
        pending_stops: list[int],
        current_floor: int,
        direction: Direction
    ) -> list[int]:
        if direction == Direction.UP:
            return [floor for floor in pending_stops if floor > current_floor]
        return [floor for floor in pending_stops if floor < current_floor]

    def _closest_among(
        self,
        floors: list[int],
        current_floor: int
    ) -> int | None:
        if not floors:
            return None
        return min(floors, key=lambda floor: abs(floor - current_floor))

    def _farthest_among(
        self, floors: list[int],
        current_floor: int
    ) -> int | None:
        if not floors:
            return None
        return max(floors, key=lambda floor: abs(floor - current_floor))

    def _pending_stops(self) -> list[int]:
        external_stops = [
            group.origin_floor() for group in self._building.all_calls()
        ]
        internal_stops = self._cabin.get_destinations()
        return sorted(set(external_stops + internal_stops))
