#!/usr/bin/env python3
"""
This module contains all utility functions that supports every transformation step.
Each function is designed to only solving one task or problem, thus keeping the code simple, highly modular and
testable.
"""

import glob
import pandas as pd
import numpy as np
from typing import List, Dict
from datetime import datetime

from code.test.utils.utils import (assert_object_in_yaml,
                                   assert_object_is_correct_type)
from code.transform.utils import load_dataframe, get_timestamp

pytest_plugins = ["code.test.pytest_fixtures"]


def test_load_dataframe_from_csv(select_random_file_from_data) -> None:
    """
    Tests whether a data file can be correctly loaded into a pandas DataFrame.
    :return: None.
    """
    try:
        _ = load_dataframe(select_random_file_from_data)
    except FileNotFoundError:
        raise AssertionError("File not found in path.")
    except pd.ParseError:
        raise AssertionError("Cannot parse .csv file.")
    except Exception as e:
        raise AssertionError(f"Some other error happened: {e}.")


def test_timestamp_follows_correct_format(select_random_file_from_data) -> None:
    """
    Tests whether the raw timestamp from the filename follows the correct syntax (yyyy-MM-dd HH:mm:ss).
    :param select_random_file_from_data: A random file from the 'data' directory.
    :return: None.
    """
    timestamp = get_timestamp(select_random_file_from_data)
    print(timestamp)
    try:
        datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValueError("Data format is wrong. Should follow: yyyy-MM-dd HH:mm:ss")
