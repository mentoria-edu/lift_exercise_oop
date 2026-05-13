
from core.passenger import Passenger


def test_destinations_from_ground_floor_never_include_floor_zero(
        passenger_amount_parametrize
):
    passenger = Passenger(
        origin_floor=0,
        passenger_amount=passenger_amount_parametrize
    )

    destinations = passenger.get_destinations()

    assert 0 not in destinations


def test_passenger_amount_parametrize_matches_number_of_destinations_generated(
        origin_floor_all_floors,
        passenger_amount_parametrize
):
    passenger = Passenger(
        origin_floor=origin_floor_all_floors,
        passenger_amount=passenger_amount_parametrize
    )

    destinations = passenger.get_destinations()

    assert len(destinations) <= passenger.passenger_amount


def test_passenger_from_upper_floor_can_go_to_ground(
        mock_happens_by_chance_false,
        origin_floor_all_except_ground,
        passenger_amount_parametrize
    ):
    passenger = Passenger(
        origin_floor=origin_floor_all_except_ground,
        passenger_amount=passenger_amount_parametrize
    )

    destinations = passenger.get_destinations()

    assert 0 in destinations


def test_passenger_from_floor_1_always_goes_to_ground_even_if_chance_is_true(
        mock_happens_by_chance_true,
        passenger_amount_parametrize
    ):
    passenger = Passenger(
        origin_floor=1,
        passenger_amount=passenger_amount_parametrize
    )
    expected_destinations = [0 for _d in range(
        1,
        passenger.passenger_amount + 1
    )]

    destinations = passenger.get_destinations()

    assert destinations == expected_destinations


def test_passenger_from_upper_floor_can_go_to_intermediate_floor(
        mock_happens_by_chance_true,
        origin_floor_all_except_first_and_ground,
        passenger_amount_parametrize
):
    passenger = Passenger(
        origin_floor=origin_floor_all_except_first_and_ground,
        passenger_amount=passenger_amount_parametrize
    )

    destinations = passenger.get_destinations()
    assert 0 not in destinations


def test_passenger_from_upper_floor_does_not_go_to_same_or_higher_floor(
        origin_floor_all_except_ground,
        passenger_amount_parametrize
):
    passenger = Passenger(
        origin_floor=origin_floor_all_except_ground,
        passenger_amount=passenger_amount_parametrize
    )

    destinations = passenger.get_destinations()
    expected_destination = [
        d for d in destinations if d < passenger.origin_floor
    ]

    assert len(destinations) == len(expected_destination)
