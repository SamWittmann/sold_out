import traceback
import unittest

import selenium.common.exceptions as exceptions

from script.sold_out import purchase

test_shipping = {
    "name": "Test McTesty",
    "email": "testy@gmail.com",
    "telephone": "1234567890",
    "address": "123 Test St.",  # note that you must ship to billing address
    "zip": "12345",
    "unit" : "",
    "city": "Test",
    "state": "TX"}

test_billing = {
    "cc_num": "1234 5678 1111 0000",  # Don't worry, only your computer gets this info
    "cc_exp_month": "01",  # MM
    "cc_exp_year": "2018",  # YYYY
    "cc_code": "123"
}


class TestPurchasing(unittest.TestCase):
    def test_no_color(self):
        """
        Tests if selecting an item without a color correctly purchases an item.
        :return:
        """
        test_item = {
            "category": "Jackets",  # "Jackets", "Shirts", "Tops/Sweaters", "Sweatshirts". "Pants", "Hats", "Accessories", "Skate
            "name": "Fuck Jacquard Puffy Jacket",  # You should copy-paste this from the item's preview - it must be exact
            "size": "Medium",  # "Small", "Medium", "Large", "XLarge"
            "color": ""
        }
        try:
            purchase(test_item, test_shipping, test_billing, True)
            self.assertTrue(True)
        except exceptions.NoSuchElementException:
            tb = traceback.format_exc()
            print tb
            self.assertTrue(False)

    def test_getting_correct_color(self):
        """
        Tests if selecting an item with a color correctly purchases the specified item.
        :return:
        """
        test_item = {
            "category": "Jackets",  # "Jackets", "Shirts", "Tops/Sweaters", "Sweatshirts". "Pants", "Hats", "Accessories", "Skate
            "name": "Fuck Jacquard Puffy Jacket",  # You should copy-paste this from the item's preview - it must be exact
            "size": "Large",  # "Small", "Medium", "Large", "XLarge"
            "color": "Black"  # If left blank, will choose the default color
        }
        try:
            purchase(test_item, test_shipping, test_billing, True)
            self.assertTrue(True)
        except exceptions.NoSuchElementException:
            tb = traceback.format_exc()
            print tb
            self.assertTrue(False)

    def test_input_correcting(self):
        """
        Tests if purchases can be made with malformed item info
        :return:
        """
        test_item = {
            "category": "Jackets",  # Capitalized category
            "name": "Fuck Jacquard Puffy Jacket",  # Name must be exact
            "size": "large",  # Lowercase size
            "color": "black"  # Lowercase color
        }
        try:
            purchase(test_item, test_shipping, test_billing, True)
            self.assertTrue(True)
        except exceptions.NoSuchElementException:
            tb = traceback.format_exc()
            print tb
            self.assertTrue(False)