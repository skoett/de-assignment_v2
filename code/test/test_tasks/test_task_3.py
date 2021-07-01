#!/usr/bin/env python3

"""
This file includes test scenarios and test cases for task 3
Pytest is the preferred test framework
"""

pytest_plugins = ["test.fixtures"]


def test_configuration_contains_task_3(get_configuration) -> None:
    """
    Tests whether the configuration contains an entry for task 3.
    :param get_configuration: The configuration yaml file.
    :return: None
    """
    assert get_configuration.task3 is not None, "'task3 is not in configuration file"
    assert "git_path" in get_configuration.task3, "'git_path' is missing from configuration file in task 3"
    assert isinstance(get_configuration.task3.get("git_path"), str), "'git_path' is not of type 'string'"
    assert "source" in get_configuration.task3, "'source' is missing from configuration file in task 3"
    assert isinstance(get_configuration.task3.get("source"), str), "'source' is not of type 'string'"
    assert "sink" in get_configuration.task3, "'sink' is missing from configuration file in task 3"
    assert isinstance(get_configuration.task3.get("sink"), str), "'sink' is not of type string"
