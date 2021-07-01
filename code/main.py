#!/usr/bin/env python3

"""
This module contains the main loop for execution the solution to Lunar's Data Engineering Python assignment.
The assignment involves the small-files problem in a space setting.
"""

from code.ingest.ingestion import data_ingestion
from code.transform.transformation import transform_data
from code.transform.task_2 import task2
from code.transform.task_3 import task3
from code.transform.task_4 import task4
from code.transform.task_5 import task5
from code.transform.task_6 import task6

from code.utils.utils import time_execution, setup_config

CONFIG_PATH = "../config/config.yaml"


@time_execution
def main() -> None:
    """
    Main loop
    :return: None
    """
    config = setup_config(CONFIG_PATH)
    # Task 1 - Download files from Github in batches of a certain size.
    # data_ingestion(config.ingestion)

    # Task 2 - Transform data
    transform_data(config.transformation)

    # Task 2 - Extract the <date>_<time> components from each file name, and convert that to a timestamp.
    # Add the timestamp as a column called timestamp in the given file in the format yyy-MM-dd HH:mm:ss
    # task2(config.task2)

    # Task 3 - Parse the `id` column's middle value (for `bf8d460f-943c-4084-835c-a03dde141041` this is `4084`),
    # and use that as an id in the newly generated file.
    # task3(config.task3)

    # Task 4 - Convert all column names to lowercase
    # task4(config.task4)

    # Task 5 - Transform the size column
    # task5(config.task5)

    # Task 6 - Output a single csv file per craft per planet (ex. `rocket_venus.csv`)
    # task6(config.task6)


main()
