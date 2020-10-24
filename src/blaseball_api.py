import requests
from pathlib import Path
import pickle


SRC_PATH = Path(__file__).resolve().parent
CACHE_PATH = Path(SRC_PATH / '..' / 'cache')


class Blaseball_API(object):
    def __init__(self):
        self.api_root = 'https://www.blaseball.com/database/'

    def _query(self, endpoint):
        target = self.api_root + endpoint
        resp = requests.get(target)
        if resp.status_code != 200:
            raise Exception('Endpoint Inaccessible')
        return resp.json()

    def getTeams(self):
        team_data = self._query('allTeams')
        return team_data

    def getMatchResults(self, season, force_fetch=False):
        results_file = Path(CACHE_PATH / 'bb_results' / f's{season}.p')
        if results_file.is_file() and not force_fetch:
            print(f'Using cached data')
            return pickle.load(open(results_file, 'rb'))

        results = []
        for day in range(200):
            if not day%10:
                print('.', end='', flush=True)
            game_data_endpoint = f'games?day={day}&season={season}'
            day_games = self._query(game_data_endpoint)
            #print(day, len(day_games))
            if len(day_games) == 0:
                break
            for game in day_games:
                if game['gameComplete'] != True:
                    continue
                game_results = [
                        game['homeTeam'],
                        game['awayTeam'],
                        game['homeScore'],
                        game['awayScore'],
                        game['isPostseason']+1]
                results.append(game_results)
        pickle.dump(results, open(results_file, 'wb'))
        return results


if __name__ == '__main__':
    from pprint import pprint
    bbapi = Blaseball_API()
    #pprint(bbapi.getTeams())
    bbapi.getMatchResults(0)
    #pprint(bbapi.getTournaments('idk'))
    #pprint(bbapi.getSeasonResults('season'))
