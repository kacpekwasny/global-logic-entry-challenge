import logging
from pathlib import Path

SHOPLIB_DIR = Path(__file__).parent
LOG_FILE = SHOPLIB_DIR / "logs.txt"

LGR_NAME = "shoplib"
lgr = logging.getLogger(LGR_NAME)
lgr.setLevel(logging.DEBUG) # this seems to be necessary

# create handlers and set their levels
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(str(LOG_FILE.resolve()))
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.WARNING)

# create formatters for handlers
COMMON_FORMAT = "%(levelname)-10s %(filename)-30s :%(lineno)-4s %(funcName)-30s %(message)s"
c_format = logging.Formatter(COMMON_FORMAT)
f_format = logging.Formatter("%(asctime)s "+ COMMON_FORMAT)
console_handler.setFormatter(c_format)
file_handler.setFormatter(f_format)

# add the handlers to the logger
lgr.addHandler(console_handler)
lgr.addHandler(file_handler)

lgr.debug(f"{LGR_NAME=} logger successfully created.")



########################
from .shop import *
from .warehouse import *

