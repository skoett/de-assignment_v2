#!/usr/bin/env python3

"""
This file contains fixture generator functions task 1 - task 6
Pytest is the preferred test framework
"""
import pickle
import pytest
import glob
import random
from types import SimpleNamespace
from typing import Dict

from code.utils.utils import setup_config, get_project_root

CONFIG_PATH = "/config/config.yaml"


@pytest.fixture
def get_configuration() -> SimpleNamespace:
    """
    Loads in the configuration.
    :return: The configuration as a SimpleNamespace object.
    """
    return setup_config(get_project_root() + CONFIG_PATH)


@pytest.fixture
def get_cached_batch_tree(get_configuration) -> Dict[str, str]:
    """
    Loads in the cached batch tree from Artefacts.
    :param get_configuration: The get_configuration file object.
    :return: The batch tree dictionary.
    """
    with open(get_project_root() + get_configuration.ingestion.get("file_path"), 'rb') as fh:
        batches = pickle.load(fh)
    assert isinstance(batches, Dict), "Cached batch tree is not a dictionary"
    return batches


@pytest.fixture
def select_random_file_from_data(get_configuration) -> str:
    """
    Selects a random .csv file from the 'data' directory.
    :param get_configuration: The configuration object to get the data directory path from.
    :return: The absolute path to a random .csv file.
    """
    dir_path = get_project_root() + "/" + get_configuration.transformation.get("source")
    return random.choice(glob.glob(dir_path + '*.csv'))
