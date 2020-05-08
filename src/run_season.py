from elo import elo
from get_league_data import Leaguepedia_DB

def run_league(region):
    lpdb = Leaguepedia_DB()
    SEASON_RESET = None

    if region == "LCS":
        seasons = [
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
        league = elo.EloRatingSystem(region, "../cfg/LCS_teams.csv", K=30)
    elif region == "LEC":
        seasons = [
            "EU LCS 2018 Spring",
            "EU LCS 2018 Spring Playoffs",
            SEASON_RESET,
            "EU LCS 2018 Summer",
            "EU LCS 2018 Summer Playoffs",
            SEASON_RESET,
            "LEC 2019 Spring",
            "LEC 2019 Spring Playoffs",
            SEASON_RESET,
            "LEC 2019 Summer",
            "LEC 2019 Summer Playoffs",
            SEASON_RESET,
            "LEC 2020 Spring",
            "LEC 2020 Spring Playoffs",
            ]
        league = elo.EloRatingSystem(region, "../cfg/LEC_teams.csv", K=30)
    elif region == "LCK":
        seasons = [
            "LCK 2019 Spring",
            "LCK 2019 Spring Playoffs",
            SEASON_RESET,
            "LCK 2019 Summer",
            "LCK 2019 Summer Playoffs",
            SEASON_RESET,
            "LCK 2020 Spring",
            "LCK 2020 Spring Playoffs",
            ]
        league = elo.EloRatingSystem(region, "../cfg/LCK_teams.csv", K=30)
    else:
        exit()

    for season in seasons:
        if season:
            results = lpdb.get_season_results(season)
            league.loadGames(results, "Playoffs" in season)
        else:
            league.newSeasonReset()
    league.printStats()

def run_pleague(region):
    lpdb = Leaguepedia_DB()
    SEASON_RESET = None

    if region == "LCS":
        seasons = [
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
        teamfile = "../cfg/LCS_teams.csv"
    elif region == "LEC":
        seasons = [
            "EU LCS 2018 Spring",
            "EU LCS 2018 Spring Playoffs",
            SEASON_RESET,
            "EU LCS 2018 Summer",
            "EU LCS 2018 Summer Playoffs",
            SEASON_RESET,
            "LEC 2019 Spring",
            "LEC 2019 Spring Playoffs",
            SEASON_RESET,
            "LEC 2019 Summer",
            "LEC 2019 Summer Playoffs",
            SEASON_RESET,
            "LEC 2020 Spring",
            "LEC 2020 Spring Playoffs",
            ]
        teamfile = "../cfg/LEC_teams.csv"
    elif region == "LCK":
        seasons = [
            "LCK 2019 Spring",
            "LCK 2019 Spring Playoffs",
            SEASON_RESET,
            "LCK 2019 Summer",
            "LCK 2019 Summer Playoffs",
            SEASON_RESET,
            "LCK 2020 Spring",
            "LCK 2020 Spring Playoffs",
            ]
        teamfile = "../cfg/LCK_teams.csv"
    else:
        exit()

    league = elo.PlayerEloRatingSystem(region, teamfile, K=30)
    for season in seasons:
        if season:
            league.loadRosters(lpdb.getSeasonRosters(season))
            results = lpdb.get_season_results(season)
            league.loadGames(results, "Playoffs" in season)
        else:
            league.newSeasonReset()
    league.printStats()


run_league("LCK")
