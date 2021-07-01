#!/usr/bin/env python3
"""
This module contains all utility functions that supports every transformation step.
Each function is designed to only solving one task or problem, thus keeping the code simple, highly modular and
testable.
"""

import glob
import pandas as pd
import numpy as np
from typing import List, Dict
from datetime import datetime

from code.utils.utils import get_project_root


def load_dataframe(source_path: str) -> pd.DataFrame:
    """
    Loads in data from 'source_path' into a Pandas DataFrame
    :param source_path: The designated path to the source file
    :return: A Pandas DataFrame
    """
    return pd.read_csv(source_path)


def find_source_files(source_path: str) -> List[str]:
    """
    Acquires all files in source path that is of type '.csv'.
    :param source_path: The file path
    :return: A list of matches to the file extension '.csv'.
    """
    return glob.glob(get_project_root() + '/' + source_path + '*.csv')


def get_timestamp(source_path: str) -> str:
    """
    Gets the timestamp from at absolute file path.
    :param source_path: The absolute file path.
    :return: A string with the datetime in correct syntax.
    """
    dt = ''.join(source_path.split('.')[-2].split('_')[-2:])
    return str(datetime.strptime(dt, '%Y%m%d%H%M%S'))


def get_middle_value(id_string: str) -> str:
    """
    Simple lambda wrapper for extracting the middle value of an id string.
    :param id_string: The id string
    :return: The extracted id
    """
    return id_string.split('-')[2]


def filter_integer_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Opens a csv file and filters out all non-integer values from 'size'.
    Returns a Pandas DataFrame.
    :param df: The designated file path for the .csv file.
    :return: A pandas DataFrame where the 'size' column is assured to be of type 'int'.
    """
    # Assert that the target column exists
    assert 'size' in df.columns, "The size column could not be found!"

    # Cast size column to integer. Recast 'size' column with pd.astype to convert from object to int64
    return df[pd.to_numeric(df['size'], errors='coerce').notnull()].astype({'size': int})


def populate_magnitude_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates the column 'magnitude' and populates it according to the requirements.
    Then it drops the original 'size' column and returns the parsed pd.DataFrame.
    :param df: The DataFrame to be parsed.
    :return: The parsed DataFrame
    """
    df['magnitude'] = np.str
    df['magnitude'] = np.where((df['size'] < 1000) & (df['size'] >= 500), 'massive', df['magnitude'])
    df['magnitude'] = np.where((df['size'] <= 500) & (df['size'] >= 100), 'big', df['magnitude'])
    df['magnitude'] = np.where((df['size'] <= 100) & (df['size'] >= 50), 'medium', df['magnitude'])
    df['magnitude'] = np.where((df['size'] <= 50) & (df['size'] >= 10), 'small', df['magnitude'])
    df['magnitude'] = np.where((df['size'] <= 10) & (df['size'] >= 1), 'tiny', df['magnitude'])
    return df


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


def get_mission(source_path: str) -> str:
    """
    Gets the mission from the source file name.
    :param source_path: The absolute path to the source file.
    :return: A string that an determine the mission of the file.
    """
    return '_'.join(source_path.split('/')[-1].split('_')[:2])