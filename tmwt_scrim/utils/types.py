import datetime


class TeamInfo:
    def __init__(
            self,
            team_id: str,
            seed: int,
            account_id_1: str,
            account_id_2: str
    ):
        self.id = team_id
        self.seed = seed
        self.account_id_1 = account_id_1
        self.account_id_2 = account_id_2


class PastebinInfo:
    def __init__(
            self,
            api_dev_key: str,
            username: str,
            password: str
    ):
        self.api_dev_key = api_dev_key
        self.username = username
        self.password = password


class ScrimInfo:
    def __init__(
            self,
            name: str,
            my_club_id: int,
            campaign_club_id: int,
            campaign_id: int,
            start_date: datetime,
            team_1: TeamInfo,
            team_2: TeamInfo,
            team_pastebin_url: str,
    ):
        self.name = name
        self.my_club_id = my_club_id
        self.campaign_club_id = campaign_club_id
        self.campaign_id = campaign_id
        self.start_date = start_date
        self.team_1 = team_1
        self.team_2 = team_2
        self.team_pastebin_url = team_pastebin_url
