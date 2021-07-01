#!/usr/bin/env python3

"""
This file contains fixture generator functions task 1 - task 6
Pytest is the preferred test framework
"""
import pickle
from types import SimpleNamespace

import pytest
from datetime import datetime
from typing import List, Union, Tuple, Callable, Dict

from code.utils.utils import setup_config, get_project_root

CONFIG_PATH = "../../config/config.yaml"


@pytest.fixture
def get_configuration() -> SimpleNamespace:
    return setup_config(CONFIG_PATH)


@pytest.fixture
def get_cached_batch_tree(get_configuration) -> Dict[str, str]:
    with open(get_project_root() + get_configuration.task1.get("file_path"), 'rb') as fh:
        batches = pickle.load(fh)
    assert isinstance(batches, Dict), "Cached batch tree is not a dictionary"
    return batches
