from copy import deepcopy
from email.policy import default
from json import dumps, loads, JSONDecodeError
import logging
import os
import pathlib
from typing import IO


WAREHOUSE_DIR = pathlib.Path(__file__).parent
CONFIG_DIR = WAREHOUSE_DIR / ".." / "config"
lgr = logging.getLogger(__name__)

class Warehouse:

    def __init__(self, *, config_file_name="warehouse_config.json") -> None:
        self.config_file_name: str = config_file_name    # this will change on which database it will be operating
        self.config: dict[str, bool | str | float | dict] = {}
        self.warehouse = {}
        self.items: dict[str, dict[str, list[dict]]] = {}

        self.load_config()
        self.load_data()

        self.warehouse_file: IO

    def load_config(self):
        """load config from src/config/{config_file}.json, parse it and set to self.config"""
        file_path = (CONFIG_DIR / self.config_file_name).resolve()
        error = True
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.config = loads(f.read())
            error = False
        except OSError as e:
            lgr.error(f"Failed to open file: {file_path=}")
            lgr.debug(e)
        except JSONDecodeError as e:
            lgr.error("Failed to load config")
            lgr.debug(e)
        except e:
            lgr.critical("Unknown error")
            lgr.debug(e)
        finally:
            if error:
                exit()

    def load_data(self):
        file_path = WAREHOUSE_DIR / self.config["warehouse.json"]
        error = True
        try:
            with open(file_path, "rw", encoding="utf-8") as f:
                self.warehouse = loads(f.read())
            self.items = self.warehouse["items"]
            error = False
        except OSError as e:
            lgr.error(f"Failed to open file: {file_path=}")
            lgr.debug(e)
        except JSONDecodeError as e:
            lgr.error("Failed to load warehouse")
            lgr.debug(e)
        except e:
            lgr.critical("Unknown error")
            lgr.debug(e)
        finally:
            if error:
                exit()

    def open_warehouse_file(self):
        file_path = (WAREHOUSE_DIR / self.config["warehouse_file"]).resolve()
        error = True
        try:
            self.warehouse_file = open(file_path, "w", encoding="utf-8")
            error = False
        except OSError as e:
            lgr.error(f"Failed to open file: {file_path=}")
            lgr.debug(e)
        except e:
            lgr.critical(f"Failed to open file for writing: {file_path=}")
            lgr.debug(e)
        finally:
            if error:
                exit()

    def persist_warehouse(self):
        try:
            self.warehouse_file.truncate(0)
            self.warehouse_file.write(dumps(self.warehouse))
            self.warehouse_file.flush()
            os.fsync(self.warehouse_file.fileno())
        except e:
            lgr.critical("Error while saving the warehouse")
            lgr.debug(e)

    def close(self) -> None:
        """
        turn off the HTTP server and close the file
        """
        self.warehouse_file.close()

    def listen_and_serve(self):
        """
        Listen for http
        """

    # ~~~~~~~~~ API ~~~~~~~~~ #
    def get_status(self) -> dict:
        """
        return the dict warehouse items
        """
        return self.items

    def get_item_status(self, item: str) -> dict | None:
        """
        returns:
            dict if item was found in self.items
            None if no such item was found
        """
        lgr.debug(f"Get status of {item=}")
        return deepcopy(self.items.get(item, default=None))

    def get_estimate(self, item: str, qty: int) -> float:
        """
        returns
            float: price of buying the product in desired quantity
            -1: if there is not enough of the product for the desired quantity
        """
        item_stats = self.items.get(item, default=None)
        if item is None:
            return -1
        price = 0
        for v in item_stats["stock"].values():
            available = v["in_stock"]
            price = v["price"]
            if qty > available:
                qty -= available
                price += available * price
            if qty < available:
                return qty * price
            if qty == 0:
                return price
        return -1

    def buy(self, item: str, qty: int) -> float:
        """
        returns:
            float: price of buying the product in the desired quantity
            -1: if there is not enough of the product for the desired quantity
        """
        price = self.get_estimate(item, qty)
        if price == -1:
            # not enough of the item to buy
            return -1
        
        # enough of the item
        stock = self.items[item]["stock"]
        while qty > 0:
            available = stock[0]["in_stock"]
            price = stock[0]["price"]
            if qty >= available:
                qty -= available
                price += available * price
                stock.pop(0)
            if qty < available:
                stock[0]["in_stock"] -= qty
                return qty * price
            if qty == 0:
                return price

        self.persist_warehouse()

    def add_product(self, item: str, qty: int, price: float) -> None:
        """
        add product to warehouse
        """
        self.items[item]["stock"].append({
            "in_stock": qty,
            "price": price
        })
        self.persist_warehouse()

