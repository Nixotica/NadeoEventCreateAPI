import datetime as dt
import os.path
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

    structure_info = StructureInfo(
        open(os.path.join(os.path.curdir, 'premade_structures/24PlayerSingle_B_1.txt')).read(),
        True
    )

    write_structure(driver, structure_info)

    qualifier_info = QualifierInfo(

    )

    update_qualifier(driver, qualifier_info)
