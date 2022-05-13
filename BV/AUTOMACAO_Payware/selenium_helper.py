from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from config import payware_login_url, payware_search_url
import time


def login(user, password):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(payware_login_url)

    input_login = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/form/input[2]")
    input_pass = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/form/input[3]")
    btn_login = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div/form/div[1]/table/tbody/tr/td[1]/button")

    input_login.send_keys(user)
    input_pass.send_keys(password)
    btn_login.click()

    time.sleep(3)

    if driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[1]/ul/li[5]/a"):
        return True, driver
    else:
        return False


def retrieve_cookies(user, password):
    is_logged_in, driver = login(user, password)

    if is_logged_in:
        cookies = driver.get_cookies()

        return cookies, driver
    return None


def populate_table(pontuacao, item, table):
    table.loc[table["Conta"] == item, "Pontuação"] = pontuacao


def extract_item(driver, item):

    # Clica no botão de pesquisar
    driver.find_element_by_xpath("/html/body/div[5]/div[2]/span/a[1]").click()

    time.sleep(1)

    # Extrai pontuação
    pontuacao = driver.find_element_by_xpath(
        "/html/body/table/tbody/tr/td/div/table[2]/tbody/tr[9]/td/table/tbody/tr[4]/td[4]/input").get_attribute("value")

    # seleciona emissor
    select = Select(driver.find_element_by_xpath(
        '/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[1]/td[2]/div/div[2]/select'))
    select.select_by_index(1)

    # seleciona produto
    select = Select(driver.find_element_by_xpath(
        '/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td[2]/div/div[2]/select'))
    select.select_by_visible_text('6 - MC PARCERIA')

    # clica dentro e depois fora do select para atualizar
    driver.find_element_by_xpath(
        '/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td[2]/div').click()
    driver.find_element_by_xpath(
        '/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td[2]/div').click()

    input_account_number = driver.find_element_by_xpath(
        "/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[4]/td[2]/input")

    input_account_number.send_keys(item)

    # Clica no botão de pesquisar
    driver.find_element_by_xpath(
        "/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[5]/td/button").click()

    return pontuacao


def extract_info(driver: webdriver.Chrome, table):
    driver.get(payware_search_url)

    work_items = list(table["Conta"])

    time.sleep(3)

    # seleciona emissor
    select = Select(driver.find_element_by_xpath(
        '/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[1]/td[2]/div/div[2]/select'))
    select.select_by_index(1)

    # seleciona produto
    select = Select(driver.find_element_by_xpath(
        '/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td[2]/div/div[2]/select'))
    select.select_by_visible_text('6 - MC PARCERIA')

    # clica dentro e depois fora do select para atualizar
    driver.find_element_by_xpath(
        '/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td[2]/div').click()
    driver.find_element_by_xpath(
        '/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[3]/td[2]/div').click()

    input_account_number = driver.find_element_by_xpath(
        "/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[4]/td[2]/input")

    input_account_number.send_keys(work_items.pop())

    # Clica no botão de pesquisar
    driver.find_element_by_xpath(
        "/html/body/div[6]/div/div/div[2]/div[2]/form/div/div/div[2]/table/tbody/tr/td/div/div/div[2]/table/tbody/tr[5]/td/button").click()

    pontuacao = driver.find_element_by_xpath(
        "/html/body/table/tbody/tr/td/div/table[2]/tbody/tr[9]/td/table/tbody/tr[4]/td[4]/input").get_attribute("value")

    for item in work_items():
        pontuacao = extract_item(driver, item)
        populate_table(pontuacao, item, table)
