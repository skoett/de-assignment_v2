#!/usr/bin/env python3

"""
This module contains the functions for solving task 4.
Task description:
    Convert all column names to lowercase
"""
import glob
import csv
from types import SimpleNamespace
from code.utils.utils import get_project_root, time_execution


def header_to_lower(file_path: str, target_path: str) -> None:
    """
    Opens a .csv file, lower-cases the header and saves the new file to 'target_path' destination.
    :param file_path: The input file.
    :param target_path: The target destination.
    :return: None
    """
    new_file_path = get_project_root() + '/' + target_path + file_path.split('/')[-1][:-4] + '.csv'
    with open(file_path, 'r') as infile, open(new_file_path, 'w') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(list(map(lambda header: header.lower(), next(reader, None))))
        for row in reader:
            writer.writerow(row)


def clean_headers_to_lower(source_path: str, target_path: str) -> None:
    """
    Cleans all headers in all .csv files located in source path
    :param source_path: The source location of files
    :param target_path: The target location of files
    :return: None as we create new files
    """
    files = glob.glob(get_project_root() + '/' + source_path + '*.csv')

    # Acquire all headers from csv and flatten nested list of headers
    [header_to_lower(f, target_path) for f in files]


@time_execution
def task4(config: SimpleNamespace) -> None:
    """
    Executes the solution of fourth task
    :param config: The configuration file from the initial .yaml
    :type config: SimpleNamespace
    :return: None
    """
    clean_headers_to_lower(config.get('source'), config.get('sink'))
    return None
