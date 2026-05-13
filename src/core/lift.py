from logging import debug, info
from time import sleep

from core.building import Building
from core.direction import Direction
from utils.constant import LIFT_CAPACITY


class Lift:
    def __init__(self):
        self.building = Building()
        self.lift_capacity = LIFT_CAPACITY

        self.current_floor = 0
        self.passengers_aboard = 0
        self.destinations = []
        self.direction = Direction.IDLE

    @property
    def available_spots(self) -> int:
        available_spots = self.lift_capacity - self.passengers_aboard

        return available_spots

    @property
    def is_empty(self) -> bool:
        check = self.passengers_aboard == 0
        return check

    @property
    def is_idle(self) -> bool:
        check = self.is_empty and not self.building.called_floors
        return check

    @property
    def all_stops(self) -> set:
        if not self.is_empty:
            return set(self.destinations)
        return self.building.called_floors

    def next_stop(self) -> int | None:
        stops = self.all_stops

        if not stops:
            return None

        floors_above = [
            floor for floor in stops if floor > self.current_floor
        ]
        floors_below = [
            floor for floor in stops if floor < self.current_floor
        ]

        if self.direction == Direction.UP:
            target = self._set_target_up_direction(
                floors_below=floors_below,
                floors_above=floors_above
            )

        if self.direction == Direction.DOWN:
            target = self._set_target_down_direction(
                floors_above=floors_above,
                floors_below=floors_below
            )

        if self.direction == Direction.IDLE:
            target = min(
                stops,
                key=lambda floor: abs(floor - self.current_floor)
            )

        debug(f"[NEXT STOP] TARGET = {target}")
        return target

    def _set_target_up_direction(self, floors_below, floors_above):
        if not floors_above:
            target = max(floors_below)
            return target

        if self.is_empty:
            target = max(floors_above)
            return target

        if not self.is_empty:
            target = min(floors_above)
            return target

    def _set_target_down_direction(self, floors_below, floors_above):
        if not floors_below:
            target = max(floors_above)
            return target

        if self.is_empty:
            target = max(floors_below)
            return target

        if not self.is_empty:
            target = min(floors_below)
            return target

    def update_direction(self, target: int) -> None:
        if target > self.current_floor:
            self.direction = Direction.UP
        if target < self.current_floor:
            self.direction = Direction.DOWN
        if target is None:
            self.direction = Direction.IDLE
        debug(
            f"[UPDATE DIRECTION] DIRECTION = {self.direction.name} | "
            f"TARGET = {target}"
        )

    def unboard(self) -> None:
        count = self.destinations.count(self.current_floor)
        if count == 0:
            return None

        info(f"{count} passenger(s) unboarded at floor {self.current_floor}.")
        sleep(2)

        self.passengers_aboard -= count
        self.destinations = [
            dest for dest in self.destinations if dest != self.current_floor
        ]
        return None

    def board(self) -> None:
        if not self.is_empty and self.direction == Direction.UP:
            return None

        passengers_at_floor = self.building.calls_waiting.get(
            self.current_floor
        )
        if self.available_spots == 0:
            if passengers_at_floor:
                info(
                    "Lift is full. "
                    f"{passengers_at_floor.passenger_amount} "
                    "passenger(s) at "
                    f"floor {self.current_floor} will have to wait."
                )
            return None

        boarded = self.building.take_passengers(
            floor=self.current_floor,
            available_spots=self.available_spots,
        )
        if boarded is None:
            return None

        info(
            f"{boarded.passenger_amount} passenger(s) boarded from "
            f"floor no. {self.current_floor}."
        )

        sleep(3)

        new_destinations = boarded.get_destinations()
        self.destinations.extend(new_destinations)
        self.passengers_aboard += boarded.passenger_amount

    def open_doors(self) -> None:
        info(f"Lift stopped at floor {self.current_floor}. Doors open.")
        sleep(2)
        self.unboard()
        self.board()
        info("Doors closed.")
        sleep(2)

    def move(self) -> bool:
        self.building.call_lift()

        target = self.next_stop()

        debug(f"[MOVE] TARGET = {target}")

        if target is None:
            self.direction = Direction.IDLE
            return False

        self.update_direction(target)

        if self.direction == Direction.UP:
            self.current_floor += 1
            info(f"Going up: Floor {self.current_floor}")
            sleep(1)

        if self.direction == Direction.DOWN:
            self.current_floor -= 1
            info(f"Going down: Floor {self.current_floor}")
            sleep(1)

        should_stop = any([
            self.current_floor in self.destinations,
            self.current_floor == target,
            self.direction == Direction.DOWN and
            self.current_floor in self.building.called_floors
        ])

        if should_stop:
            self.open_doors()

        debug(
            f"[MOVE] current floor = {self.current_floor} "
            f"direction = {self.direction.name} "
            f"passengers aboard = {self.passengers_aboard} "
            f"destinations = {self.destinations} "
            f"called floors = {self.building.called_floors}"
        )

        return True

    def stand_by(self) -> None:
        self.direction = Direction.IDLE
        debug(
            f"[STAND BY] Direction = {self.direction.name} | "
            f"Current Floor = {self.current_floor}"
        )
        info(f"No calls. Lift waiting at floor no. {self.current_floor}.")

    def operate_lift(self) -> None:
        while True:
            if self.is_idle:
                self.stand_by()
                while self.is_empty and not self.building.called_floors:
                    sleep(2)
                    self.building.call_lift()

            debug(
                f"[OPERATE LIFT] Current floor = {self.current_floor} | "
                f"Passengers aboard = {self.passengers_aboard}/"
                f"{self.lift_capacity} | "
                f"Destinations = {self.destinations} | "
                f"Called floors = {sorted(self.building.called_floors)}"
            )

            moved = self.move()

            if not moved and self.all_stops:
                self.open_doors()
