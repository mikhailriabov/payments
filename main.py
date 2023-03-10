import os
from re import match
import xml.etree.ElementTree as Et
from typing import List
from dataclasses import dataclass
from datetime import datetime

import xml_responses
from weather_prediction.weather_prediction import DummyWeatherModel


PATH = "resources/payments/"


@dataclass
class Card:
    balance: int = 0
    current_day_transactions_count: int = 0


CARD_ELEM_1234567890 = 0
CARD_ELEM_0987654321 = CARD_ELEM_1234567890 + 1
CARD_ELEM_BANK = CARD_ELEM_0987654321 + 1
card_array: List[Card] = []
date_buffer: datetime  # For saving actual data

# Creation of the array of cards that will be used
def init_card_array():
    card_1234567890 = Card(190, 0)
    card_0987654321 = Card(20, 0)
    bank = Card(999800, 0)
    array = (card_1234567890, card_0987654321, bank)
    return array

# The function for getting information by tag
def get_xml_data_by_name(tree: Et.ElementTree, name: str) -> str:
    try:
        text = tree.find(".//" + name).text
    except:
        text = ""
    return text

# Sorting the input files according to the numbers
def key_sort(value: str):
    matching = match(rf"^{PATH}payment_(\d+)\.xml", value)
    if matching:
        return int(matching.group(1))
    else:
        return -1

# The function for checking if the date changed or not
def check_new_date(date: datetime.date):
    global date_buffer, card_array
    if date_buffer != date:
        for elem in card_array:
            elem.current_day_transactions_count = 0
    date_buffer = date


def check_transaction_accept(date_str: str, city: str, money: int, token: str, filename: str):

    # Class of weather modul from external file
    weather_handler = DummyWeatherModel()
    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S,%f%z').date()

    # Check if the date changed
    check_new_date(date)
    weather_info: dict[str, str] = weather_handler.get_weather(date, city)

    # if it's raining decline all the transactions
    if weather_info.get("clouds") == "RAINING":
        xml_responses.declined_ItsRaining(filename)
        return
    else:

        # if it's sunny increase the limit of transactions to 2
        if weather_info.get("clouds") == "SUNNY":
            transaction_limit_count = 2
        else:
            transaction_limit_count = 1

        # if < 10 deg, than the limit for one transaction is 150 / 2 else 150
        if weather_info.get("temperature") < 10:
            transaction_limit_money = 150 / 2
        else:
            transaction_limit_money = 150

        # It's time to know from which card it will be paid. Let's get the index of card_array
        if weather_info.get("wind_direction") == "S" \
                or weather_info.get("wind_direction") == "NS":
            card_elem = CARD_ELEM_BANK
        elif token == "0987654321":
            card_elem = CARD_ELEM_0987654321
        else:
            card_elem = CARD_ELEM_1234567890

        # Now we have all information we need, so we can decide about the transaction

        # Do we have enough money on the account?
        if card_array[card_elem].balance < money:
            xml_responses.declined_InsufficientFunds(filename)
            return

        # Are we in the limit of money per one transaction?
        elif money > transaction_limit_money:
            xml_responses.declined_TransactionAmountOverLimit(filename)
            return

        # Are we in the limit of transactions per day?
        elif card_array[card_elem].current_day_transactions_count + 1 > transaction_limit_count:
            xml_responses.declined_TransactionCountOverLimit(filename)
            return

        # If all previous requirements are false, than we accept the payment
        else:
            if card_elem != CARD_ELEM_BANK:
                card_array[card_elem].current_day_transactions_count += 1
            card_array[card_elem].balance -= money

            xml_responses.accepted_payment(filename)
            return


def main_function():

    global card_array, date_buffer
    card_array = init_card_array()

# Getting the input XML files and their sorting
    filelist = []
    for root, dirs, files in os.walk(PATH):
        for file in files:
            filelist.append(os.path.join(root, file))
    filelist.sort(key=key_sort)

    # Getting the first date
    tree = Et.parse(filelist[0])
    date = get_xml_data_by_name(tree, "Transaction_Time")
    date_buffer = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S,%f%z').date()

    for filename in filelist:
        tree = Et.parse(filename)
        token = get_xml_data_by_name(tree, "Token")

        if len(token) == 0:
            xml_responses.declined(filename)

        else:
            date = get_xml_data_by_name(tree, "Transaction_Time")
            city = get_xml_data_by_name(tree, "Merchant_City")
            money = int(get_xml_data_by_name(tree, "Amount"))
            check_transaction_accept(date, city, money, token, filename)


if __name__ == '__main__':
    main_function()
