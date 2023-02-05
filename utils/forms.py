import json
from datetime import datetime
from enum import IntEnum


class LeaderboardScore(IntEnum):
    RANKS = 1,
    SKILLPOINTS = 2,
    TIME = 3,


class LeaderboardType(IntEnum):
    BRACKET = 1,
    SUM_SCORE = 2,
    BIGGEST_SCORE = 3,


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


class QualifierInfo:
    def __init__(
            self,
            name: str,
            start_date: datetime,
            end_date: datetime,
            leaderboard_score: LeaderboardScore,
            max_players: int,
            maps: list[str],
            settings: json = None
    ):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.leaderboard_score = leaderboard_score
        self.max_players = max_players
        self.maps = maps
        self.settings = settings


class RoundInfo:
    def __init__(
            self,
            name: str,
            start_date: datetime,
            end_date: datetime,
            leaderboard_type: LeaderboardType,
            script: str,
            max_players: int,
            maps: list[str],
            max_spectators: int = None,
            qualifier: str = None,
            settings: json = None
    ):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.leaderboard_type = leaderboard_type
        self.script = script
        self.max_players = max_players
        self.maps = maps
        self.max_spectators = max_spectators
        self.qualifier = qualifier
        self.settings = settings
