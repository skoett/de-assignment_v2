#!/usr/bin/env python3

"""
This file includes test scenarios and test cases for task 1
Pytest is the preferred test framework
"""

pytest_plugins = ["test.fixtures"]


def test_configuration_contains_task_1(get_configuration) -> None:
    """
    Tests whether the configuration contains an entry for task 1.
    :param get_configuration: The configuration yaml file.
    :return: None
    """
    assert get_configuration.task1 is not None, "'task1 is not in configuration file"
    assert "url" in get_configuration.task1, "'url' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("url"), str), "'url' is not of type 'string'"
    assert "repo_url" in get_configuration.task1, "'repo_url' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("repo_url"), str), "'repo_url' is not of type 'string'"
    assert "sink" in get_configuration.task1, "'sink' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("sink"), str), "'sink' is not of type string"
    assert "user" in get_configuration.task1, "'user' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("user"), str), "'user' is not of type string"
    assert "repo" in get_configuration.task1, "'repo' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("url"), str), "'url' is not of type string"
    assert "batch_size" in get_configuration.task1, "'batch_size' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("batch_size"), int), "'batch_size' is not of type int"
    assert "file_size" in get_configuration.task1, "'file_size' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("file_size"), int), "'file_size' is not of type int"
    assert "save_tree" in get_configuration.task1, "'save_tree' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("save_tree"), bool), "'save_tree' is not of type bool"
    assert "use_cached" in get_configuration.task1, "'use_cached' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("use_cached"), bool), "'use_cached' is not of type bool"
    assert "file_path" in get_configuration.task1, "'file_path' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("file_path"), str), "'file_path' is not of type string"
    assert "download_method" in get_configuration.task1, "'download_method' is missing from configuration file in" \
                                                         "task 1"
    assert isinstance(get_configuration.task1.get("download_method"), str), "'download_method' is not of type string"
    assert "use_api" in get_configuration.task1, "'use_api' is missing from configuration file in task 1"
    assert isinstance(get_configuration.task1.get("use_api"), bool), "'use_api' is not of type bool"
