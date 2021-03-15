#!/usr/local/bin/python3

from elo import elo
from blaseball_api import Blaseball_API
from pathlib import Path


def runBlaseballModel(current_season):
    bbapi = Blaseball_API()
    teams = bbapi.getTeams()
    bb_league = elo.EloRatingSystem('Blaseball', K=7)
    bb_league.loadTeamsDict(teams)

    for season in range(current_season):
        print(f'Running Season {season+1}')
        bb_league.newSeasonReset(f'Season {season+1}', rating_reset=True)
        results = bbapi.getMatchResults(season, force_fetch=(season == current_season))
        print(f'  {len(results)} matches')
        bb_league.loadGames(results, using_ids=True)
    bb_league.printStats()
    bb_league.genPlots(Path('.'), no_open=False)


if __name__ == '__main__':
    runBlaseballModel(11)
