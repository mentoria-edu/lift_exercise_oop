import pytest


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr('core.building.sleep', lambda x: None)
    monkeypatch.setattr('core.lift.sleep', lambda x: None)


@pytest.fixture
def mock_happens_by_chance_true(mocker):
    mock_chance_true = mocker.patch(
        'core.passenger.Chance.happens_by_chance'
    )
    mock_chance_true.return_value = True

    return mock_chance_true


@pytest.fixture
def mock_happens_by_chance_false(mocker):
    mock_chance_false = mocker.patch(
        'core.passenger.Chance.happens_by_chance'
    )
    mock_chance_false.return_value = False

    return mock_chance_false


@pytest.fixture(params=list(range(1, 6 + 1)))
def passenger_amount_parametrize(request):
    return request.param


@pytest.fixture(params=list(range(1, 18 + 1)))
def origin_floor_all_except_ground(request):
    return request.param


@pytest.fixture(params=list(range(1, 18 + 1)))
def origin_floor_all_floors(request):
    return request.param


@pytest.fixture(params=list(range(2, 18 + 1)))
def origin_floor_all_except_first_and_ground(request):
    return request.param
