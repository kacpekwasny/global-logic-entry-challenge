from copy import deepcopy
import unittest
import sys, os
import pathlib
TEST_DIR = pathlib.Path(__file__).parent
sys.path.append(str(TEST_DIR / "../src/"))


import logging
from pathlib import Path

CMD_DIR = Path(__file__).parent
LOG_FILE = CMD_DIR / "logs.txt"

lgr = logging.getLogger("global-logic")

# create handlers and set their levels
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create formatters for handlers
c_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(c_format)

# add the handlers to the logger
lgr.addHandler(console_handler)

lgr.debug("Logger successfully created.")
lgr.setLevel(logging.DEBUG)

from warehouse.warehouse import Warehouse


warehouse_content = {
    "items": {
        "1": {
            "stock": [{
                "price": 15.43,
                "in_stock": 22
            },{
                "price": 12.00,
                "in_stock": 12
            },{
                "price": 18.00,
                "in_stock": 30
            }]
        },
        "2": {
            "stock": [{
                "price": 1.43,
                "in_stock": 25
            },{
                "price": 5.43,
                "in_stock": 45
            },{
                "price": 1.30,
                "in_stock": 10
            }]
        }
    }
}

warehouse = Warehouse(config_file_name="warehouse_config_test.json")
warehouse.warehouse = deepcopy(warehouse_content)
warehouse.persist_warehouse()

exit()

class TestWarehouse(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse(config_file_name="warehouse_config_test.json")
        self.warehouse.warehouse = deepcopy(warehouse_content)
        self.warehouse.persist_warehouse()


    def test_get_estimate(self):
        self.assertEqual(-1, self.warehouse.get_estimate("1", 100))
        self.assertEqual(-1, self.warehouse.get_estimate("2", 100))

        self.assertEqual(1023.46, self.warehouse.get_estimate("1", 64))
        self.assertEqual(293.1, self.warehouse.get_estimate("2", 80))

        self.assertEqual(1023.46, self.warehouse.get_estimate("1", 64))
        self.assertEqual(293.1, self.warehouse.get_estimate("2", 80))

        self.assertEqual(435.46, self.warehouse.get_estimate("1", 30))
        self.assertEqual(282.70000000000005, self.warehouse.get_estimate("2", 72))

    def test_buy(self):
        self.assertEqual(-1, self.warehouse.buy("1", 3000))
        
        self.assertEqual(435.46, self.warehouse.buy("1", 30))
        self.assertEqual(282.70000000000005, self.warehouse.buy("2", 72))

        self.assertEqual(self.warehouse.items, {
        "1": {
            "stock": [{
                "price": 12.00,
                "in_stock": 4
            },{
                "price": 18.00,
                "in_stock": 30
            }]
        },
        "2": {
            "stock": [{
                "price": 1.30,
                "in_stock": 8
            }]
        }
    })

    def test_add_product(self):
        self.warehouse.add_product("lime", 10, 12.20)

        self.assertEqual(self.warehouse.items,  {
        "1": {
            "stock": [{
                "price": 15.43,
                "in_stock": 22
            },{
                "price": 12.00,
                "in_stock": 12
            },{
                "price": 18.00,
                "in_stock": 30
            }]
        },
        "2": {
            "stock": [{
                "price": 1.43,
                "in_stock": 25
            },{
                "price": 5.43,
                "in_stock": 45
            },{
                "price": 1.30,
                "in_stock": 10
            }]
        },
        "lime": {
            "stock": [{
                "price": 12.20,
                "in_stock": 10
            }]
        }
    })


if __name__ == '__main__':
    unittest.main()
