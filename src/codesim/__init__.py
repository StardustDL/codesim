import logging
import os
import pathlib
import click

__version__ = "0.0.0"


def get_app_directory():
    return pathlib.Path(__file__).parent


def get_temp_directory():
    result = get_app_directory().joinpath("temp")
    if not result.exists() or not result.is_dir():
        os.makedirs(result)
    return result
