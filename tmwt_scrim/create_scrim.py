import datetime

import yaml

from tmwt_scrim.utils.apis import *

teams_pastebin_post_url = "https://competition.trackmania.nadeo.club/api/competitions/4825/teams"
add_team_to_match_post_url = "https://competition.trackmania.nadeo.club/api/matches/48214/add-team"
create_empty_match_post_url = "https://competition.trackmania.nadeo.club/api/rounds/11925/empty-match"

def create_scrim_from_config(config: str):
    with open(os.path.join(os.path.curdir, f"tmwt_scrim/scrim_configs/{config}")) as stream:
        scrim = yaml.safe_load(stream)

    team_1 = TeamInfo(
        scrim["Team 1"]["Id"],
        scrim["Team 1"]["Player 1"],
        scrim["Team 1"]["Player 2"]
    )
    team_2 = TeamInfo(
        scrim["Team 2"]["Id"],
        scrim["Team 2"]["Player 1"],
        scrim["Team 2"]["Player 2"]
    )
    pastebin_info = PastebinInfo(
        os.environ["PASTEBIN_DEV_KEY"],
        os.environ["PASTEBIN_USER"],
        os.environ["PASTEBIN_PASS"]
    )

    s_teamsurl = get_team_pair_pastebin_url(team_1, team_2, pastebin_info)

    if scrim["Start Date"]:
        date_format = "%m/%d/%Y %H:%M:%S"
        start_date = datetime.datetime.strptime(scrim["Start Date"], date_format)
    elif scrim["Start Offset"]:
        start_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=scrim["Start Offset"])
    else:
        start_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=3)

    scrim_info = ScrimInfo(
        scrim["Name"],
        scrim["My Club"],
        scrim["Campaign Club"],
        scrim["Campaign"],
        start_date,
        team_1,
        team_2,
        s_teamsurl
    )

    token = authenticate("NadeoClubServices", os.environ["AUTHORIZATION"])

    create_base_scrim(token, scrim_info)
