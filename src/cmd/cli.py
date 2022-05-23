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
"""

##### LOGGING #####
import logging
lgr = logging.getLogger("shoplib")


##### RELATIVE IMPORT SHOPLIB #####
import sys
from pathlib import Path
CMD_DIR = Path(__file__).parent
sys.path.append((CMD_DIR / "..").resolve().__str__())
from shoplib.warehouse import Warehouse



def main():
    ##### ARGPARSE ######
    import argparse
    parser = argparse.ArgumentParser(description="Buy things from shop and warehouse...")
    subparser = parser.add_subparsers(help="chose wether shop or warehouse will be executing commands")

    subparser.add_parser("shop", help="shop is NOT implemented yet.")
    warehouse_parser = subparser.add_parser("warehouse", help="choose from one of subcommands to be executed.")

    warehouse_parser.add_argument("status", type=str, help="Status displays every items info.")

    args = parser.parse_args(sys.argv[1:])
    print(dir(args))





if __name__ == "__main__":
    main()
