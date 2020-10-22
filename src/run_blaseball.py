#!/usr/local/bin/python3

from elo import elo
from blaseball_api import Blaseball_API


def runBlaseballModel():
    bbapi = Blaseball_API()
    teams = bbapi.getTeams()
    bb_league = elo.EloRatingSystem('Blaseball', K=30)
    bb_league.loadTeamsDict(teams)

    bb_league.getActiveTeamsRatings();return
    season_list = bbapi.getSeasons(regions, start_year, stop_date)

    for season in season_list:
        split = new_split[0]
        split_transmissions.append(season)

    for season in season_list:
        print(season)
        bb_league.newSeasonReset(season, rating_reset=True)
        results = bbapi.getMatchResults(season)
        print(season, len(results))
        bb_league.loadGames(results)
    bb_league.printStats()
    bb_league.genPlots('.', no_open=False)


if __name__ == '__main__':
    runBlaseballModel()
