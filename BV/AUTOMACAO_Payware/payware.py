import win32com.client
from selenium_helper import retrieve_cookies, extract_info
from excel_helper import init
import os


def get_credentials():
    user = os.environ["USER"]
    password = os.environ["PASSWORD"]

    return user, password


def start_extraction(table):
    user, password = get_credentials()
    cookies, driver = retrieve_cookies(user, password)

    if cookies and driver:
        result_table = extract_info(driver, table)


def set_table(table):
    print("Table found and set!")

    target_table = init(table)

    if target_table:
        start_extraction(target_table)
    else:
        print("Error while extracting from payware!")


ol = win32com.client.Dispatch("Outlook.Application")
