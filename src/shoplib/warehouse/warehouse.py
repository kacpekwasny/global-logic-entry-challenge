import sys
from copy import deepcopy
from json import dumps, loads, JSONDecodeError
import logging
import os
import pathlib
from typing import IO


WAREHOUSE_DIR = pathlib.Path(__file__).parent
CONFIG_DIR = WAREHOUSE_DIR / ".." / "config"
lgr = logging.getLogger("shoplib")

class Warehouse:

    def __init__(self, *, config_file_name="warehouse_config.json") -> None:
        # this will change on which database it will be operating
        self.config_file_name: str = config_file_name
        self.config: dict[str, bool | str | float | dict] = {}
        self.warehouse = {}
        self.items: dict[str, dict[str, list[dict]]] = {}

        self.load_config()
        self.load_data()

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
        file_path = WAREHOUSE_DIR / self.config["warehouse_file"]
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip() != "":
                try:
                    self.warehouse = loads(content)
                except JSONDecodeError as e:
                    lgr.error("Failed to load warehouse")
                    lgr.debug(f"{content=}")
                    self.warehouse = {}
            else:
                self.warehouse = {}
            if "items" not  in self.warehouse:
                self.warehouse["items"] = {}
        self.items = self.warehouse["items"]
        return

        error = True


        try:
            pass
            error = False
        except OSError as e:
            lgr.error(f"Failed to open file: {file_path=}")
            lgr.debug(e)
        except Exception as e:
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
            self.open_warehouse_file()
            self.warehouse_file.truncate(0)
            dump = dumps(self.warehouse)
            self.warehouse_file.write(dump)
            self.warehouse_file.close()
            lgr.debug(f"saved to: {self.config['warehouse_file']}")
        except Exception as e:
            lgr.critical("Error while saving the warehouse")
            lgr.debug(dump)
            lgr.debug(e)

    def listen_and_serve(self):
        """
        Listen for http
        """

    def close(self) -> None:
        """
        turn off the HTTP server and close the file
        """
        self.warehouse_file.close()

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
        return deepcopy(self.items.get(item, None))

    def get_estimate(self, item: str, qty: int) -> float:
        """
        returns
            float: price of buying the product in desired quantity
            -1: if there is not enough of the product for the desired quantity
        """
        item_stats = self.items.get(item, None)
        if item_stats is None:
            return -1
        cost = 0
        for v in item_stats["stock"]:
            available = v["in_stock"]
            price = v["price"]
            if qty < available:
                return cost + qty * price

            # qty >= available
            qty -= available
            cost += available * price
                
            if qty == 0:
                return cost
        return -1

    def buy(self, item: str, qty: int) -> float:
        """
        returns:
            float: price of buying the product in the desired quantity
            -1: if there is not enough of the product for the desired quantity (or there is no such product)
        """
        cost = self.get_estimate(item, qty)
        if cost == -1:
            # not enough of the item to buy
            # or the item does not exist
            return -1

        lgr.debug(self.warehouse)

        # enough of the item
        stock = self.items[item]["stock"]
        while qty > 0:
            available = stock[0]["in_stock"]
            if qty < available:
                stock[0]["in_stock"] -= qty
                break
            if qty >= available:
                qty -= available
                stock.pop(0)
            if qty == 0:
                break

        lgr.debug(self.warehouse)

        self.persist_warehouse()
        return cost

    def add_product(self, item: str, qty: int, price: float) -> None:
        """
        add product to warehouse
        """
        d = {
            "in_stock": qty,
            "price": price
        }
        if item in self.items:
            self.items[item]["stock"].append(d)
        else:
            self.items[item] = {
                "stock": [d]
            }
        self.persist_warehouse()
