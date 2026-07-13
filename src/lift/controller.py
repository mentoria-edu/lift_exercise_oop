from logging import debug, info
from time import sleep

from enums.direction import Direction
from lift.lift import Lift
from passengers.passenger import Passenger
from utils.constants import PAUSE_SECONDS


class LiftController:
    def __init__(self, lift: Lift) -> None:
        self._lift = lift
        self._direction = Direction.IDLE

    def current_floor(self):
        return self._lift.current_floor()

    def operate_lift(self) -> None:
        if self._lift_has_arrived():
            self._stop_at_floor(pause_seconds=PAUSE_SECONDS)
            self._update_direction()
            return
        self._update_direction()
        if self._lift.is_idle():
            self._stand_by(pause_seconds=PAUSE_SECONDS)
            return
        self._move()

    def _lift_has_arrived(self) -> bool:
        if self._lift.is_idle():
            return False
        return self._lift.has_reached_target()

    def _update_direction(self) -> None:
        incoming_direction = self._direction
        self._lift.recalculate_target(direction=incoming_direction)
        self._direction = self._lift.preview_direction(
            direction=incoming_direction
        )
        debug(
            f"[_update_direction] CURRENT FLOOR: {self.current_floor()}"
        )
        debug(
            f"[_update_direction] DIRECTION: {self._direction.name}"
        )

    def _stand_by(self, pause_seconds: float) -> None:
        info(
            f"No calls. Lift waiting at floor no. {self.current_floor()}."
        )
        sleep(pause_seconds)

    def _move(self) -> None:
        self._lift.move_one_floor_towards(
            self._lift.target_floor(),
            pause_seconds=PAUSE_SECONDS
        )
        info(f"Going {self._direction_word()}: floor {self.current_floor()}")

    def _direction_word(self) -> str:
        if self._direction == Direction.UP:
            return "up"
        return "down"

    def _stop_at_floor(self, pause_seconds: float) -> None:
        current_floor = self._lift.current_floor()
        info(f"Lift stopped at floor {current_floor}. Doors Open")
        sleep(pause_seconds)
        self._handle_unboarding(
            current_floor=current_floor,
            pause_seconds=PAUSE_SECONDS
        )
        self._handle_boarding(
            current_floor=current_floor,
            pause_seconds=PAUSE_SECONDS
        )
        info("Doors Closed")
        sleep(pause_seconds)

    def _handle_unboarding(
            self,
            current_floor: int,
            pause_seconds: float
        ) -> None:
        leaving_passengers = self._lift.unboard_passengers()
        self._log_unboarding(
            passengers=leaving_passengers,
            current_floor=current_floor
        )
        sleep(pause_seconds)

    def _log_unboarding(
            self,
            passengers: list[Passenger],
            current_floor: int
        ) -> None:
        if not passengers:
            return
        info(
            f"{len(passengers)} passengers unboarded at floor {current_floor}"
        )

    def _handle_boarding(
            self,
            current_floor: int,
            pause_seconds: float
        ) -> None:
        boarding_direction = self._lift.preview_direction(
            direction=self._direction
        )
        if not self._lift.call_is_compatible_with(
            direction=boarding_direction
        ):
            return
        boarding_passengers = self._lift.board_waiting_passengers()
        self._log_boarding(
            passengers=boarding_passengers
        )
        self._log_full_lift_if_needed(
            current_floor=current_floor
        )
        sleep(pause_seconds)

    def _log_boarding(self, passengers: list[Passenger]) -> None:
        if not passengers:
            return
        destinations = ",".join(
            str(passenger.destination_floor()) for passenger in passengers
        )
        info(
            f"{len(passengers)} passengers boarded, "
            f"they're heading towards floors: {destinations}"
        )

    def _log_full_lift_if_needed(self, current_floor: int) -> None:
        remaining_passengers = self._lift.remaining_passengers_waiting()
        if remaining_passengers == 0:
            return
        info(
            f"Lift is full. {remaining_passengers} passengers at "
            f"floor {current_floor} will have to wait"
        )
