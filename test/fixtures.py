#!/usr/bin/env python3

"""
This file contains fixture generator functions task 1 - task 6
Pytest is the preferred test framework
"""
from types import SimpleNamespace

import pytest
from datetime import datetime
from typing import List, Union, Tuple, Callable

from code.utils.utils import setup_config

CONFIG_PATH = "../../config/config.yaml"


@pytest.fixture
def get_configuration() -> SimpleNamespace:
    return setup_config(CONFIG_PATH)
