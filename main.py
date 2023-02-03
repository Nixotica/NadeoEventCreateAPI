import datetime as dt
import sys

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from utils.create_competition import *
from utils.forms import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    options = ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get("https://admin.trackmania.nadeo.club/create/competition")

    assert(len(sys.argv) == 3)
    email = sys.argv[1]
    password = sys.argv[2]

    login(driver, email, password)

    comp_info = CompetitionBasicInfo(
        "test_comp",
        "Project Delta",
        False,
        "My test comp"
    )
    write_basic_info(driver, comp_info)

    registration_info = RegistrationInfo(
        dt.datetime.now() + dt.timedelta(days=1),
        dt.datetime.now() + dt.timedelta(days=7),
        24
    )

    write_registration(driver, registration_info)
