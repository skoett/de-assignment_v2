#!/usr/bin/env python3
"""
Utility functions for the various tasks
"""
import time
from typing import Callable, Any
from pathlib import Path


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
