import copy
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

    email = os.environ.get('UBI_EMAIL')
    password = os.environ.get('UBI_PASS')

    if email is None or password is None:
        logging.error("Need to set environment variables for UBI_EMAIL and UBI_PASS")
        exit(1)

    login(driver, email, password)

    comp_info = CompetitionBasicInfo(
        name="test_comp",
        club="Project Delta",
        teams=False,
        desc="My test comp"
    )
    write_basic_info(driver, comp_info)

    registration_info = RegistrationInfo(
        start_date=dt.datetime.now(),
        end_date=dt.datetime.now() + dt.timedelta(minutes=5),
        max_players=64
    )

    write_registration(driver, registration_info)

    structure_info = StructureInfo(
        structure_config=open(
            os.path.join(os.path.curdir,
                         'premade_structures/24PlayerSingleElimBinaryBracket/structure.txt')).read(),
        qualifier=True
    )

    write_structure(driver, structure_info)

    qualifier_info = QualifierInfo(
        name="test_qualifier",
        start_date=dt.datetime.now() + dt.timedelta(minutes=5),
        end_date=dt.datetime.now() + dt.timedelta(minutes=15),
        leaderboard_score=LeaderboardScore.TIME,
        max_players=64,
        maps=["JgdwUWRLCujJCCQWzIk9PUqv_hh", "WVer0yh80n1MG_KNDL22QzXZGn8"],
        settings=json.load(open(
            os.path.join(os.path.curdir,
                         'premade_structures/24PlayerSingleElimBinaryBracket/qualifier_settings.json')
        ))
    )

    update_qualifier(driver, qualifier_info)

    round_1_info = RoundInfo(
        name="test_round_1",
        start_date=qualifier_info.end_date + dt.timedelta(minutes=5),
        end_date=qualifier_info.end_date + dt.timedelta(minutes=25),
        leaderboard_type=LeaderboardType.BRACKET,
        script="Cup",
        max_players=64,
        maps=['YI2kowTGtzFHqkPGZFyRG4SUha3'],
        qualifier=qualifier_info,
        settings=json.load(open(
            os.path.join(os.path.curdir,
                         'premade_structures/24PlayerSingleElimBinaryBracket/round_settings.json')
        ))
    )

    round_2_info = copy.copy(round_1_info)
    round_2_info.name = "test_round_2"
    round_2_info.start_date = round_1_info.end_date + dt.timedelta(minutes=5)
    round_2_info.end_date = round_2_info.start_date + dt.timedelta(minutes=20)
    round_2_info.qualifier = None

    round_3_info = copy.copy(round_2_info)
    round_3_info.name = "test_round_3"
    round_3_info.start_date = round_2_info.end_date + dt.timedelta(minutes=5)
    round_3_info.end_date = round_3_info.start_date + dt.timedelta(minutes=20)
    round_3_info.qualifier = None

    update_rounds(driver, [round_1_info, round_2_info, round_3_info])

    create_comp(driver)
