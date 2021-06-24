#!/usr/bin/env python3

"""
This module contains the functions for solving task 6.
Task description:
    Output a single csv file per craft per planet (ex. `rocket_venus.csv`)
"""

import glob
import csv
import pandas as pd
from typing import List, Dict
from types import SimpleNamespace
from code.utils.utils import get_project_root, time_execution


def get_unique_rocket_lander_names(files: List[str]) -> Dict[str, Dict[str, List]]:
    """
    Finds all unique rocket names from a list of file names.
    :param files: The list of file names.
    :return: A list of unique names or new files.
    """
    # We assume the pattern: rocket_<planet>_XXX_XXX.csv
    # First, we split on the last '/' to ensure the file name, then we get the first two names separated by '_'.
    # Set is used to remove duplicates and is afterwards casted to list for convenience.
    unique_names = list(set(['_'.join(name.split('/')[-1].split('_')[:2]) for name in files]))
    return {key: {} for key in unique_names}


def get_rocket_lander_data_structure(files: List[str], names: Dict[str, Dict[str, List]]) -> Dict[str, Dict[str, List]]:
    """
    Fills the data structure where keys are unique names, e.g. lander_venus with associated file paths as values
    in a list
    :param files: The list of all file paths to parsed files.
    :param names: The data structure where keys are unique missions and values are empty lists.
    :return: A filled data structure in the form of 'names'.
    """
    for file in files:
        for key, data in names.items():
            if key in file:
                with open(file, 'rU') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        for header, value in row.items():
                            data.setdefault(header, list()).append(value)
    return names


def create_merged_file(lander_dict: Dict[str, Dict[str, List]], files_path: str) -> None:
    """
    Takes a dictionary with keys as unique lander/rocket missions and corresponding file paths as values.
    Creates a merged .csv file for each key.
    :param lander_dict: The corresponding data structure as dict.
    :param files_path: The path where the merged files should be located.
    :return: None.
    """
    for mission_name, file_dicts in lander_dict.items():
        file_uri = get_project_root() + '/' + files_path + mission_name + '.csv'
        pd.DataFrame.from_dict(file_dicts).to_csv(file_uri, index_label=False, index=False)


@time_execution
def task6(config: SimpleNamespace) -> None:
    """
    Executes the solution of the sixth task
    :param config: The configuration file from the initial .yaml
    :type config: SimpleNamespace
    :return: None
    """
    files = glob.glob(get_project_root() + '/' + config.get("source") + '*.csv')
    unique_names = get_unique_rocket_lander_names(files)

    names = get_rocket_lander_data_structure(files, unique_names)
    create_merged_file(names, config.get("sink"))
