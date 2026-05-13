from logging import info
from random import randint, sample

from utils.chance import Chance
from utils.constant import FLOOR_AMOUNT


class Passenger:
    def __init__(self, origin_floor: int, passenger_amount: int):
        self.origin_floor = origin_floor
        self.passenger_amount = passenger_amount

    def get_destinations(self) -> list:
        destinations = []

        if self.origin_floor == 0:
            floor_picker = sample(
                range(1, FLOOR_AMOUNT),
                self.passenger_amount
            )
            destinations = floor_picker

        if self.origin_floor > 0:
            for _passenger in range(self.passenger_amount):
                if Chance.happens_by_chance(0.5) and self.origin_floor > 1:
                    destinations.append(randint(1, self.origin_floor - 1))
                else:
                    destinations.append(0)

        destinations_set = sorted(set(destinations))
        string_destinations_set = map(str, destinations_set)
        string_destinations = ", ".join(string_destinations_set)

        if self.passenger_amount == 1:
            info(
                f"{self.passenger_amount} passenger boarded is heading to "
                f"floor(s): {string_destinations}."
            )

        if self.passenger_amount > 1:
            info(
                f"{self.passenger_amount} passengers boarded are heading to "
                f"floor(s): {string_destinations}."
            )

        return destinations
