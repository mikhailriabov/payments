import xml.etree.ElementTree as ET
from pathlib import Path


def make_response_file(filename: str, data: str):
    path = Path(filename)

    with Path(f"{path.parent.parent}/response/response_for_{path.name}") as file:
        file.parent.mkdir(mode=0o777, exist_ok=True)
        file.write_bytes(data)


def accepted_payment(filename):
    body = ET.Element('Body')
    transaction_response = ET.SubElement(body, 'TransactionResponse')
    result = ET.SubElement(transaction_response, 'Result')
    reason = ET.SubElement(transaction_response, 'Reason')
    result.text = 'ACCEPTED'
    reason.text = 'None'
    mydata = ET.tostring(body)
    make_response_file(filename, mydata)


def declined_InsufficientFunds(filename):
    body = ET.Element('Body')
    transaction_response = ET.SubElement(body, 'TransactionResponse')
    result = ET.SubElement(transaction_response, 'Result')
    reason = ET.SubElement(transaction_response, 'Reason')
    result.text = 'DECLINED'
    reason.text = 'InsufficientFunds'
    mydata = ET.tostring(body)
    make_response_file(filename, mydata)


def declined_TransactionCountOverLimit(filename):
    body = ET.Element('Body')
    transaction_response = ET.SubElement(body, 'TransactionResponse')
    result = ET.SubElement(transaction_response, 'Result')
    reason = ET.SubElement(transaction_response, 'Reason')
    result.text = 'DECLINED'
    reason.text = 'TransactionCountOverLimit'
    mydata = ET.tostring(body)
    make_response_file(filename, mydata)


def declined_TransactionAmountOverLimit(filename):
    body = ET.Element('Body')
    transaction_response = ET.SubElement(body, 'TransactionResponse')
    result = ET.SubElement(transaction_response, 'Result')
    reason = ET.SubElement(transaction_response, 'Reason')
    result.text = 'DECLINED'
    reason.text = 'TransactionAmountOverLimit'
    mydata = ET.tostring(body)
    make_response_file(filename, mydata)


def declined_ItsRaining(filename):
    body = ET.Element('Body')
    transaction_response = ET.SubElement(body, 'TransactionResponse')
    result = ET.SubElement(transaction_response, 'Result')
    reason = ET.SubElement(transaction_response, 'Reason')
    result.text = 'DECLINED'
    reason.text = 'ItsRaining'
    mydata = ET.tostring(body)
    make_response_file(filename, mydata)


def declined(filename):
    body = ET.Element('Body')
    transaction_response = ET.SubElement(body, 'TransactionResponse')
    result = ET.SubElement(transaction_response, 'Result')
    reason = ET.SubElement(transaction_response, 'Reason')
    result.text = 'DECLINED'
    reason.text = 'None'
    mydata = ET.tostring(body)
    make_response_file(filename, mydata)





