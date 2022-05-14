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
from pathlib import Path

CMD_DIR = Path(__file__).parent
LOG_FILE = CMD_DIR / "logs.txt"

lgr = logging.getLogger("global-logic")

# create handlers and set their levels
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(str(LOG_FILE.resolve()))
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)

# create formatters for handlers
c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
f_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(c_format)
file_handler.setFormatter(f_format)

# add the handlers to the logger
lgr.addHandler(console_handler)
lgr.addHandler(file_handler)

lgr.debug("Logger successfully created.")



def main():
    pass


if __name__ == "__main__":
    main()
