from lift.controller import LiftController
from simulation.call_generator import CallGenerator


class Simulation:
    def __init__(
        self,
        controller: LiftController,
        call_generator: CallGenerator,
    ) -> None:
        self._controller = controller
        self._call_generator = call_generator

    def run(self) -> None:
        self._call_generator.maybe_generate_call()
        self._controller.operate_lift()
