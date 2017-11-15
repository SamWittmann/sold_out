# coding=utf-8
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from time import sleep

# Add path to the Chrome Driver
# CHROME_DRIVER_PATH = "/path/to/chromedriver"  # Fill in the location of your chromedriver file
CHROME_DRIVER_PATH = "/Users/samwittmann/Documents/sold_out/sold_out/driver/chromedriver"

# Insert shipping info here
SHIPPING_INFO = {
    "name": "INSERT NAME HERE",
    "email": "INSERT EMAIL ADDRESS HERE",
    "telephone": "INSERT PHONE NUMBER HERE", #1234567890
    "address": "INSERT BILLING/SHIPPING STREET ADDRESS HERE",  # note that you must ship to your billing address
    "zip": "INSERT BILLING/SHIPPING ZIP HERE",
    "unit" : "INSERT APARTMENT UNIT",
    "city": "INSERT BILLING/SHIPPING CITY HERE",
    "state": "INSERT BILLING/SHIPPING STATE HERE"  # 2 letter state abbreviate
}

# Insert billing info here
BILLING_INFO = {
    "cc_num": "INSERT CREDIT CARD NUMBER HERE",  # Don't worry, only your computer gets this info
    "cc_exp_month": "INSERT CREDIT CARD EXPIRATION MONTH HERE",  # MM
    "cc_exp_year": "INSERT CREDIT CARD EXPIRATION YEAR HERE",  # YYYY
    "cc_code": "INSERT SECURITY CODE HERE"
}

"""
You should try to find the direct link - reddit.com/r/supremeclothing will probably have a thread with links.

If you don't have a link, try to directly copy-paste the name of the item from supremenewyork.com - it must be exact!
"""
ITEM_INFO = {
    "category": "CHOOSE ONE:",  # "Jackets", "Shirts", "Tops/Sweaters", "Sweatshirts". "Pants", "Hats", "Accessories", "Skate
    "name": "INSERT NAME HERE",  # You should copy-paste this from the item's preview - it must be exact
    "size": "INSERT SIZE HERE",  # "Small", "Medium", "Large", "XLarge"
    "color": "INSERT COLOR HERE",  # If left blank, will choose the default color
    "optional_direct_link": "INSERT LINK HERE"  # If you have a direct link to the item, put it here, otherwise leave blank
}


"""
USERS: MAKE NO EDITS BELOW THIS LINE
"""


class Item:
    def __init__(self, item_dict):
        self.category = item_dict["category"].lower()
        self.name = item_dict["name"]
        self.size = item_dict["size"].title()
        self.color = item_dict["color"].title()
        self.link = item_dict["optional_direct_link"] if "optional_direct_link" in item_dict else None


class Shipping:
    def __init__(self, shipping_dict):
        self.name = shipping_dict["name"]
        self.email = shipping_dict["email"]
        self.phone = shipping_dict["telephone"]
        self.address = shipping_dict["address"]
        self.unit = shipping_dict["unit"]
        self.zip = shipping_dict["zip"]
        self.city = shipping_dict["city"]
        self.state = shipping_dict["state"].upper()


class Payment:
    def __init__(self, billing_dict):
        self.number = billing_dict["cc_num"]
        self.exp_month = billing_dict["cc_exp_month"]
        self.exp_year = billing_dict["cc_exp_year"]
        self.code = billing_dict["cc_code"]


def wait_for_drop():
    """
    Calculates the time until 11:00 AM, then sleeps until 1 second before it
    """
    today = datetime.utcnow()

    # The datetime library represents days of the week as integers - Thursday is 3
    days_until_thursday = (3 - today.weekday()) % 7
    drop_time = today.replace(day=today.day + days_until_thursday, hour=15, minute=59, second=59, microsecond=0)
    delta_t = drop_time - today

    secs = delta_t.seconds

    sleep(secs)


def purchase(item_dictionary, shipping_dictionary, billing_dictionary, test_mode=False):
    """
    Opens a browser, waits until 11AM EST on the next Thursday, and automatically purchases the requested item
    :param item_dictionary: a dictionary containing the information needed to find the desired item
    :param shipping_dictionary: a dictionary containing the information needed to fill out the shipping information
    :param billing_dictionary: a dictionary containing the information needed to fill out the billing information
    :param test_mode: boolean, defaulting to False, which if set to True, will attempt to purchase immediately
    rather than waiting until drop time.
    :return: None
    """
    driver = webdriver.Chrome(executable_path="../driver/chromedriver")
    driver.get("http://www.supremenewyork.com/shop/all")

    item = Item(item_dictionary)

    shipping = Shipping(shipping_dictionary)

    payment = Payment(billing_dictionary)

    # If not testing, wait until drop time
    if not test_mode:
        wait_for_drop()

    find_item(item, driver)
    add_to_cart(item, driver)
    checkout(shipping, payment, driver)


def find_item(item_info, driver):
    """
    Navigates to the page of the desired item, ensuring that it exists
    :param item_info: Item object with the required info
    :param driver: the Selenium driver object
    :return: None
    """
    # if a direct link to the item exists, load that
    if item_info.link:
        driver.get(item_info.link)

    # otherwise, find the item from the store page
    else:
        # go to the category of the desired item
        driver.find_element_by_link_text(item_info.category).click()

        # wait for the page to load, then find the item and click on it
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located(
                    (By.LINK_TEXT, item_info.name)))
            all_colorways = driver.find_elements_by_link_text(item_info.name)

            # If a specific color is requested, find it
            if item_info.color:
                """
                The correct colorway is found by finding all items of the correct color and finding which of the found
                items is in the list of items with the correct name. 
                """
                all_colors = driver.find_elements_by_link_text(item_info.color)
                for colored_item in all_colors:
                    for colorway in all_colorways:
                        if colored_item.get_attribute("href") == colorway.get_attribute("href"):
                            colorway.click()
                return NoSuchElementException

            # If no color is requested, choose the first one
            else:
                all_colorways[0].click()

        except NoSuchElementException:
            print("Item could not be found! Check the item name and try again")
            return NoSuchElementException


def add_to_cart(item_info, driver):
    """
    Attempts to add the item to the cart
    :param item_info: Item object with the required info
    :param driver: the Selenium driver object
    :return: None
    """
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "description")
    ))

    # select the input size from the size menu
    size_select = Select(driver.find_element_by_id("s"))
    size_select.select_by_visible_text(item_info.size)

    # add the item to the cart
    driver.find_element_by_xpath("//*[@id='add-remove-buttons']/input").click()

    # go to checkout
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.LINK_TEXT, "checkout now")
    ))
    # driver.find_element_by_link_text("checkout now")
    driver.get("https://www.supremenewyork.com/checkout")


def checkout(shipping_info, payment_info, driver):
    """
    Checks out your item
    :param shipping_info: Shipping object
    :param payment_info: Payment object
    :param driver: the Selenium driver object
    :return: None
    """
    # Input shipping info
    driver.find_element_by_id("order_billing_name").send_keys(shipping_info.name)
    driver.find_element_by_id("order_email").send_keys(shipping_info.email)
    driver.find_element_by_id("order_tel").send_keys(shipping_info.phone)
    driver.find_element_by_id("bo").send_keys(shipping_info.address)
    driver.find_element_by_id("oba3").send_keys(shipping_info.unit)
    driver.find_element_by_id("order_billing_zip").send_keys(shipping_info.zip)
    driver.find_element_by_id("order_billing_city").send_keys(shipping_info.city)
    Select(driver.find_element_by_id("order_billing_state")).select_by_visible_text(shipping_info.state)

    # Input billing info
    driver.find_element_by_id("nnaerb").send_keys(payment_info.number)
    Select(driver.find_element_by_id("credit_card_month")).select_by_visible_text(payment_info.exp_month)
    Select(driver.find_element_by_id("credit_card_year")).select_by_visible_text(payment_info.exp_year)
    driver.find_element_by_id("orcer").send_keys(payment_info.code)

    # Accept terms
    box = driver.find_element_by_id("order_terms")
    actions = ActionChains(driver)
    actions.move_to_element(box).click().perform()

    # Check out
    driver.find_element_by_name("commit").click()


"""
Runs the script using the info dictionaries at the top of the page.
"""
if __name__ == '__main__':
    purchase(ITEM_INFO, SHIPPING_INFO, BILLING_INFO)