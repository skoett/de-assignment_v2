#!/usr/bin/env python3

"""
This module contains the functions for handling all transformation steps listed in Task 2.
Task description:
 - Extract the `<date>_<time>` components from each file name, and convert that to a timestamp. Add the timestamp as a
   column called `timestamp` in the given file in the format `yyy-MM-dd HH:mm:ss`
 - Parse the `id` column's middle value (for `bf8d460f-943c-4084-835c-a03dde141041` this is `4084`), and use that as
   an id in the newly generated file.
 - Convert all column names to lowercase
 - From the `size` column :
    - filter out all non-integer values and create a new column called `size` of type Integer
    - based on the value of the newly created integer-based `size` column, create a new column called `magnitude` that
      is of the type String. Populate the `magnitude` column by mapping the `size` values to their respective range
      according to the following scheme:
        - `massive` : 500 <= x < 1000
        - `big` : 100 <= x < 500
        - `medium` : 50 <= x < 100
        - `small` : 10 <= x < 50
        - `tiny` : 1 <= x < 10
    - drop the original `size` column
 - Output a single csv file per craft per planet (ex. `rocket_venus.csv`)
"""

from types import SimpleNamespace

from code.utils.utils import time_execution
from code.transform.utils import (find_source_files,
                                  get_unique_rocket_lander_names,
                                  load_dataframe,
                                  get_timestamp,
                                  get_middle_value,
                                  filter_integer_values,
                                  populate_magnitude_column,
                                  get_mission,
                                  create_merged_file)


@time_execution
def transform_data(config: SimpleNamespace) -> None:
    """
    Performs the transformation steps one-by-one.
    :param config: The configuration variables for the transformation steps.
    :return: None.
    """
    # Get all files in source path.
    source_files = find_source_files(config.get('source'))

    # Create merged files data structure for each mission.
    unique_missions = get_unique_rocket_lander_names(source_files)

    for file in source_files:

        # Load in the data into a dataframe object.
        df = load_dataframe(file)

        # Task 1: Extend the '.csv' file with a timestamp column.
        timestamp = get_timestamp(file)
        df['timestamp'] = timestamp

        # Task 2: Parse the 'id' column.
        df['id'] = df['id'].apply(get_middle_value)

        # Task 3: Clean all column names to lowercase.
        df.columns = map(lambda col: col.lower(), df.columns)

        # Task 4: Filter the 'size' column and populate the 'magnitude' column. Drop the 'size' column.
        # Filter and populate the corresponding columns
        df = filter_integer_values(df)
        df = populate_magnitude_column(df)

        # Drop the 'size' column.
        df.drop('size', axis=1, inplace=True)

        # Task 5: Create a merged file for each rocket mission.
        mission = get_mission(file)

        # Create a dictionary from the pd.DataFrame object.
        df_dict = df.to_dict(orient='list')

        # Insert the dictionary into the nested dictionary data structure.
        for header, value in df_dict.items():
            unique_missions[mission].setdefault(header, list())
            unique_missions[mission][header] += value

    # Create merged files for each rocket/lander mission.
    create_merged_file(unique_missions, config.get("sink"))

    return None
