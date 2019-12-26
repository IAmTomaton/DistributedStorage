import unittest
from unittest.mock import MagicMock
from distributed_storage.router.orders import Orders
from distributed_storage.router.order import Order


class Test_test_orders(unittest.TestCase):

    def test_send(self):
        orders = Orders()
        customer = MagicMock()
        order = Order("1", customer)

        orders.add_order(order)

        orders.send("s", "1", "123", 1, MagicMock(), MagicMock())

        self.assertTrue(customer.send.called)
        self.assertEqual(0, len(orders._orders))


if __name__ == '__main__':
    unittest.main()
