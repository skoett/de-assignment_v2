#!/usr/bin/env python3

"""
This module contains the functions for solving the data ingestion task.
Task Description:
    Download files from GitHub in batches of a certain size.
"""
import pickle
import sys
from types import SimpleNamespace
from typing import Dict
import requests
from multiprocessing.pool import ThreadPool

from code.utils.utils import get_project_root, time_execution


def get_batches(user: str,
                repo: str,
                file_size: int = None,
                batch_size: int = None,
                save_tree: bool = False,
                tree_path: str = None,
                repo_url: str = None) -> Dict:
    """
    Extracts files in either batches or a size constraint form github.
    Puts all downloaded files into the 'destination' location.
    :param user: The github user of Lunarway.
    :param repo: The repository.
    :param file_size: The file_size for file ingestion. Either file_size or batch_size must be None.
    :param batch_size: The batch_size for file ingestion.
    :param save_tree: Whether the response tree should be saved as an object.
    :param tree_path: The relative file path for saving the tree structure.
    :param repo_url: The repository url from Github.
    :return: A dict containing metadata wrt. wanted batches.
    """
    # Ensure that only one of batch_size and file_size is set using logical XOR.
    assert bool(batch_size) != bool(file_size), "Only one of batch_size and file_size must be set"

    # Setup batches data structure and counters
    batches = {"batch_1": {}}
    num_batch = 1
    num_file = 1
    current_file_size = 0

    # Get response for the corresponding github tree.
    target = f"https://api.github.com/repos/{user}/{repo}/git/trees/master?recursive=1"
    res = requests.get(target).json()
    try:
        # Acquire the batches.
        for file in res["tree"]:
            if file["path"].startswith("data/"):

                # Distinguish batching method using lazy evaluation.
                if bool(file_size) and (file_size < current_file_size):
                    num_batch += 1
                    num_file = 1
                    current_file_size = 0
                    batches["batch_" + str(num_batch)] = {}
                if bool(batch_size) and (batch_size < num_file):
                    num_batch += 1
                    num_file = 1
                    batches["batch_" + str(num_batch)] = {}
                batches["batch_" + str(num_batch)]["file_" + str(num_file)] = {"url": file["url"],
                                                                               "size": file["size"],
                                                                               "path": file["path"],
                                                                               "repo_url": repo_url + file["path"]}
                num_file += 1
                current_file_size += file["size"]
    except KeyError as e:
        sys.exit("Exceeded number of API calls to github. Wait 1 hour and try again or use a vpn: KeyError: " + str(e))
    except Exception as e:
        sys.exit(str(e))
    if save_tree:
        full_path = get_project_root() + '/' + tree_path
        with open(full_path, 'wb') as fp:
            pickle.dump(batches, fp, protocol=pickle.HIGHEST_PROTOCOL)
    return batches


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
    # Create batches.
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
