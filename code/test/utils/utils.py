#!/usr/bin/env python3

"""
This file includes all utility functions for all pytest functions and test cases.
Pytest is the preferred test framework.
"""
from types import SimpleNamespace
from typing import Tuple, Any


def assert_object_in_yaml(object_name: str, config: SimpleNamespace, task_name: str) -> None:
    """
    Wrapper function to ease the code density in test cases.
    Wraps an assertion case that checks whether the object is in the configuration.
    :param object_name: The object to look for in the yaml configuration file.
    :param config: The subset of the configuration file as a 'SimpleNamespace' object.
    :param task_name: The task name of the current task.
    :return: None
    """
    assert object_name in config, f"{object_name} is missing from configuration file in {task_name}"


def assert_object_is_correct_type(object_name: str, config: SimpleNamespace, object_type: Any) -> None:
    """
    Wrapper function to ease the code density in test cases.
    Wraps an assertion case that checks a type of an object in the configuration.
    :param object_name: The object to look for in the yaml configuration file.
    :param config: The subset of the configuration file as a 'SimpleNamespace' object.
    :param object_type: The type designation of the object.
    :return: None
    """
    assert isinstance(config.get(object_name), object_type), f"{object_name} is not of type: {str(object_type)}"
