#!/usr/bin/env python3

"""
This file includes test scenarios and test cases for code regarding ingestion.
Pytest is the preferred test framework.
"""

from code.test.utils.utils import (assert_object_in_yaml,
                                   assert_object_is_correct_type)

pytest_plugins = ["code.test.pytest_fixtures"]
configuration_objects = [('url', str),
                         ('repo_url', str),
                         ('sink', str),
                         ('user', str),
                         ('repo', str),
                         ('batch_size', int),
                         ('file_size', int),
                         ('save_tree', bool),
                         ('use_cached', bool),
                         ('file_path', str),
                         ('download_method', str),
                         ('use_api', bool)]
task = 'ingest'


def test_configuration_contains_ingestion(get_configuration) -> None:
    """
    Tests whether the configuration contains an entry for task 1.
    :param get_configuration: The configuration yaml file.
    :return: None
    """

    assert get_configuration.ingestion is not None, "'task1 is not in configuration file"
    for object_name, type_def in configuration_objects:
        assert_object_in_yaml(object_name, get_configuration.ingestion, "ingest")
        assert_object_is_correct_type(object_name, get_configuration.ingestion, type_def)


def test_configuration_fails_on_wrong_object_name(get_configuration) -> None:
    """
    Tests whether the configuration contains an entry for task 1.
    :param get_configuration: The configuration yaml file.
    :return: None
    """

    assert get_configuration.ingestion is not None, "'task1 is not in configuration file"
    configuration_objects.append(("not_an_object", str))
    try:
        for object_name, type_def in configuration_objects:
            assert_object_in_yaml(object_name, get_configuration.ingestion, "ingest")
            assert_object_is_correct_type(object_name, get_configuration.ingestion, type_def)
    except AssertionError:
        return
    raise AssertionError("Test failed")


def test_configuration_fails_on_wrong_object_type(get_configuration) -> None:
    """
    Tests whether the configuration contains an entry for task 1.
    :param get_configuration: The configuration yaml file.
    :return: None
    """

    assert get_configuration.ingestion is not None, "'task1 is not in configuration file"
    configuration_objects[-1] = ("use_api", str)
    try:
        for object_name, type_def in configuration_objects:
            assert_object_in_yaml(object_name, get_configuration.ingestion, "ingest")
            assert_object_is_correct_type(object_name, get_configuration.ingestion, type_def)
    except AssertionError:
        return
    raise AssertionError("Test failed")


def test_batch_tree_contains_batches(get_cached_batch_tree) -> None:
    keys = list(get_cached_batch_tree.keys())
    batches = list(map(lambda x: x.split('_')[0], keys))
    numbers = list(map(lambda x: x.split('_')[1], keys))
    assert all(number.isdigit() for number in numbers)
    assert all(batch == "batch" for batch in batches)
