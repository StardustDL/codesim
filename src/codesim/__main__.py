import logging
import pathlib
import time
from typing import Optional

import click
from click.exceptions import ClickException

from . import __version__


def measure(src1: str, src2: str) -> float:
    from .langs.cpp.needle import measure
    return measure(src1, src2)


@click.command()
@click.argument("file1", type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=pathlib.Path), default=None)
@click.argument("file2", type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=pathlib.Path), default=None)
@click.option('-v', '--verbose', count=True, default=0, type=click.IntRange(0, 4))
@click.version_option(__version__, package_name="codesim", prog_name="codesim", message="%(prog)s v%(version)s, written by StardustDL.")
def main(file1: pathlib.Path, file2: pathlib.Path, verbose: int = 0) -> None:
    """Codesim (https://github.com/StardustDL/codesim)"""

    logger = logging.getLogger("Cli-Main")

    loggingLevel = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
        4: logging.NOTSET
    }[verbose]

    logging.basicConfig(level=loggingLevel)

    logger.debug(f"Logging level: {loggingLevel}")

    try:
        src1 = file1.read_text(encoding="utf-8")
    except Exception as ex:
        message = f"Failed to read from {file1} in UTF-8 encoding."
        logger.error(message, exc_info=ex)
        raise ClickException(message)
    try:
        src2 = file2.read_text(encoding="utf-8")
    except Exception as ex:
        message = f"Failed to read from {file2} in UTF-8 encoding."
        logger.error(message, exc_info=ex)
        raise ClickException(message)

    try:
        result = measure(src1, src2)
        assert 0 <= result <= 1
    except Exception as ex:
        message = f"Failed to measure code similarity between {file1} and {file2}."
        logger.error(message, exc_info=ex)
        raise ClickException(message)

    print(int(round(result * 1000)) / 10)


if __name__ == '__main__':
    main()
