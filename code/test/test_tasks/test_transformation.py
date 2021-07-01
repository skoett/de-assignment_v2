#!/usr/bin/env python3

"""
This file includes test scenarios and test cases for all code wrt. transformation.
Pytest is the preferred test framework.
"""
from code.test.utils.utils import (assert_object_in_yaml,
                                   assert_object_is_correct_type)

pytest_plugins = ["code.test.pytest_fixtures"]


def test_configuration_contains_transformation(get_configuration) -> None:
    """
    Tests whether the configuration contains an entry for task 2.
    :param get_configuration: The configuration yaml file.
    :return: None
    """
    assert get_configuration.transformation is not None, "'transformation is not in configuration file"
    assert_object_in_yaml("source", get_configuration.transformation, "transformation")
    assert_object_in_yaml("sink", get_configuration.transformation, "transformation")
    assert_object_is_correct_type("source", get_configuration.transformation, str)
    assert_object_is_correct_type("sink", get_configuration.transformation, str)
