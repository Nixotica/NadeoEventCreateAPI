import datetime
import json
import os.path
import time
import urllib
import urllib3
import requests
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
            print("found pair locally")
            return team["S_TeamsUrl"]

    paste = json.load(open(os.path.join(os.path.curdir, "tmwt_scrim/utils/payloads/TeamsPastebin.json")))

    paste[0]["Id"] = team_1.id
    paste[0]["Name"] = team_1.id
    paste[0]["Players"][0]["AccountId"] = team_1.account_id_1
    paste[0]["Players"][1]["AccountId"] = team_1.account_id_2

    paste[1]["Id"] = team_2.id
    paste[1]["Name"] = team_2.id
    paste[1]["Players"][0]["AccountId"] = team_2.account_id_1
    paste[1]["Players"][1]["AccountId"] = team_2.account_id_2

    url = "https://pastebin.com/api/api_post.php"
    values = {
        "api_dev_key": pastebin_info.api_dev_key,
        "api_option": "paste",
        "api_paste_code": json.dumps(paste)
    }
    data = urllib.parse.urlencode(values).encode("utf-8")
    pastebin_url = urllib.request.urlopen(url, data).read().decode()

    with open(os.path.join(os.path.curdir, "tmwt_scrim/utils/team_pastebin_pairs.json"), 'r+') as f:
        file_data = json.load(f)
        file_data.append({
            "Team_Ids": [
                team_1.id,
                team_2.id
            ],
            "S_TeamsUrl": pastebin_url
        })
        f.seek(0)
        json.dump(file_data, f, indent=4)

    return pastebin_url


def add_team_to_match(token: str, comp_id: int, match_id: int, team: TeamInfo) -> str:
    """
    Create team for the competition and add them to the provided match.
    :param token: NadeoClubServices token
    :param comp_id: The competition ID
    :param match_id: The match ID
    :param team: The team to add to the match for this competition
    """
    create_team_payload = json.load(open(os.path.join(os.path.curdir, "tmwt_scrim/utils/payloads/CreateTeam.json")))
    create_team_payload["id"] = team.id
    create_team_payload["name"] = team.id
    create_team_payload["seed"] = team.seed
    create_team_payload["members"][0]["member"] = team.account_id_1
    create_team_payload["members"][1]["member"] = team.account_id_2

    create_team_url = f"https://competition.trackmania.nadeo.club/api/competitions/{comp_id}/teams"
    requests.post(
        url=create_team_url,
        headers={'Authorization': 'nadeo_v1 t=' + token},
        json=create_team_payload
    )

    add_team_to_match_payload = \
        json.load(open(os.path.join(os.path.curdir, "tmwt_scrim/utils/payloads/AddTeamToMatch.json")))
    add_team_to_match_payload["team"] = team.id

    add_team_to_match_url = f"https://competition.trackmania.nadeo.club/api/matches/{match_id}/add-team"
    requests.post(
        url=add_team_to_match_url,
        headers={'Authorization': 'nadeo_v1 t=' + token},
        json=add_team_to_match_payload
    )


def create_scrim(token: str, info: ScrimInfo) -> str:
    """
    Creates the base scrim using scrim info
    :param token: Nadeo Club Services token
    :param info:
    :return: Match ID
    """
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

    club_services_header = {'Authorization': 'nadeo_v1 t=' + token}

    create_comp_url = "https://competition.trackmania.nadeo.club/api/competitions/web/create"
    response = requests.post(
        url=create_comp_url,
        headers=club_services_header,
        json=create_payload
    ).json()
    comp_id = response["id"]

    get_rounds_url = f"https://competition.trackmania.nadeo.club/api/competitions/{comp_id}/rounds"
    response = requests.get(
        url=get_rounds_url,
        headers=club_services_header
    ).json()
    round_id = response[0]["id"]

    create_empty_match_url = f"https://competition.trackmania.nadeo.club/api/rounds/{round_id}/empty-match"
    requests.post(
        url=create_empty_match_url,
        headers=club_services_header
    )

    # For some reason this can take some time
    time.sleep(2)
    get_round_match_url = f"https://competition.trackmania.nadeo.club/api/rounds/{round_id}/matches"
    response = requests.get(
        url=get_round_match_url,
        headers=club_services_header
    ).json()
    match_id = response["matches"][0]["id"]

    add_team_to_match(token, comp_id, match_id, info.team_1)
    add_team_to_match(token, comp_id, match_id, info.team_2)
