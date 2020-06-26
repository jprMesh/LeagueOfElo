from elo import elo
from get_league_data import Leaguepedia_DB
from typing import Dict
from time import strftime
import argparse
import re


TEAMFILES = {
    'NA': ('../cfg/LCS_teams.csv', 2015),
    'EU': ('../cfg/LEC_teams.csv', 2015),
    'KR': ('../cfg/LCK_teams.csv', 2015),
    'CN': ('../cfg/LPL_teams.csv', 2015),
    'INT': ('../cfg/INT_teams.csv', 2015),
}
IGNORE_TOURNAMENTS = [
    'Rift Rivals',
    'EU Face-Off',
    'Mid-Season Showdown']


def runMultiRegion(model, region, stop_date):
    regions = ['NA', 'EU', 'KR', 'CN', 'INT'] if region == 'ALL' else [region]
    teamfiles = []
    start_year = 2010
    for region in regions:
        teamfile, region_start_year = TEAMFILES.get(region)
        teamfiles.append(teamfile)
        start_year = max(start_year, region_start_year)
    league = model('_'.join(regions), teamfiles, K=30)
    lpdb = Leaguepedia_DB()
    season_list = lpdb.getTournaments(regions, start_year, stop_date)
    season_list = filter(lambda x: all([t not in x for t in IGNORE_TOURNAMENTS]), season_list)

    year = None
    split = None
    for season in season_list:
        new_split = re.search('(Spring|Summer|MSI|Worlds|Mid-Season Cup)', season)
        if new_split and new_split[0] != split:
            split = new_split[0]
            year = re.search('\d\d\d\d', season)[0]
            print(f'{year} {split}')
            if split in ['Spring', 'Summer']:
                league.newSeasonReset(f'{year} {split}')
            else:
                league.newSeasonReset(split, rating_reset=True)
        league.loadRosters(lpdb.getSeasonRosters(season))
        results = lpdb.getSeasonResults(season)
        #print(season, len(results))
        league.loadGames(results, 'Playoffs' in season)
    league.printStats()

def parseArgs() -> Dict:
    parser = argparse.ArgumentParser()
    parser.add_argument('region', choices=['NA', 'EU', 'KR', 'CN', 'ALL'], default='ALL',
                        help='Region to run the model on.', nargs='?')
    parser.add_argument('stop_date', nargs='?', type=str, default=strftime('%Y-%m-%d'),
                        help='Date to stop processing data in YYYY-MM-DD format. Defaults to current day.')
    parser.add_argument('--player_model', '-p', dest='model', action='store_const',
                        const=elo.PlayerEloRatingSystem, default=elo.EloRatingSystem,
                        help='Use the player-based elo model rather than the team-based rating system')
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = parseArgs()
    runMultiRegion(**args)
