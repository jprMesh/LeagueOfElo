from elo import elo
from get_league_data import Leaguepedia_DB
from sys import argv

teamfiles = {
    'LCS': '../cfg/LCS_teams.csv',
    'LEC': '../cfg/LEC_teams.csv',
    'LCK': '../cfg/LCK_teams.csv',
    'LPL': '../cfg/LPL_teams.csv'
}
reset_seasons = ['Spring', 'Summer']
region_alts = {
    'LCS': 'NA LCS',
    'LEC': 'EU LCS'
}

def run_model(model, region):
    lpdb = Leaguepedia_DB()
    region_alt = region_alts.get(region, 'None')
    season_list = lpdb.getAllSeasons(region, '2018-01-01', region_alt)
    teamfile = teamfiles.get(region)
    league = model(region, teamfile, K=30)

    for season in season_list:
        if "Promotion" in season:
            continue
        if season.split()[-1] in reset_seasons:
            league.newSeasonReset()
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
    region = argv[2].upper()
    run_model(model, region)
