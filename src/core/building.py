from logging import debug, info
from random import randint
from time import sleep

from utils.chance import Chance
from utils.constant import FLOOR_AMOUNT
from core.passenger import Passenger


class Building:
    CALL_CHANCE = 0.1

    def __init__(self, floor_amount: int = FLOOR_AMOUNT):
        self.floor_amount = floor_amount
        self.calls_waiting: dict = {}

    @property
    def called_floors(self) -> list:
        return set(self.calls_waiting.keys())

    def call_lift(self) -> None:
        floor = randint(0, self.floor_amount)

        if Chance.happens_by_chance(
            self.CALL_CHANCE
        ) and floor not in self.calls_waiting:
            passenger_amount = randint(1, 6)
            self.calls_waiting[floor] = Passenger(
                origin_floor=floor, passenger_amount=passenger_amount
            )
            info(
                f"Floor {floor} called the lift ({passenger_amount} "
                "passenger(s) waiting)."
            )
            sleep(2)

        return None

    def take_passengers(self, floor: int, available_spots: int) -> None:
        passengers_at_floor = self.calls_waiting.get(floor)

        if passengers_at_floor is None:
            return None

        debug(
            f"[TAKE PASSENGERS] CURRENT FLOOR = {floor} | "
            f"PASSENGERS AT FLOOR = {passengers_at_floor.passenger_amount}"
        )

        boarding = min(passengers_at_floor.passenger_amount, available_spots)
        remaining = passengers_at_floor.passenger_amount - boarding
        boarded = Passenger(origin_floor=floor, passenger_amount=boarding)

        if remaining > 0:
            self.calls_waiting[floor].passenger_amount = remaining
        if remaining == 0:
            del self.calls_waiting[floor]

        return boarded
