import random
from logging import info

from building.building import Building
from passengers.passenger import PassengersGroupFactory
from utils.constants import DEFAULT_CALL_PROBABILITY


class CallGenerator:
    def __init__(
        self,
        building: Building,
        passengers_factory: PassengersGroupFactory,
        call_probability: float = DEFAULT_CALL_PROBABILITY,
        random_generator: random.Random | None = None,
    ) -> None:
        self._building = building
        self._passengers_factory = passengers_factory
        self._call_probability = call_probability
        self._random_generator = random_generator

    def maybe_generate_call(self) -> None:
        if not self._should_generate_call():
            return False
        self._generate_call()
        return None

    def _should_generate_call(self) -> bool:
        return self._random_generator.random() < self._call_probability

    def _generate_call(self) -> None:
        floor = self._pick_available_floor()
        if floor is None:
            return
        group = self._passengers_factory.create_group(
            origin_floor=floor,
            top_floor=self._building.top_floor()
        )
        self._building.call_floor(group=group)
        info(
            f"Floor {floor} called the lift "
            f"({group.amount()} passengers waiting)"
        )

    def _pick_available_floor(self) -> int | None:
        available_floors = self._floors_without_calls()
        if not available_floors:
            return None
        return self._random_generator.choice(available_floors)

    def _floors_without_calls(self) -> list[int]:
        all_floors = range(
            self._building.ground_floor(),
            self._building.top_floor() + 1
        )
        return [
            floor
            for floor in all_floors
            if not self._building.is_called_at(floor=floor)
        ]
