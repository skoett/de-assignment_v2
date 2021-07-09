#!/usr/bin/env python3

"""
This module contains the functions for solving the data ingestion task.
Task Description:
    Download files from GitHub in batches of a certain size.
"""
import pickle
import requests
from typing import Dict
from types import SimpleNamespace
from multiprocessing.pool import ThreadPool

from code.ingest.utils import get_batches
from code.utils.utils import get_project_root, time_execution


def download_batches(destination: str, batches: Dict, method: str = "parallel", use_api: bool = False) -> None:
    """
    Wrapper function for downloading batches in either single or parallel execution.
    :param destination: The target destination.
    :param batches: The batches data structure.
    :param method: Can either be "parallel" or "single".
    :param use_api: Whether the Github API should be used to download files or raw URL's.
    :return: None
    """
    assert method in ["parallel", "single"], "method must bet either 'parallel' or 'single'"
    print(f"number of batches: {len(batches.keys())}. Download method is {method}")
    if method == "single":
        for batch, _ in batches.items():
            get_files(destination=destination, batches=batches[batch], use_api=use_api)
    if method == "parallel":
        for batch, _ in batches.items():
            get_files(destination=destination, batches=batches[batch])
            ThreadPool(8).imap_unordered(get_files, [destination, batches[batch], use_api])


def get_files(destination: str, batches: Dict, use_api: bool = False) -> None:
    """
    Downloads all files in batches to destination without parallelism and usage of batches.
    :param destination: The target destination.
    :param batches: The batches data structure.
    :param use_api: Whether the Github API should be used to download files or raw URL's.
    :return: None.
    """
    # TODO: Optimize ThreadPool on batch level
    for _, v in batches.items():
        print(f"downloading {v['url'] if use_api else v['repo_url']} ..")
        r = requests.get(v['url'], stream=True) if use_api else requests.get(v["repo_url"], stream=True)
        if r.status_code == 200:
            with open((get_project_root() + '/' + destination + v['path']), 'wb') as f:
                for chunk in r:
                    f.write(chunk)


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
    download_batches(destination=config.get("sink"), batches=batches, method=config.get("download_method"))
    return None
