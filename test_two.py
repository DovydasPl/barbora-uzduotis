import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os


load_dotenv()


SELECTORS = {
    'login_button': {
        'selector': 'fti-header-login',
        'by': By.ID
    },
    'email_input': {
        'selector': 'email',
        'by': By.NAME
    },
    'password_input': {
        'selector': 'password',
        'by': By.ID
    },
    'login_submit_button': {
        'selector': 'fti-login-email',
        'by': By.ID
    },
    'login_error': {
        'selector': '#login-tab-0 > div > div > div > form > div.b-alert.b-alert--error',
        'by': By.CSS_SELECTOR
    },
    'customer_menu': {
        'selector': 'fti-header-customer-menu',
        'by': By.ID
    }
}


def get_element(driver, element):
    return WebDriverWait(driver, 20).until(EC.presence_of_element_located((element['by'], element['selector'])))


@pytest.fixture(scope='function')
def driver():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()


def test_login_success(driver):
    driver.get('https://www.barbora.lt/')

    get_element(driver, SELECTORS['login_button']).click()
    get_element(driver, SELECTORS['email_input']).send_keys(os.getenv('ACCOUNT_EMAIL'))
    get_element(driver, SELECTORS['password_input']).send_keys(os.getenv('ACCOUNT_PASSWORD'))
    get_element(driver, SELECTORS['login_submit_button']).click()

    assert get_element(driver, SELECTORS['customer_menu']).is_displayed()


def test_login_fail(driver):
    driver.get('https://www.barbora.lt/')

    get_element(driver, SELECTORS['login_button']).click()
    get_element(driver, SELECTORS['email_input']).send_keys('testinis.elpastas@kuris.neegzistuoja')
    get_element(driver, SELECTORS['password_input']).send_keys('testinisslaptazodis')
    get_element(driver, SELECTORS['login_submit_button']).click()

    login_error = get_element(driver, SELECTORS['login_error'])

    assert login_error.is_displayed()
    assert login_error.text == 'Neteisingas el. pašto adresas arba slaptažodis'
