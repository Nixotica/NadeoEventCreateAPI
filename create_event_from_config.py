from random import choice
from typing import Tuple

import yaml
import copy
import datetime as dt
import os.path

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from utils.create_competition import *
from utils.forms import *
from utils.map_finder import *


def get_dates(info: dict) -> Tuple[datetime, datetime]:
    if info['Start Date']:
        start_date = dt.datetime.fromtimestamp(info['Start Date'])
    elif info['Start Offset']:
        start_date = dt.datetime.now() + dt.timedelta(minutes=info['Start Offset'])
    else:
        start_date = None
    if info['End Date']:
        end_date = dt.datetime.fromtimestamp(info['End Date'])
    elif info['End Offset']:
        end_date = dt.datetime.now() + dt.timedelta(minutes=info['End Offset'])
    else:
        end_date = None
    return start_date, end_date


def get_maps(info: dict) -> list[str]:
    pool = info['Maps']['Pool']
    random = info['Maps']['Choose Random']
    count = info['Maps']['Choose Count']
    maps = []
    if pool and random and count:
        for i in range(count):
            maps.append(choice(pool))
    elif pool and random and not count:
        maps.append(choice(pool))
    elif pool and not random and count:
        for i in range(count):
            maps.append(pool[i])
    elif pool and not random and not count:
        maps = pool
    elif not pool and random and count:
        for i in range(count):
            maps.append(get_random_map_uid())
    elif not pool and random and not count:
        maps.append(get_random_map_uid())
    elif not pool and not random and count:
        for i in range(count):
            maps.append(get_random_map_uid())
    else:
        maps.append(get_random_map_uid())
    return maps


def create_event(event_config: str):
    with open(f"event_configs/{event_config}", "r") as stream:
        event = yaml.safe_load(stream)
    if event['Browser'] == "Chrome":
        options = ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get("https://admin.trackmania.nadeo.club/create/competition")

    email = os.environ.get('UBI_EMAIL')
    password = os.environ.get('UBI_PASS')

    if email is None or password is None:
        logging.error("Need to set environment variables for UBI_EMAIL and UBI_PASS")
        return

    login(driver, email, password)

    basic_info = event['Basic Info']
    comp_info = CompetitionBasicInfo(
        name=basic_info['Name'],
        club=basic_info['Club'],
        teams=basic_info['Teams'],
        desc=basic_info['Desc'],
        rules=basic_info['Rules']
    )
    write_basic_info(driver, comp_info)

    reg_info = event['Registration Info']
    if reg_info['Registration']:
        start_date, end_date = get_dates(reg_info)
        registration_info = RegistrationInfo(
            start_date=start_date,
            end_date=end_date,
            max_players=reg_info['Max Players']
        )
        write_registration(driver, registration_info)
    else:
        write_registration(driver, None)

    struc_info = event['Structure Info']
    structure_info = StructureInfo(
        structure_config=open(
            os.path.join(os.path.curdir,
                         f'premade_structures/{struc_info["Premade Structure"]}/structure.txt')).read(),
        qualifier=event['Qualifier Info']['Qualifier']
    )

    write_structure(driver, structure_info)

    quali_info = event['Qualifier Info']
    if quali_info['Qualifier']:
        start_date, end_date = get_dates(quali_info)
        qualifier_info = QualifierInfo(
            name=quali_info['Name'],
            start_date=start_date,
            end_date=end_date,
            leaderboard_score=quali_info['Leaderboard Score'],
            max_players=quali_info['Max Players'],
            maps=get_maps(quali_info),
            settings=json.load(open(
                os.path.join(os.path.curdir,
                             f'premade_structures/{struc_info["Premade Structure"]}/{quali_info["Settings"]}')
            ))
        )
        update_qualifier(driver, qualifier_info)
    else:
        update_qualifier(driver, None)

    i = 1
    rounds_info = event['Round Info']
    rounds = []
    while f'Round {i}' in rounds_info:
        round_info = rounds_info[f'Round {i}']
        start_date, end_date = get_dates(round_info)
        if i == 1 and quali_info['Qualifier']:
            qualifier = quali_info['Name']
        else:
            qualifier = None
        round_i_info = RoundInfo(
            name=round_info['Name'],
            start_date=start_date,
            end_date=end_date,
            leaderboard_type=round_info['Leaderboard Type'],
            script=round_info['Script'],
            max_players=round_info['Max Players'],
            maps=get_maps(round_info),
            qualifier=qualifier,
            settings=json.load(open(
                os.path.join(os.path.curdir,
                             f'premade_structures/{struc_info["Premade Structure"]}/{round_info["Settings"]}')
            ))
        )
        rounds.append(round_i_info)
        i += 1

    update_rounds(driver, rounds)

    create_comp(driver)
