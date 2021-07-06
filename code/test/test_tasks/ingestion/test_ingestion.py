#!/usr/bin/env python3
"""
This module contains all utility functions that supports every transformation step.
Each function is designed to only solving one task or problem, thus keeping the code simple, highly modular and
testable.
"""

import glob
import os
from typing import List, Dict
from datetime import datetime

from code.test.utils.utils import (assert_object_in_yaml,
                                   assert_object_is_correct_type)
from code.ingest.ingestion import get_files
from code.utils.utils import get_project_root

pytest_plugins = ["code.test.pytest_fixtures"]


def test_download_single_file(get_cached_batch_tree) -> None:
    """
    Tests whether a single file can be downloaded with the information provided in the cached batch tree.
    :param get_cached_batch_tree: The cached batch tree.
    :return: None
    """
    batch_1 = get_cached_batch_tree.get('batch_1')
    file_1 = {"batch_1": batch_1.get('file_1')}
    tmp_dir = "code/test/temp_files/"
    directory = glob.glob(get_project_root() + "/" + tmp_dir + "data/*.csv")
    assert len(directory) == 0
    get_files(destination=tmp_dir, batches=file_1)
    directory = glob.glob(get_project_root() + "/" + tmp_dir + "data/*.csv")
    assert len(directory) == 1
    for file in directory:
        os.remove(file)
