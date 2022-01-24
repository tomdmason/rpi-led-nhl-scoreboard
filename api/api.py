class LeagueApiInterface:
    BASE_URL = ""
    ENDPOINT_TEAMS = ""
    ENDPOINT_SCHEDULE = ""

    def __init__(self, ) -> None:
        pass

    def getTeamData(self):
        """Get team names and abreviations from the League API, return information as a list of dictionaries.
        Returns:
            teams (list of dictionaries): Each dict contains the longform name and abbreviation of a single team.
        """
        pass

    def getGameData(self, teams):
        """Get game data for all of todays games from the League API, returns games as a list of dictionaries.

        Args:
            teams (list of dictionaries): Team names and abberivations. Needed as the game API doen't return team abbreviations.

        Returns:
            games (list of dictionaries): All game info needed to display on scoreboard. Teams, scores, start times, game clock, etc.
        """
        pass
