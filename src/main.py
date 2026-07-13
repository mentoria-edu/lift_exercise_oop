import random

from building.building import Building
from cabin.cabin import Cabin
from lift.controller import LiftController
from lift.lift import Lift
from lift.scheduler import LiftScheduler
from passengers.passenger import PassengersGroupFactory
from simulation.call_generator import CallGenerator
from simulation.simulation import Simulation
from utils.constants import TOTAL_FLOORS
from utils.logger_config import config_logger


def build_simulation() -> Simulation:
    building = Building(total_floors=TOTAL_FLOORS)
    cabin = Cabin()
    scheduler = LiftScheduler(building=building, cabin=cabin)
    lift = Lift(building=building, cabin=cabin, scheduler=scheduler)
    controller = LiftController(lift=lift)

    passengers_factory = PassengersGroupFactory(
        random_generator=random.Random()
    )
    call_generator = CallGenerator(
        building=building,
        passengers_factory=passengers_factory,
        random_generator=random.Random(),
        call_probability=0.05
    )

    return Simulation(
        controller=controller,
        call_generator=call_generator,
    )


def main() -> None:
    config_logger()
    simulation = build_simulation()
    while True:
        simulation.run()


main()
