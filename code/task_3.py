#!/usr/bin/env python3

"""
This module contains the functions for solving task 3.
Task description:
    Parse the `id` column's middle value (for `bf8d460f-943c-4084-835c-a03dde141041` this is `4084`),
    and use that as an id in the newly generated file.
"""
import glob

import pandas as pd
from types import SimpleNamespace
from code.utils.utils import get_project_root, time_execution


def middle_value(id_string: str) -> str:
    """
    Simple lambda wrapper for extracting the middle value of an id string.
    :param id_string: The id string
    :return: The extracted id
    """
    return id_string.split('-')[2]


def parse_csv_file(file_path: str, target_path: str) -> None:
    """
    parses and cleans the file with uri: 'file_path' and creates a parsed version in 'target_path'
    :param file_path: The file uri
    :param target_path: The target destination for cleaned files
    :return: None
    """
    # Read csv with pandas for convenience
    csv = pd.read_csv(file_path)
    # We assume that the id column holds the same convention for all files i.e. `bf8d460f-943c-4084-835c-a03dde141041`.
    csv['id'] = csv['id'].apply(middle_value)
    new_file_path = get_project_root() + '/' + target_path + file_path.split('/')[-1][:-4] + '.csv'
    csv.to_csv(new_file_path, index_label=False, index=False)


def clean_id_field_and_parse(source_path: str, target_path: str) -> None:
    """
    Cleans the id columns in all .csv files located in 'file_path' and creates new, parsed files in 'target_path'
    :param source_path: The file path where raw .csv files are located
    :param target_path: The target path for parsed .csv files where id fields are cleaned
    :return: None as we generate new files
    """
    files = glob.glob(get_project_root() + '/' + source_path + '*.csv')
    for file in files:
        parse_csv_file(file, target_path)


@time_execution
def task3(config: SimpleNamespace) -> None:
    """
    Executes the solution of third task
    :param config: The configuration file from the initial .yaml
    :type config: SimpleNamespace
    :return: None
    """
    clean_id_field_and_parse(config.get('source'), config.get("sink"))
    return None
