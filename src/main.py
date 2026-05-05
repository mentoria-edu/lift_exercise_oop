from lift import Lift
from logger_config import config_logger


def exec_lift() -> None:
    config_logger()
    lift = Lift()
    lift.operate_lift()


exec_lift()
