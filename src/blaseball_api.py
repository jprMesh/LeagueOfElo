import requests as r


class Blaseball_API(object):
    def __init__(self):
        pass

    def getTeams(self):
        all_teams_endpoint = 'https://www.blaseball.com/database/allTeams'
        resp = r.get(all_teams_endpoint)
        if resp.status_code != 200:
            raise Exception('Endpoint Inaccessible')
        return resp.json()

    def getSeasons(self):
        pass

    def getMatchResults(self):
        pass


if __name__ == '__main__':
    from pprint import pprint
    bbapi = Blaseball_API()
    pprint(bbapi.getTeams())
    #pprint(bbapi.getTournaments('idk'))
    #pprint(bbapi.getSeasonResults('season'))
