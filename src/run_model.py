from elo import elo
from get_league_data import Leaguepedia_DB
from typing import Dict
from time import strftime
import argparse


teamfiles = {
    'NA': '../cfg/LCS_teams.csv',
    'EU': '../cfg/LEC_teams.csv',
    'KR': '../cfg/LCK_teams.csv',
    'CN': '../cfg/LPL_teams.csv'
}


def runModel(model, region, start_year, stop_date):
    lpdb = Leaguepedia_DB()
    teamfile = teamfiles.get(region)
    league = model(region, teamfile, K=30)
    season_list = lpdb.getTournaments(region, f'{start_year}-01-01', stop_date)

    for season in season_list:
        if season.split()[-1] in ['Spring', 'Summer']:
            league.newSeasonReset(season)
        league.loadRosters(lpdb.getSeasonRosters(season))
        results = lpdb.getSeasonResults(season)
        print(season, len(results))
        league.loadGames(results, 'Playoffs' in season)
    league.printStats()


def parseArgs() -> Dict:
    parser = argparse.ArgumentParser()
    parser.add_argument('region', choices=['NA', 'EU', 'KR', 'CN'],
                        help='Region to run the model on.')
    parser.add_argument('start_year', nargs='?', type=int, choices=range(2010, int(strftime('%Y'))+1), default=2010,
                        help='Year from which to start training the model. Defaults to 2010.')
    parser.add_argument('stop_date', nargs='?', type=str, default=strftime('%Y-%m-%d'),
                        help='Date to stop processing data in YYYY-MM-DD format. Defaults to current day.')
    parser.add_argument('--player_model', '-p', dest='model', action='store_const',
                        const=elo.PlayerEloRatingSystem, default=elo.EloRatingSystem,
                        help='Use the player-based elo model rather than the team-based rating system')
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = parseArgs()
    runModel(**args)
