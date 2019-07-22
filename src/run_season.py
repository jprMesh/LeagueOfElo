from elo import elo
from get_league_data import Leaguepedia_DB

def LCS():
    lpdb = Leaguepedia_DB()
    SEASON_RESET = None

    lcs_seasons = [
        "LCS 2018 Spring",
        "LCS 2018 Spring Playoffs",
        SEASON_RESET,
        "LCS 2018 Summer",
        "LCS 2018 Summer Playoffs",
        SEASON_RESET,
        "LCS 2019 Spring",
        "LCS 2019 Spring Playoffs",
        SEASON_RESET,
        "LCS 2019 Summer",
        "LCS 2019 Summer Playoffs",
        ]

    lcs = elo.EloRatingSystem("LCS", "../data/LCS/teams.csv", K=30)
    for season in lcs_seasons:
        if season:
            results = lpdb.get_season_results(season)
            lcs.loadGames(results)
        else:
            lcs.newSeasonReset()

    lcs.predict('Team Liquid', 'Cloud9')
    lcs.stats()

LCS()
#LEC()