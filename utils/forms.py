from datetime import datetime


class CompetitionBasicInfo:
    def __init__(
            self,
            name: str,
            club: str,
            teams: bool,
            desc: str = None,
            rules: str = None
    ):
        self.name = name
        self.club = club
        self.teams = teams
        self.desc = desc
        self.rules = rules


class RegistrationInfo:
    def __init__(
            self,
            start_date: datetime,
            end_date: datetime,
            max_players: int,
            zones: str = None
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.max_players = max_players
        self.zones = zones


class StructureInfo:
    def __init__(
            self,
            structure_config: str,
            qualifier: bool
    ):
        self.structure_config = structure_config
        self.qualifier = qualifier
