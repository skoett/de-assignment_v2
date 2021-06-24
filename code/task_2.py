#!/usr/bin/env python3

"""
This module contains the functions for solving task 2.
Task description:
    Extract the <date>_<time> components from each file name, and convert that to a timestamp.
    Add the timestamp as a column called timestamp in the given file in the format yyy-MM-dd HH:mm:ss
"""
import glob
import numpy as np

import csv
from datetime import datetime
from types import SimpleNamespace
from code.utils.utils import get_project_root, time_execution


def filename_to_timestamp(file_path: str, target_path: str) -> None:
    """
    Lambda wrapper to extract timestamps from filenames
    :param file_path: The source filename.
    :param target_path: The target filename.
    :return: None
    """
    # Extract the date and time from filenames
    # We assume the name convention local_path/proj_root/path_to_data/lander_planet_date_time.csv
    dt = ''.join(file_path.split('.')[-2].split('_')[-2:])
    new_target_path = get_project_root() + '/' + target_path + file_path.split('/')[-1]
    with open(file_path, 'r') as infile, open(new_target_path, 'w') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(next(reader) + ['timestamp'])
        for row in reader:
            writer.writerow(row + [str(datetime.strptime(dt, '%Y%m%d%H%M%S'))])


def get_unique_col_names(source_path: str, sink_path: str) -> None:
    """
    Gets all unique column names for all csv files in file path.
    :param source_path: The file path
    :param sink_path: The target file path
    :return: None
    """
    # Get all files in data directory
    files = glob.glob(get_project_root() + '/' + source_path + '*.csv')

    # Get all timestamps from filenames
    [filename_to_timestamp(f, sink_path) for f in files]


@time_execution
def task2(config: SimpleNamespace) -> None:
    """
    Executes the solution of second task
    :param config: The configuration file from the initial .yaml
    :type config: SimpleNamespace
    :return: None
    """
    get_unique_col_names(config.get('source'), config.get("sink"))
