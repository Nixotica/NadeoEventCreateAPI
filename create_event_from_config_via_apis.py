import datetime
import json
import os

import requests
import yaml

from utils.api_helpers import *


def authenticate():
    url = "https://public-ubiservices.ubi.com/v3/profiles/sessions"
    headers = {
        "Content-Type": "application/json",
        "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
        "Authorization": os.environ["AUTHORIZATION"],
        "User-Agent": "My app / nixotica@gmail.com",
    }
    result = requests.post(url, headers=headers).json()

    url = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/ubiservices"
    ticket = result["ticket"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"ubi_v1 t={ticket}"
    }
    body = {
        "audience": "NadeoClubServices"
    }
    result = requests.post(url, headers=headers, json=body)
    return result.json()["accessToken"]


def refresh_token(refresh_token):
    url = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/refresh"
    headers = {'Authorization': 'nadeo_v1 t=' + refresh_token}
    result = requests.post(url, headers=headers)
    return result.json()


def construct_payload(event: yaml):
    payload: dict = {}

    payload["clubId"] = get_club_id()
    payload["description"] = event["Basic Info"]["Desc"]
    payload["name"] = event["Basic Info"]["Name"]
    payload["registrationEndDate"] = datetime.datetime.now() + datetime.timedelta(minutes=int(event["Registration Info"]["End Offset"]))
    payload["registrationStartDate"] = datetime.datetime.now() + datetime.timedelta(minutes=int(event["Registration Info"]["Start Offset"]))

    rounds = []
    round_num = 1
    while f"Round {round_num}" in event["Round Info"]:
        round: dict = {}

        round_num += 1

    # TODO do this if worth the effort
    return payload


def create_event(event_config: str):
    # with open(os.path.join(os.path.curdir, f'event_configs/{event_config}')) as stream:
    #     event = yaml.safe_load(stream)
    #
    # construct_payload(event)

    token = authenticate()
    create_comp_url = "https://competition.trackmania.nadeo.club/api/competitions/web/create"
    payload = json.load()
    response = requests.post(url=create_comp_url, headers={'Authorization': 'nadeo_v1 t=' + token}, json=payload)
    print(response.text)
    print(response.content)
