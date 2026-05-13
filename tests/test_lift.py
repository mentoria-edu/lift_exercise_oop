import pytest

from core.direction import Direction
from core.lift import Lift


@pytest.fixture
def lift():
    return Lift()


@pytest.fixture
def lift_at_all_floors(lift, origin_floor_all_floors):
    lift.current_floor = origin_floor_all_floors
    return lift


@pytest.fixture
def lift_going_up(lift):
    lift.direction = Direction.UP
    return lift


@pytest.fixture
def lift_going_down(lift):
    lift.direction = Direction.DOWN
    return lift


def test_next_stop_returns_none_when_no_stops(lift):
    result = lift.next_stop()
    assert result is None


def test_next_stop_returns_closest_floor_when_idle(
        lift,
        passenger_amount_parametrize
    ):
    lift.building.calls_waiting[3] = passenger_amount_parametrize
    lift.building.calls_waiting[7] = passenger_amount_parametrize
    lift.current_floor = 4
    result = lift.next_stop()
    assert result == 3
