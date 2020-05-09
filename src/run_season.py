from elo import elo
from get_league_data import Leaguepedia_DB
from sys import argv

SEASON_RESET = None
seasons = {
    'LCS':[
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
        ],
    'LEC':[
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
        ],
    'LCK':[
        "LCK 2019 Spring",
        "LCK 2019 Spring Playoffs",
        SEASON_RESET,
        "LCK 2019 Summer",
        "LCK 2019 Summer Playoffs",
        SEASON_RESET,
        "LCK 2020 Spring",
        "LCK 2020 Spring Playoffs",
        ],
    'test':[
        "LCS 2019 Spring",
        "LCS 2019 Spring Playoffs",
        SEASON_RESET,
        "LCS 2019 Summer",
        "LCS 2019 Summer Playoffs",
        SEASON_RESET,
        "LCS 2020 Spring",
    ]
}

teamfiles = {
    'LCS': '../cfg/LCS_teams.csv',
    'LEC': '../cfg/LEC_teams.csv',
    'LCK': '../cfg/LCK_teams.csv',
    'test': '../cfg/LCS_teams.csv'
}

def run_league(region):
    season_list = seasons.get(region)
    teamfile = teamfiles.get(region)
    league = elo.EloRatingSystem(region, teamfile, K=30)
    lpdb = Leaguepedia_DB()

    for season in season_list:
        if season:
            results = lpdb.get_season_results(season)
            league.loadGames(results, "Playoffs" in season)
        else:
            league.newSeasonReset()
    league.printStats()

def run_pleague(region):
    season_list = seasons.get(region)
    teamfile = teamfiles.get(region)
    league = elo.PlayerEloRatingSystem(region, teamfile, K=30)
    lpdb = Leaguepedia_DB()

    for season in season_list:
        if season:
            league.loadRosters(lpdb.getSeasonRosters(season))
            results = lpdb.get_season_results(season)
            league.loadGames(results, "Playoffs" in season)
        else:
            league.newSeasonReset()
    league.printStats()

if len(argv) != 2:
    exit()
else:
    if argv[1] != 'test':
        run_pleague(argv[1])
    else:
        run_league(argv[1])
