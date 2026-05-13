import pytest

from utils.chance import Chance


@pytest.fixture
def mock_random(mocker):
    mocker.patch('utils.chance.random', return_value=0.5)


def test_happens_by_chance_returns_true_if_random_is_below_modifier(
        mock_random
    ):
    result = Chance.happens_by_chance(0.9)

    assert result is True


def test_happens_by_chance_returns_false_if_random_is_above_modifier(
        mock_random
    ):
    result = Chance.happens_by_chance(0.1)

    assert result is False


def test_happens_by_chance_returns_true_if_random_equals_modifier(
        mock_random
    ):
    result = Chance.happens_by_chance(0.5)

    assert result is True


def test_happens_by_chance_with_zero_chance_returns_false(
        mock_random
    ):
    result = Chance.happens_by_chance(0.0)

    assert result is False


@pytest.mark.parametrize('chance_modifier', [(1.0), (1.1), (-0.1), (2)])
def test__happens_by_chance_raises_error_with_invalid_entry(chance_modifier):
    with pytest.raises(ValueError):
        Chance.happens_by_chance(chance_modifier=chance_modifier)
