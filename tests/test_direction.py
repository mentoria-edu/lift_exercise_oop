from core.direction import Direction


def test_direction_up_has_value_1():
    assert Direction.UP.value == 1


def test_direction_down_has_value_minus_1():
    assert Direction.DOWN.value == -1


def test_direction_idle_has_value_0():
    assert Direction.IDLE.value == 0
