"""
cli.py
    warehouse status            # status of all items
    warehouse status <ITEM>     # status of the selected <ITEM>

    shop status                 # status of all items
    shop status <ITEM>          # status of the selected <ITEM>

    help, h, -h, -help, --help, ? # display this guide

    config
            -s <shop address with port>         # this will change the whole projects config to run the 
            -w <warehouse address with port>




cli.py      # run with no arguments
            # You will be prompted to the cli and from there you will be able to 
cli >
"""

import logging

main_logger = logging.getLogger()
main_logger.setLevel(logging_level)

# Set up a stream handler to log to the consolestream_handler = logging.StreamHandler()
stream_handler.setLevel(logging_level)
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)