import pytest

from core.building import Building
from core.passenger import Passenger


@pytest.fixture
def building():
    return Building()


@pytest.fixture(params=list(range(0, 6 + 1)))
def avaible_spots_parametrize(request):
    return request.param


def test_called_floors_is_empty_when_no_calls_waiting(building):
    assert len(building.called_floors) == 0


def test_called_floors_returns_floors_that_called(
    mocker,
    mock_happens_by_chance_true,
    origin_floor_all_floors,
    passenger_amount_parametrize,
    building
):
    mocker.patch('core.building.randint', side_effect=[
        origin_floor_all_floors,
        passenger_amount_parametrize
    ])

    building.call_lift()

    assert origin_floor_all_floors in building.called_floors


def test_call_lift_adds_call_when_chance_happens(
        mocker,
        mock_happens_by_chance_true,
        passenger_amount_parametrize,
        origin_floor_all_floors,
        building
):
    mocker.patch('core.building.randint', side_effect=[
        origin_floor_all_floors,
        passenger_amount_parametrize
    ])

    building.call_lift()
    assert origin_floor_all_floors in building.calls_waiting


def test_call_lift_not_add_passengers_when_chance_does_not_happen(
        mocker,
        mock_happens_by_chance_false,
        passenger_amount_parametrize,
        origin_floor_all_floors,
        building
):
    mocker.patch('core.building.randint', side_effect=[
        origin_floor_all_floors,
        passenger_amount_parametrize
    ])

    building.call_lift()

    assert len(building.calls_waiting) == 0


def test_call_lift_does_not_overwrite_existing_call_on_same_floor(
        mocker,
        building,
        mock_happens_by_chance_true,
        passenger_amount_parametrize,
        origin_floor_all_floors
    ):
    existing_passenger = Passenger(
        origin_floor=origin_floor_all_floors,
        passenger_amount=passenger_amount_parametrize
    )
    building.calls_waiting[origin_floor_all_floors] = existing_passenger

    mocker.patch('core.building.randint', return_value=origin_floor_all_floors)
    building.call_lift()

    assert building.calls_waiting[
        origin_floor_all_floors
    ].passenger_amount == passenger_amount_parametrize


def test_take_passengers_returns_none_when_no_one_is_waiting(
        building,
        origin_floor_all_floors,
        avaible_spots_parametrize
    ):
    result = building.take_passengers(
        floor=origin_floor_all_floors,
        available_spots=avaible_spots_parametrize
    )

    assert result is None


def test_take_passengers_boards_correct_origin_floor(
        building,
        origin_floor_all_floors,
        passenger_amount_parametrize,
        avaible_spots_parametrize
):
    building.calls_waiting[origin_floor_all_floors] = Passenger(
        origin_floor=origin_floor_all_floors,
        passenger_amount=passenger_amount_parametrize
    )

    result = building.take_passengers(
        floor=origin_floor_all_floors,
        available_spots=avaible_spots_parametrize
    )

    assert result.origin_floor == origin_floor_all_floors
