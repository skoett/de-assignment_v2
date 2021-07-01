#!/usr/bin/env python3

"""
This file includes test scenarios and test cases for task 5
Pytest is the preferred test framework
"""

pytest_plugins = ["test.fixtures"]


def test_configuration_contains_task_5(get_configuration) -> None:
    """
    Tests whether the configuration contains an entry for task 5.
    :param get_configuration: The configuration yaml file.
    :return: None
    """
    assert get_configuration.task5 is not None, "'task4 is not in configuration file"
    assert "source" in get_configuration.task5, "'source' is missing from configuration file in task 5"
    assert isinstance(get_configuration.task5.get("source"), str), "'source' is not of type 'string'"
    assert "sink" in get_configuration.task5, "'sink' is missing from configuration file in task 5"
    assert isinstance(get_configuration.task5.get("sink"), str), "'sink' is not of type 'string'"
