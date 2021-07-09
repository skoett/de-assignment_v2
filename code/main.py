#!/usr/bin/env python3

"""
This module contains the main loop for execution the solution to Lunar's Data Engineering Python assignment.
The assignment involves the small-files problem in a space setting.
"""

from code.ingest.gcp_ingestion import data_ingestion
from code.transform.transformation import transform_data
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
    data_ingestion(config.ingestion)

    # Task 2 - Transform data and write merged files
    transform_data(config.transformation)


main()
