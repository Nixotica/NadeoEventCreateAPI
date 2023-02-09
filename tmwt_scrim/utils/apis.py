import datetime
import json
import os.path

import requests
from pastebin import PastebinAPI
from tmwt_scrim.utils.types import TeamInfo, PastebinInfo, ScrimInfo


def authenticate(service: str, auth: str) -> str:
    """
    Authenticates with Nadeo Club Services and returns an access token.
    :service: Audience (e.g. "NadeoClubServices", "NadeoLiveServices")
    :auth: Authorization (e.g. "Basic <user:pass base 64>")
    :return: Authorization token
    """
    url = "https://public-ubiservices.ubi.com/v3/profiles/sessions"
    headers = {
        "Content-Type": "application/json",
        "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
        "Authorization": auth,
        "User-Agent": "https://github.com/Nixotica/NadeoEventCreateAPI",
    }
    result = requests.post(url, headers=headers).json()

    url = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/ubiservices"
    ticket = result["ticket"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"ubi_v1 t={ticket}"
    }
    body = {
        "audience": service
    }
    result = requests.post(url, headers=headers, json=body)
    return result.json()["accessToken"]


def refresh_token(token):
    """
    Refreshes the old access token and returns a new one.
    :param token: 
    :return: 
    """
    url = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/refresh"
    headers = {'Authorization': 'nadeo_v1 t=' + token}
    result = requests.post(url, headers=headers)
    return result.json()["accessToken"]


def get_maps_from_campaign(club_id: int, campaign_id: int, token: str) -> list[str]:
    """
    Provided a club and campaign id,
    :param club_id:
    :param campaign_id:
    :param token: Token for audience "NadeoLiveServices"
    :return:
    """

    # TODO actually implement this, for now just return TMWT E Winter 2023 Campaign Maps
    return [
          "Wa0FxXSM363CCYEh3uTwjxOTcLi",
          "4VxmHRGL5aQ9Ap_WAZicwKb1ohb",
          "uOS8IXicSoHX_oo3rcpl81pwEAj",
          "YI2kowTGtzFHqkPGZFyRG4SUha3",
          "ZV2aWMY9SRgGkXR_ol8aiw7n37l",
          "w6yZQCKiSkqWDLZNErw49qtbeG6",
          "N7TWhYUiecAXf7wx_naPzpkaaUd",
          "D6JgQlTA1Zm6ukVmdk_WECLW4Ki",
          "FgFXuAsWiZr7M9RUwWduKplLcf5",
          "lgbphUU9UpJZSoKc8dTD3EjPmtj"
    ]


def get_team_pair_pastebin_url(team_1: TeamInfo, team_2: TeamInfo, pastebin_info: PastebinInfo) -> str:
    """
    Provided two teams and pastebin info, retrieve a pastebin url for the payload creating a match.
    Creates a new paste and caches locally in tmwt_scrim/utils/team_pastebin_pairs.json if does not exist.
    :param team_1:
    :param team_2:
    :param pastebin_info:
    :return: Pastebin URL
    """
    cache = json.load(open(os.path.join(os.path.curdir, "tmwt_scrim/utils/team_pastebin_pairs.json")))
    for team in cache:
        if team_1.id in team["Team_Ids"] and team_2.id in team["Team_Ids"]:
            return team["S_TeamsUrl"]

    paste = json.load(open(os.path.join(os.path.curdir, "tmwt_scrim/utils/payloads/TeamsPastebin")))

    paste[0]["Id"] = team_1.id
    paste[0]["Name"] = team_1.id
    paste[0]["Players"][0]["AccountId"] = team_1.account_id_1
    paste[0]["Players"][1]["AccountId"] = team_1.account_id_2

    paste[1]["Id"] = team_2.id
    paste[1]["Name"] = team_2.id
    paste[1]["Players"][0]["AccountId"] = team_2.account_id_1
    paste[1]["Players"][1]["AccountId"] = team_2.account_id_2

    key = PastebinAPI.generate_user_key(
        api_dev_key=pastebin_info.api_dev_key,
        username=pastebin_info.username,
        password=pastebin_info.password)

    pastebin_url = PastebinAPI.paste(
        api_dev_key=pastebin_info.api_dev_key,
        api_paste_code=json.dumps(paste),
        api_user_key=key)

    cache.append({
        "Team_Ids": [
            team_1.id,
            team_2.id
        ],
        "S_TeamsUrl": pastebin_url
    })

    return pastebin_url


def create_base_scrim(token: str, info: ScrimInfo):
    create_payload = json.load(open(os.path.join(os.path.curdir, "tmwt_scrim/utils/payloads/CreateScrim.json")))

    create_payload["clubId"] = info.my_club_id
    create_payload["name"] = info.name

    date_format = "%Y-%m-%dT%H:%M:%S.000Z"
    create_payload["rounds"][0]["startDate"] = datetime.datetime.strftime(info.start_date, date_format)
    create_payload["rounds"][0]["endDate"] = datetime.datetime.strftime(
        info.start_date + datetime.timedelta(hours=2), date_format)

    create_payload["rounds"][0]["config"]["maps"] = \
        get_maps_from_campaign(info.campaign_club_id, info.campaign_id, token)

    create_payload["rounds"][0]["config"]["scriptSettings"]["S_TeamsUrl"] = info.team_pastebin_url

    print(json.dumps(create_payload))

    create_comp_url = "https://competition.trackmania.nadeo.club/api/competitions/web/create"
    response = requests.post(
        url=create_comp_url,
        headers={'Authorization': 'nadeo_v1 t=' + token},
        json=json.dumps(create_payload))

    print(response)
    print(response.text)
