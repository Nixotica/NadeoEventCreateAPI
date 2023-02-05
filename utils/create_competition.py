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

WAIT_TIMEOUT = 20


# "get_web_element_from_xpath"
def gwefxp(driver: WebDriver, xpath: str) -> WebElement:
    return driver.find_element(By.XPATH, xpath)


# "wait_until_visible_element_xpath"
def wuvexp(driver: WebDriver, xpath: str) -> None:
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))


# select from dropdown with waiting and polling
def patient_select(driver: WebDriver, xpath: str, value) -> bool:
    wait = WebDriverWait(driver, WAIT_TIMEOUT, ignored_exceptions=NoSuchElementException)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath + '/option[1]')))
    select = Select(driver.find_element(By.XPATH, xpath))
    try:
        if isinstance(value, str):
            select.select_by_visible_text(value)
        else:
            select.select_by_index(value)
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


def add_maps(driver: WebDriver, maps: list[str]):
    for map in maps:
        wuvexp(driver, '//*[@id="buttonAddMap"]')
        button_add_maps = gwefxp(driver, '//*[@id="buttonAddMap"]')
        button_add_maps.click()

        wuvexp(driver, '//*[@id="browserMaps"]/div[2]/div[2]/div/div[1]')
        button_uid = gwefxp(driver, '//*[@id="btnManualUid"]')
        button_uid.click()

        wuvexp(driver, '//*[@id="map"]')
        uid_input = gwefxp(driver, '//*[@id="map"]')
        uid_input.send_keys(map)

        button_add = gwefxp(driver, '//*[@id="browserMaps"]/div[2]/div['
                                    '2]/div/app-map-form-component/div/form/div/button[2]')
        button_add.click()


def fill_in_setting(driver: WebDriver, setting: dict):
    wuvexp(driver, '//*[@id="name"]')
    name_input_q1 = gwefxp(driver, '/html/body/app-root/app-qualification-component/app-base-component/div/div/div/div'
                                '/form/app-config-form-component/form/div[6]/div/app-settings-component/form/div['
                                '1]/div/input')
    name_input_q2 = gwefxp(driver, '/html/body/app-root/app-qualification-component/app-base-component/div/div/div/div'
                                '/form/app-config-form-component/form/div[9]/div/app-settings-component/form/div['
                                '1]/div/input')
    name_input_r1 = gwefxp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div/div/div/div'
                                   '/form/app-config-form-component/form/div[7]/div/app-settings-component/form/div['
                                   '1]/div/input')
    name_input_r2 = gwefxp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div/div/div/div'
                                   '/form/app-config-form-component/form/div[10]/div/app-settings-component/form/div['
                                   '1]/div/input')

    name_input.send_keys(setting['Setting'])

    patient_select(driver, '//*[@id="type"]', setting['Type'])

    value_input = gwefxp(driver, '//*[@id="value"]')
    value_input.send_keys(setting['Value'])


def add_settings(driver: WebDriver, settings: json, qualifier: bool):
    for script_setting in settings['script_settings']:
        button_add_settings = gwefxp(driver, '//*[@id="buttonAddScriptSettings"]')
        button_add_settings.click()

        if qualifier:
            wuvexp(driver, '/html/body/app-root/app-qualification-component/app-base-component/div/div/div/div/form/app'
                           '-config-form-component/form/div[6]/div/app-settings-component/form/div[1]/div/input')
            name_input = gwefxp(driver, '/html/body/app-root/app-qualification-component/app-base-component/div/div'
                                        '/div/div/form/app-config-form-component/form/div['
                                        '6]/div/app-settings-component/form/div[1]/div/input')
        else:
            wuvexp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div/div/div/div/form/app'
                           '-config-form-component/form/div[7]/div/app-settings-component/form/div[1]/div/input')
            name_input = gwefxp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div/div/div'
                                        '/div/form/app-config-form-component/form/div['
                                        '7]/div/app-settings-component/form/div[1]/div/input')
        name_input.send_keys(script_setting['Setting'])

        patient_select(driver, '//*[@id="type"]', script_setting['Type'])

        if script_setting['Type'] == 'boolean':
            patient_select(driver, '//*[@id="selectBool"]', script_setting['Value'])
        else:
            value_input = gwefxp(driver, '//*[@id="value"]')
            value_input.send_keys(script_setting['Value'])

        if qualifier:
            button_add_confirm = gwefxp(driver, '/html/body/app-root/app-qualification-component/app-base-component/div'
                                                '/div/div/div/form/app-config-form-component/form/div['
                                                '6]/div/app-settings-component/form/div[4]/button[2]')
        else:
            button_add_confirm = gwefxp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div/div'
                                                '/div/div/form/app-config-form-component/form/div['
                                                '7]/div/app-settings-component/form/div[4]/button[2]')
        button_add_confirm.click()

    for plugin_setting in settings['plugin_settings']:
        button_add_settings = gwefxp(driver, '//*[@id="buttonAddPluginSettings"]')
        button_add_settings.click()

        if qualifier:
            wuvexp(driver, '/html/body/app-root/app-qualification-component/app-base-component/div/div/div/div/form'
                           '/app-config-form-component/form/div[9]/div/app-settings-component/form/div[1]/div/input')
            name_input = gwefxp(driver, '/html/body/app-root/app-qualification-component/app-base-component/div/div'
                                        '/div/div/form/app-config-form-component/form/div['
                                        '9]/div/app-settings-component/form/div[1]/div/input')
        else:
            wuvexp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div/div/div/div/form/app'
                           '-config-form-component/form/div[10]/div/app-settings-component/form/div[1]/div/input')
            name_input = gwefxp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div/div/div'
                                        '/div/form/app-config-form-component/form/div['
                                        '10]/div/app-settings-component/form/div[1]/div/input')
        name_input.send_keys(plugin_setting['Setting'])

        patient_select(driver, '//*[@id="type"]', plugin_setting['Type'])

        if plugin_setting['Type'] == 'boolean':
            patient_select(driver, '//*[@id="selectBool"]', plugin_setting['Value'])
        else:
            value_input = gwefxp(driver, '//*[@id="value"]')
            value_input.send_keys(plugin_setting['Value'])

        if qualifier:
            button_add_confirm = gwefxp(driver, '/html/body/app-root/app-qualification-component/app-base-component/div'
                                                '/div/div/div/form/app-config-form-component/form/div['
                                                '9]/div/app-settings-component/form/div[4]/button[2]')
        else:
            button_add_confirm = gwefxp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div'
                                                '/div/div/div/form/app-config-form-component/form/div['
                                                '10]/div/app-settings-component/form/div[4]/button[2]')
        button_add_confirm.click()


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
        info.desc += "\n\nThis event was generated using the Trackmania Event Creation tool. " \
                     "https://github.com/Nixotica/NadeoEventCreateAPI "
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
    wuvexp(driver, '/html/body/app-root/app-create-competition-spotstructure/app-base-component/div/div/div/div/app'
                   '-spot-structure-component/div[3]/div[1]/div[2]/button')

    button_edit = gwefxp(driver,
                         '/html/body/app-root/app-create-competition-spotstructure/app-base-component/div/div/div/div'
                         '/app-spot-structure-component/div[3]/div[1]/div[2]/button')
    button_edit.click()

    wuvexp(driver, '/html/body/app-root/app-qualification-component/app-base-component/div/div/div/div/div[1]/h1')

    if info.name:
        name_input = gwefxp(driver, '//*[@id="qualificationName"]')
        name_input.clear()
        name_input.send_keys(info.name)

    input_time(driver, '//*[@id="qualificationStartDate"]', info.start_date)
    input_time(driver, '//*[@id="qualificationEndDate"]', info.end_date)

    patient_select(driver, '//*[@id="leaderboardScore"]', int(info.leaderboard_score))

    max_players_input = gwefxp(driver, '//*[@id="max_players"]')
    max_players_input.clear()
    max_players_input.send_keys(info.max_players)

    add_maps(driver, info.maps)

    add_settings(driver, info.settings, True)

    button_final_edit = gwefxp(driver, '//*[@id="editQualification"]/span')
    button_final_edit.click()


def update_rounds(driver: WebDriver, info: list[RoundInfo]):
    round_num: int = 1
    for round_info in info:
        alert: bool = len(driver.find_elements(By.XPATH, '//*[@id="alert-dates-2"]/p')) > 0
        if alert:
            wuvexp(driver, f'/html/body/app-root/app-create-competition-spotstructure/app-base-component/div/div/div/div/app'
                           f'-spot-structure-component/div[3]/div[{1+round_num}]/div[3]/button[2]')
            button_edit = gwefxp(driver, f'/html/body/app-root/app-create-competition-spotstructure/app-base-component'
                                         f'/div/div/div/div/app-spot-structure-component/div[3]/div[{1+round_num}]/div['
                                         f'3]/button[2]')
        else:
            wuvexp(driver, f'/html/body/app-root/app-create-competition-spotstructure/app-base-component/div/div/div/div/app'
                           f'-spot-structure-component/div[3]/div[{1+round_num}]/div[2]/button[2]')
            button_edit = gwefxp(driver, f'/html/body/app-root/app-create-competition-spotstructure/app-base-component'
                                         f'/div/div/div/div/app-spot-structure-component/div[3]/div[{1+round_num}]/div['
                                         f'2]/button[2]')
        button_edit.click()

        wuvexp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div/div/div/div/div[1]/h1')

        name_input = gwefxp(driver, '//*[@id="name"]')
        name_input.clear()
        name_input.send_keys(round_info.name)

        input_time(driver, '//*[@id="roundStartDate"]', round_info.start_date)
        input_time(driver, '//*[@id="roundEndDate"]', round_info.end_date)

        if round_info.qualifier:
            patient_select(driver, '//*[@id="qualifier"]', round_info.qualifier.name)

        patient_select(driver, '//*[@id="leaderboardType"]', int(round_info.leaderboard_type))

        patient_select(
            driver,
            '/html/body/app-root/app-new-round-component/app-base-component/div/div/div/div/form/app-config-form'
            '-component/form/div[1]/select ',
            round_info.script
        )

        max_players_input = gwefxp(driver, '//*[@id="max_players"]')
        max_players_input.clear()
        max_players_input.send_keys(round_info.max_players)

        if round_info.max_spectators:
            max_spec_input = gwefxp(driver, '//*[@id="max_spectators"]')
            max_spec_input.clear()
            max_spec_input.send_keys(round_info.max_spectators)

        add_maps(driver, round_info.maps)

        add_settings(driver, round_info.settings, False)

        button_final_edit = gwefxp(driver, '/html/body/app-root/app-new-round-component/app-base-component/div/div'
                                           '/div/div/form/div[6]/div/button[2]/span')
        button_final_edit.click()

        round_num += 1

    wuvexp(driver, '/html/body/app-root/app-create-competition-spotstructure/app-base-component/div/div/div/div/div['
                   '2]/button')

    button_create = gwefxp(driver, '/html/body/app-root/app-create-competition-spotstructure/app-base-component/div'
                                   '/div/div/div/div[2]/button')
    button_create.click()


def create_comp(driver: WebDriver):
    wuvexp(driver, '//*[@id="dialog"]/div/div[2]/button[2]')
    button_create = gwefxp(driver, '//*[@id="dialog"]/div/div[2]/button[2]')
    button_create.click()