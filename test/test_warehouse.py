from copy import deepcopy
import unittest
import sys
import pathlib
TEST_DIR = pathlib.Path(__file__).parent
sys.path.append(str(TEST_DIR / "../src/"))
from shoplib.warehouse import Warehouse


import logging
lgr = logging.getLogger("shoplib")



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


class TestWarehouse(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse(config_file_name="warehouse_config_test.json")
        self.warehouse.warehouse = deepcopy(warehouse_content)
        self.warehouse.items = self.warehouse.warehouse["items"]
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
            }, {
                "price": 12.20,
                "in_stock": 10
            }]
        }
    })


if __name__ == '__main__':
    unittest.main()
