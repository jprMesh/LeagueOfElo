import mwclient
from leaguepedia_login import login, key

class Leaguepedia_DB(object):
    def __init__(self):
        self.lpdb = mwclient.Site('lol.gamepedia.com', path='/')
        self.lpdb.login(login, key)

    def get_season_results(self, season):
        r = self.lpdb.api('cargoquery',
                limit='max',
                tables="MatchSchedule=MS",
                fields = "MS.Team1,MS.Team2,MS.Team1Score,MS.Team2Score",
                where= 'MS.ShownName="{}"'.format(season),
                order_by = "MS.DateTime_UTC ASC")

        x = [(y['title']['Team1'], y['title']['Team2'], y['title']['Team1Score'], y['title']['Team2Score']) for y in r['cargoquery']]
        return x

if __name__ == '__main__':
    from pprint import pprint
    lpdb = Leaguepedia_DB()
    pprint(lpdb.get_season_results('LCS 2019 Spring Playoffs'))