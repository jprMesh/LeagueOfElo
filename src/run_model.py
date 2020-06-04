from elo import elo
from get_league_data import Leaguepedia_DB
from sys import argv
import time


teamfiles = {
    'North America': '../cfg/LCS_teams.csv',
    'Europe': '../cfg/LEC_teams.csv',
    'Korea': '../cfg/LCK_teams.csv',
    'China': '../cfg/LPL_teams.csv'
}
regions = {
    'NA': 'North America',
    'EU': 'Europe',
    'KR': 'Korea',
    'CN': 'China'
}


def run_model(model, region):
    lpdb = Leaguepedia_DB()
    today = time.strftime('%Y-%m-%d')
    season_list = lpdb.getTournaments(region, '2015-01-01', today)
    teamfile = teamfiles.get(region)
    league = model(region, teamfile, K=30)

    for season in season_list:
        if season.split()[-1] in ['Spring', 'Summer']:
            league.newSeasonReset(season)
        league.loadRosters(lpdb.getSeasonRosters(season))
        results = lpdb.getSeasonResults(season)
        print(season, len(results))
        league.loadGames(results, "Playoffs" in season)
    league.printStats()


if len(argv) < 3:
    exit()
else:
    player_model = argv[1].lower() == 'player'
    model = elo.PlayerEloRatingSystem if player_model else elo.EloRatingSystem
    region = regions.get(argv[2])
    run_model(model, region)
