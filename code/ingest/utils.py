#!/usr/bin/env python3
"""
This module contains all utility functions that supports the ingestion process.
Each function is designed to only solving one task or problem, thus keeping the code simple, highly modular and
testable.
"""
import pickle
import sys
from multiprocessing import Process

import requests
from typing import Dict
from code.utils.utils import get_project_root


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


def fn_parallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()
