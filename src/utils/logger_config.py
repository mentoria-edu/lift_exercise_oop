from logging import DEBUG, basicConfig


def config_logger() -> None:
    basicConfig(
        level=DEBUG,
        encoding="utf-8",
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
