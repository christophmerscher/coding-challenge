import io
import time
import unittest
from contextlib import redirect_stdout

from coding_challenge.exceptions.item_not_listed_in_store import ItemNotListedInStore
from coding_challenge.exceptions.item_out_of_stock import ItemOutOfStock
from coding_challenge.item import Item
from coding_challenge.basket import Basket
from coding_challenge.user import User
from coding_challenge.warehouse import Warehouse
from coding_challenge.rules.buy_one_get_one_free_rule import BuyOneGetOneFreeRule
from coding_challenge.rules.percent_discount_rule import PercentDiscountRule


TEN_PERCENT = 0.1
INVALID_ITEM = "XXXXXX"
TEN_MILLION_THOUSAND = 10000000


class TestDiscountRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.warehouse = Warehouse()
        cls.user = User()
        cls.basket = Basket(cls.user, cls.warehouse)

        # Artikel dem Warehouse hinzufügen
        cls.item1 = Item("C0001", 10.0)
        cls.item2 = Item("C0002", 20.0)
        cls.item3 = Item("C0003", 1)

        cls.warehouse.add_item(cls.item1, 10)
        cls.warehouse.add_item(cls.item2, 10)
        cls.warehouse.add_item(cls.item3, 5)

    def test_buy_one_get_one_free_even_quantity(self):
        # Rabattregel hinzufügen
        self.warehouse.add_discount_rule(self.item1.item_id, BuyOneGetOneFreeRule(item=self.item1))

        # Scan items
        self.basket.scan(self.item1.item_id)
        self.basket.scan(self.item1.item_id)
        self.basket.scan(self.item1.item_id)
        self.basket.scan(self.item1.item_id)

        # Berechne preis
        total_price = self.basket.total()
        self.assertEqual(total_price,
                         20.0,
                         "Total price should be 20.0 for Buy One Get One Free rule with even quantity"
                         )
        self.basket.empty()

    def test_buy_one_get_one_free_odd_quantity(self):
        # Rabattregel hinzufügen
        self.warehouse.add_discount_rule(self.item1.item_id, BuyOneGetOneFreeRule(item=self.item1))

        # Scan items
        self.basket.scan(self.item1.item_id)
        self.basket.scan(self.item1.item_id)
        self.basket.scan(self.item1.item_id)

        # Berechne preis
        total_price = self.basket.total()
        self.assertEqual(total_price, 20.0, "Total price should be 20.0 for Buy One Get One Free rule with odd quantity")
        self.basket.empty()

    def test_percent_discount_rule_invalid_discount(self):
        with self.assertRaises(ValueError):
            PercentDiscountRule(self.item2, 1.5)
        with self.assertRaises(ValueError):
            PercentDiscountRule(self.item2, -0.5)
        self.basket.empty()

    def test_percent_discount_rule_valid_discount(self):
        # Rabattregel hinzufügen
        self.warehouse.add_discount_rule(item_id=self.item2.item_id,
                                         discount_rule=PercentDiscountRule(
                                             item=self.item2,
                                             discount=TEN_PERCENT)
                                         )

        # Scan items
        self.basket.scan(self.item2.item_id)
        self.basket.scan(self.item2.item_id)

        # Berechne preis
        total_price = self.basket.total()
        self.assertEqual(total_price, 36.0, "Total price should be 36.0 for 10% discount on two items priced 20.0 each")
        self.basket.empty()

    def test_item_quantity_decrease_in_warehouse(self):
        initial_quantity = self.warehouse.inventory[self.item1.item_id][1]

        # Scan item
        self.basket.scan(self.item1.item_id)

        # Überprüfe ob dem Warehouse auch die richtige menge abgezogen wird
        remaining_quantity = self.warehouse.inventory[self.item1.item_id][1]
        self.assertEqual(remaining_quantity,
                         initial_quantity - 1,
                         "Warehouse quantity should decrease by 1 after scanning item into basket")
        self.basket.empty()

    def test_item_not_listed_in_store(self):
        with self.assertRaises(ItemNotListedInStore):
            self.basket.scan(INVALID_ITEM)
        self.basket.empty()

    def test_item_out_of_stock(self):
        with self.assertRaises(ItemOutOfStock):
            self.basket.scan(item_id=self.item3.item_id, quantity=60)
        self.basket.empty()

    def test_empty_basket(self):
        self.basket.scan(self.item1.item_id)
        self.basket.scan(self.item2.item_id)
        self.basket.empty()
        self.assertTrue(self.basket.is_empty(), "Basket should be empty after calling empty method")
        self.assertEqual(self.warehouse.inventory[self.item1.item_id][1], 10,
                         "Warehouse should have all items returned after emptying basket")
        self.assertEqual(self.warehouse.inventory[self.item2.item_id][1], 10,
                         "Warehouse should have all items returned after emptying basket")

    def test_performance_for_large_number_of_items(self):
        large_basket = Basket(self.user, self.warehouse)
        large_item = Item("LARGE_ITEM", 10.0)
        self.warehouse.add_item(large_item, TEN_MILLION_THOUSAND)

        start_time = time.time()

        with io.StringIO() as buf, redirect_stdout(buf):
            for _ in range(TEN_MILLION_THOUSAND):
                large_basket.scan(large_item.item_id)

        total_price = large_basket.total()
        end_time = time.time()
        duration = end_time - start_time

        self.assertEqual(total_price,
                         10 * TEN_MILLION_THOUSAND,
                         "Total price should be 1,000,000 for 100,000 items priced 10.0 each")
        self.assertLessEqual(duration,
                             120,
                             "Price calculation for 100,000 items should take less than 2 minutes")


if __name__ == '__main__':
    unittest.main()
