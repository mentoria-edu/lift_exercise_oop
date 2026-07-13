from logging import DEBUG, INFO, FileHandler, StreamHandler, basicConfig
from sys import stdout

console_handler = StreamHandler(stream=stdout)
console_handler.setLevel(INFO)

file_handler = FileHandler(filename="debug_logs.txt", mode="w")
file_handler.setLevel(DEBUG)


def config_logger() -> None:
    basicConfig(
        level=DEBUG,
        encoding="utf-8",
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[console_handler, file_handler]
    )
