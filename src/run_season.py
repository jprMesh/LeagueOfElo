from elo import elo
from get_league_data import Leaguepedia_DB

def LCS():
    lpdb = Leaguepedia_DB()
    SEASON_RESET = None

    lcs_seasons = [
        "NA LCS 2018 Spring",
        "NA LCS 2018 Spring Playoffs",
        SEASON_RESET,
        "NA LCS 2018 Summer",
        "NA LCS 2018 Summer Playoffs",
        SEASON_RESET,
        "LCS 2019 Spring",
        "LCS 2019 Spring Playoffs",
        SEASON_RESET,
        "LCS 2019 Summer",
        "LCS 2019 Summer Playoffs",
        SEASON_RESET,
        "LCS 2020 Spring",
        "LCS 2020 Spring Playoffs",
        ]

    lcs = elo.EloRatingSystem("LCS", "../cfg/LCS_teams.csv", K=30)
    for season in lcs_seasons:
        if season:
            results = lpdb.get_season_results(season)
            lcs.loadGames(results, "Playoffs" in season)
        else:
            lcs.newSeasonReset()

    lcs.stats()

LCS()
#LEC()