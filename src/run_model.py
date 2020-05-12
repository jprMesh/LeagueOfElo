from elo import elo
from get_league_data import Leaguepedia_DB
from sys import argv

SEASON_RESET = None
seasons = {
    'lcs':[
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
    'lec':[
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
    'lck':[
        "LCK 2019 Spring",
        "LCK 2019 Spring Playoffs",
        SEASON_RESET,
        "LCK 2019 Summer",
        "LCK 2019 Summer Playoffs",
        SEASON_RESET,
        "LCK 2020 Spring",
        "LCK 2020 Spring Playoffs",
        ],
    'lpl':[
        "LPL 2018 Spring",
        "LPL 2018 Spring Playoffs",
        SEASON_RESET,
        "LPL 2018 Summer",
        "LPL 2018 Summer Playoffs",
        SEASON_RESET,
        "LPL 2019 Spring",
        "LPL 2019 Spring Playoffs",
        SEASON_RESET,
        "LPL 2019 Summer",
        "LPL 2019 Summer Playoffs",
        SEASON_RESET,
        "LPL 2020 Spring",
        "LPL 2020 Spring Playoffs",
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
    'lcs': '../cfg/LCS_teams.csv',
    'lec': '../cfg/LEC_teams.csv',
    'lck': '../cfg/LCK_teams.csv',
    'lpl': '../cfg/LPL_teams.csv',
    'test': '../cfg/LCS_teams.csv'
}

def run_model(model, region):
    season_list = seasons.get(region)
    teamfile = teamfiles.get(region)
    league = model(region.upper(), teamfile, K=30)
    lpdb = Leaguepedia_DB()

    for season in season_list:
        if season:
            league.loadRosters(lpdb.getSeasonRosters(season))
            results = lpdb.get_season_results(season)
            league.loadGames(results, "Playoffs" in season)
        else:
            league.newSeasonReset()
    league.printStats()


if len(argv) < 3:
    exit()
else:
    player_model = argv[1].lower() == 'player'
    model = elo.PlayerEloRatingSystem if player_model else elo.EloRatingSystem
    region = argv[2].lower()
    run_model(model, region)
