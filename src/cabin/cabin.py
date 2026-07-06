from logging import debug

from passengers.passenger import Passenger

DEFAULT_CAPACITY = 6


class Cabin:
    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        self._capacity = capacity
        self._passengers: list[Passenger] = []

    def available_spots(self) -> int:
        return self._capacity - len(self._passengers)

    def is_empty(self) -> bool:
        return len(self._passengers) == 0

    def is_full(self) -> bool:
        return self.available_spots() == 0

    def occupants_count(self) -> int:
        return len(self._passengers)

    def board(self, passengers: list[Passenger]) -> None:
        boarding_passengers = passengers[: self.available_spots()]
        self._passengers.extend(boarding_passengers)
        debug(f"[board] PASSENGERS ABOARD: {self.occupants_count()}")

    def unboard(self, floor: int) -> list[Passenger]:
        leaving_passengers = self._passengers_going_to(floor)
        self._passengers = self._passengers_not_going_to(floor)
        return leaving_passengers

    def get_destinations(self) -> list[int]:
        unique_destinations = {
            passenger.destination_floor() for passenger in self._passengers
        }
        destinations = sorted(unique_destinations)
        debug(f"[get_destinations] PASSENGERS DESTINATIONS: {destinations}")
        return destinations

    def _passengers_going_to(self, floor: int) -> list[Passenger]:
        going_to_list = [
            passenger
            for passenger in self._passengers
            if passenger.wants_to_get_off_at(floor)
        ]
        return going_to_list

    def _passengers_not_going_to(self, floor: int) -> list[Passenger]:
        not_going_to_list = [
            passenger
            for passenger in self._passengers
            if not passenger.wants_to_get_off_at(floor)
        ]
        return not_going_to_list
