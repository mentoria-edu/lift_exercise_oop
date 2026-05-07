from core.lift import Lift
from utils.logger_config import config_logger


def exec_lift() -> None:
    config_logger()
    lift = Lift()
    lift.operate_lift()


exec_lift()
