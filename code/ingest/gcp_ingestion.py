#!/usr/bin/env python3

"""
This module contains the functions for solving the data ingestion task.
Task Description:
    Download files from GitHub in batches of a certain size.
"""
import pickle
from typing import Dict
from types import SimpleNamespace

from google.cloud import storage

from code.ingest.utils import get_batches, fn_parallel
from code.utils.utils import time_execution, get_project_root


def download_batches_from_bucket(destination: str, source: str, batches: Dict) -> None:
    """
    Downloads the batches from the target source bucket using Google Python Libraries.
    :param destination: The target destination.
    :param source: The target source.
    :param batches: The batches data structure.
    :return: None.
    """
    # Setup bucket
    client = storage.Client.create_anonymous_client()
    bucket = client.bucket(bucket_name=source, user_project=None)
    for batch, _ in batches.items():
        fn_calls = []
        for _, v in batches[batch].items():
            blob = storage.Blob(v['path'], bucket)
            fn_calls.append(blob.download_to_filename(filename=get_project_root() + '/' + destination + v['path'],
                                                      client=client))
        fn_parallel(*fn_calls)


@time_execution
def data_ingestion(config: SimpleNamespace) -> None:
    """
    Executes the solution of first task.
    :param config: The configuration file from the initial .yaml.
    :type config: SimpleNamespace.
    :return: None.
    """
    # Create or get batches.
    if config.get("use_cached"):
        with open(get_project_root() + config.get("file_path"), 'rb') as fh:
            batches = pickle.load(fh)
    else:
        batches = get_batches(user=config.get("user"),
                              repo=config.get("repo"),
                              batch_size=config.get("batch_size"),
                              save_tree=config.get("save_tree"),
                              tree_path=config.get("file_path"),
                              repo_url=config.get("repo_url"))

    # Download files into target destination folder.
    download_batches_from_bucket(destination=config.get("sink"),source=config.get("source"), batches=batches)
    return None
