from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .forms import *
import logging

WAIT_TIMEOUT = 10


# "get_web_element_from_xpath"
def gwefxp(driver: WebDriver, xpath: str) -> WebElement:
    return driver.find_element(By.XPATH, xpath)


# "wait_until_visible_element_xpath"
def wuvexp(driver: WebDriver, xpath: str) -> None:
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))


# select from dropdown with waiting and polling
def patient_select(driver: WebDriver, xpath: str, value: str) -> bool:
    wait = WebDriverWait(driver, WAIT_TIMEOUT, ignored_exceptions=NoSuchElementException)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath + '/option[1]')))
    select = Select(driver.find_element(By.XPATH, xpath))
    try:
        select.select_by_visible_text(value)
        return True
    except NoSuchElementException:
        logging.warning(f"Could not find selection '{value}', defaulting to first available.")
        try:
            select.select_by_index(0)
        except NoSuchElementException:
            logging.error(f"Could not make any selections")
            return False


# fill in a datetime field
def input_time(driver: WebDriver, xpath: str, time: datetime):
    date_format = '%m%d%Y'
    time_format = '%I%M%p'

    datetime_input = gwefxp(driver, xpath)

    date_formatted = time.strftime(date_format)
    datetime_input.send_keys(date_formatted)

    datetime_input.send_keys(Keys.TAB)

    time_formatted = time.strftime(time_format)
    datetime_input.send_keys(time_formatted)


def login(driver: WebDriver, email: str, password: str):
    wuvexp(driver, '//*[@id="loginiframe"]')

    iframe = gwefxp(driver, '//*[@id="loginiframe"]')
    driver.switch_to.frame(iframe)

    wuvexp(driver, '//*[@id="AuthEmail"]')
    email_login = gwefxp(driver, '//*[@id="AuthEmail"]')
    email_login.send_keys(email)

    pass_login = gwefxp(driver, '//*[@id="AuthPassword"]')
    pass_login.send_keys(password)

    button_login = gwefxp(driver, '/html/body/app-component/div/app-login-component/main/app-login-shared-component'
                                  '/section/form/button')
    button_login.click()

    driver.switch_to.default_content()


def write_basic_info(driver: WebDriver, info: CompetitionBasicInfo):
    wuvexp(driver, '/html/body/app-root/app-create-competition-component/app-base-component/div/div/div/div/div[1]/h1')

    name_input = gwefxp(driver, '//*[@id="name"]')
    name_input.send_keys(info.name)

    select_success = patient_select(driver, '//*[@id="clubList"]', info.club)
    if not select_success:
        return

    if info.teams:
        teams_input = gwefxp(driver, '//*[@id="isTeam"]')
        teams_input.click()

    if info.desc:
        desc_input = gwefxp(driver, '//*[@id="description"]')
        desc_input.send_keys(info.desc)

    if info.rules:
        rules_input = gwefxp(driver, '//*[@id="rulesUrl"]')
        rules_input.send_keys(info.rules)

    button_next = gwefxp(driver, '/html/body/app-root/app-create-competition-component/app-base-component/div/div/div'
                                 '/div/div[2]/div/button/span[1]')
    button_next.click()


def disable_registration(driver: WebDriver):
    wuvexp(driver, '/html/body/app-root/app-registration-component/app-base-component/div/div/div/div/div[1]/div/h1')

    toggle_button = gwefxp(driver, '//*[@id="toggle"]')
    toggle_button.click()


def write_registration(driver: WebDriver, info: RegistrationInfo):
    wuvexp(driver, '/html/body/app-root/app-registration-component/app-base-component/div/div/div/div/div[1]/div/h1')

    input_time(driver, '//*[@id="startDate"]', info.start_date)
    input_time(driver, '//*[@id="endDate"]', info.end_date)

    max_players_input = gwefxp(driver, '//*[@id="addRegistrationContainer"]/form/div[3]/input')
    max_players_input.clear()
    max_players_input.send_keys(info.max_players)

    if info.zones:
        zones_input = gwefxp(driver, '//*[@id="addRegistrationContainer"]/form/div[4]/input')
        zones_input.send_keys(info.zones)

    button_next = gwefxp(driver, '/html/body/app-root/app-registration-component/app-base-component/div/div/div/div'
                                 '/div[4]/div/button/span[1]')
    button_next.click()


def write_structure(driver: WebDriver, info: StructureInfo):
    wuvexp(driver, '/html/body/app-root/app-create-competition-format-component/app-base-component/div/div/div/div'
                   '/div[1]/div/h1')

    button_import = gwefxp(driver, '/html/body/app-root/app-create-competition-format-component/app-base-component'
                                   '/div/div/div/div/form/div[2]/label')
    button_import.click()

    if info.qualifier:
        toggle_qualifier = gwefxp(driver, '//*[@id="create_qualifier"]')
        toggle_qualifier.click()

    structure_input = gwefxp(driver, '//*[@id="custom_structure_area"]')
    structure_input.send_keys(info.structure_config)

    button_next = gwefxp(driver, '/html/body/app-root/app-create-competition-format-component/app-base-component/div'
                                 '/div/div/div/div[3]/div/button/span[1]')
    button_next.click()


def update_qualifier(driver: WebDriver, info: QualifierInfo):
    wuvexp(driver, '/html/body/app-root/app-create-competition-spotstructure/app-base-component/div/div/div/div/div['
                   '1]/div/h1')

    button_edit = gwefxp(driver, '/html/body/app-root/app-create-competition-spotstructure/app-base-component/div/div'
                                 '/div/div/app-spot-structure-component/div[3]/div[1]/div[2]/button/svg/path')
    button_edit.click()
