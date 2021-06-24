#!/usr/bin/env python3

"""
This module contains the functions for solving task 5.
Task description:
    From the `size` column :
    - filter out all non-integer values and create a new column called `size` of type Integer
    - based on the value of the newly created integer-based `size` column, create a new column called `magnitude`
      that is of the type String. Populate the `magnitude` column by mapping the `size` values to their respective
      range according to the following scheme :
        - `massive` : 500 <= x < 1000
        - `big` : 100 <= x < 500
        - `medium` : 50 <= x < 100
        - `small` : 10 <= x < 50
        - `tiny` : 1 <= x < 10
    - drop the original `size` column
"""

import glob
import pandas as pd
import numpy as np
from types import SimpleNamespace
from code.utils.utils import get_project_root, time_execution


def filter_integer_values(file_path: str) -> pd.DataFrame:
    """
    Opens a csv file and filters out all non-integer values from 'size'.
    Returns a Pandas DataFrame.
    :param file_path: The designated file path for the .csv file.
    :return: A pandas DataFrame.
    """
    df = pd.read_csv(file_path)

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


@time_execution
def task5(config: SimpleNamespace) -> None:
    """
    Executes the solution of the fifth taskcal
    :param config: The configuration file from the initial .yaml
    :type config: SimpleNamespace
    :return: None
    """
    files = glob.glob(get_project_root() + '/' + config.get("source") + '*.csv')
    for file in files:
        silver_df = filter_integer_values(file)
        gold_df = populate_magnitude_column(silver_df)
        gold_df.drop('size', axis=1, inplace=True)
        new_file_path = get_project_root() + '/' + config.get("sink") + file.split('/')[-1][:-4] + '.csv'
        gold_df.to_csv(new_file_path, index_label=False, index=False)
