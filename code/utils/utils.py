#!/usr/bin/env python3
"""
Utility functions for the various tasks
"""
import time
import yaml
from types import SimpleNamespace
from pathlib import Path
from typing import Callable, Any



def get_project_root() -> str:
    return str(Path(__file__).parent.parent.parent)


def time_execution(func: Callable) -> Callable:
    """
    A decorator function at enables us to measure time in function calls.
    :param func: The function that we want to call
    :return: The wrapper function
    """
    def wrapper(*args, **kwargs) -> Any:
        """The wrapper function"""
        start = time.time()
        val = func(*args, **kwargs)
        print(f"Execution of '{func.__name__}' took: {round(time.time() - start, 2)} seconds")
        return val
    return wrapper


def setup_config(config_path) -> SimpleNamespace:
    with open(config_path) as stream:
        config_file = yaml.safe_load(stream)
    return SimpleNamespace(**config_file)
