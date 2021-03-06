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

from audioop import add
from json import dumps
from pathlib import Path
import argparse
import sys


##### RELATIVE IMPORT SHOPLIB #####
CMD_DIR = Path(__file__).parent
sys.path.append((CMD_DIR / "..").resolve().__str__())
from shoplib.warehouse import Warehouse  # nopep8

import logging  # nopep8
lgr = logging.getLogger("shoplib")
lgr.handlers[0].level = logging.INFO # console handler is the first one added in shoplib/__init__.py


def make_parser() -> argparse.ArgumentParser:

    ##### ARGPARSE ######
    base_parser = argparse.ArgumentParser(
        description="Buy things from shop and warehouse...")

    place_sp = base_parser.add_subparsers(help="place: chose whether shop or warehouse will be executing commands.",
                                          dest="place")
    place_sp.required = True

    # shop
    shop_p = place_sp.add_parser(
        "shop", help="shop is NOT implemented yet.")

    # warehouse
    warehouse_p = place_sp.add_parser(
        "warehouse", help="choose from one of subcommands to be executed.")

    ##### the same options fof warehouse and shop #####
    ##### status, estimate, buy
    for parser in [shop_p, warehouse_p]:
        action_sp = parser.add_subparsers(
            help="chose command to be executed by the chosen place.", dest="action")
        # I need to access this parser below in order to add a parser to it
        parser.action_subparser = action_sp
        action_sp.required = True

        ##### status #####
        status = action_sp.add_parser(
            "status", help="status of every item in shop")
        status.add_argument("item", nargs="?")

        ##### estimate #####
        estimate = action_sp.add_parser(
            "estimate", help="Status displays every items info.")
        estimate.add_argument("item", nargs=1)
        estimate.add_argument("quantity", nargs=1, type=int)

        ##### buy #####
        buy = action_sp.add_parser(
            "buy", help="Status displays every items info.")
        buy.add_argument("item", nargs=1)
        buy.add_argument("quantity", nargs=1, type=int)

    ##### add item to warehouse #####
    action_sp: argparse._SubParsersAction = warehouse_p.action_subparser
    add_p: argparse.ArgumentParser = action_sp.add_parser(
        "add", help="add item to warehouse")
    add_p.add_argument("-product", type=str, help="the product name")
    add_p.add_argument("-qty", type=int, help="the product quantity")
    add_p.add_argument("-price", type=float, help="the product cost per item")

    return base_parser


def main():
    base_parser = make_parser()
    args = base_parser.parse_args()
    match args.place:
        case "shop":
            print("shop is not implemented, use warehouse")
            exit()

        case "warehouse":
            warehouse = Warehouse()
            lgr.debug(f"{args.action= }")
            match args.action:
                case "status":
                    if args.item:
                        status = warehouse.get_item_status(args.item)
                        if status is None:
                            print("No item with this name was found")
                            return
                    else:
                        status = warehouse.get_status()
                    print(dumps(status, indent=4))
                case "estimate":
                    item = args.item[0]
                    qty = args.quantity[0]
                    cost = warehouse.get_estimate(item, qty)
                    if cost == -1:
                        print(
                            f"There is less than {qty} of the desired item in warehouse.\nUse the `<place> status {item}` command to find out how much there is in warehouse.")
                        return
                    print(cost)
                    print(f"{cost=} of buying {qty} {item}s")
                case "buy":
                    item = args.item[0]
                    qty = args.quantity[0]
                    cost = warehouse.buy(item, qty)
                    if cost == -1:
                        print(
                            f"There is less than {qty} of the desired item in warehouse.\nUse the `<place> status {item}` command to find out how much there is in warehouse.")
                        return
                    print(f"{cost=} of buying  {qty} {item}s")
                case "add":
                    lgr.debug("add item to warehouse")
                    lgr.debug(f"{args.product=} {args.qty=} {args.price=}")
                    warehouse.add_product(args.product, args.qty, args.price)


if __name__ == "__main__":
    main()
