import unittest
import requests

warehouse = {
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

    def test_get_status(self):
        pass


if __name__ == '__main__':
    unittest.main()
