import mwclient
from leaguepedia_login import login, key

class Leaguepedia_DB(object):
    def __init__(self):
        self.lpdb = mwclient.Site('lol.gamepedia.com', path='/')
        self.lpdb.login(login, key)

    def get_season_results(self, season):
        r = self.lpdb.api('cargoquery',
                limit = 'max',
                tables = 'MatchSchedule=MS',
                fields = 'MS.Team1,MS.Team2,MS.Team1Score,MS.Team2Score',
                where = f'MS.ShownName="{season}"',
                order_by = 'MS.DateTime_UTC ASC')

        matches = [(m['title']['Team1'],
                    m['title']['Team2'],
                    m['title']['Team1Score'],
                    m['title']['Team2Score'])
                   for m in r['cargoquery']]
        return matches

    def getSeasonRosters(self, season):
        r = self.lpdb.api('cargoquery',
                limit = 'max',
                tables = 'TournamentRosters=TR',
                fields = 'TR.Team, TR.RosterLinks, TR.Roles',
                where = f'TR.Tournament="{season}"')

        rosters = []
        for m in r['cargoquery']:
            team = m['title']['Team']
            roster = list(zip(m['title']['Roles'].split(';;'),
                              m['title']['RosterLinks'].split(';;')))
            rosters.append([team, roster])
        return rosters

# Unused (for now)
    def get_season_games(self, season):
        r = self.lpdb.api('cargoquery',
                limit = 'max',
                tables = "MatchScheduleGame=MSG,MatchSchedule=MS",
                fields = "MS.Team1,MS.Team2,MS.Team1Score,MS.Team2Score,MSG.GameID_Wiki",
                where = f'MS.ShownName="{season}"', 
                join_on = "MSG.UniqueMatch=MS.UniqueMatch",
                order_by = "MS.DateTime_UTC ASC")

        matches = [m['title'].values()
                   for m in r['cargoquery']]
        return matches

    def get_rosters_seasons(self, season):
        r = self.lpdb.api('cargoquery',
                limit = 'max',
                tables = "MatchScheduleGame=MSG,ScoreboardGame=SG",
                fields = "MSG.GameID_Wiki, SG.ScoreboardID_Wiki, SG.Team1Names, SG.Team2Names",
                where = f'SG.Tournament="{season}"', 
                join_on = "MSG.GameID_Wiki=SG.ScoreboardID_Wiki",
                order_by = "SG.DateTime_UTC ASC")

        matches = [m['title'].values()
                   for m in r['cargoquery']]
        return matches

if __name__ == '__main__':
    from pprint import pprint
    lpdb = Leaguepedia_DB()
    pprint(lpdb.getSeasonRosters('LCS 2020 Spring Playoffs'))

    #pprint(lpdb.get_season_games('LCS 2020 Spring Playoffs'))
    #print("\n")
    #pprint(lpdb.get_rosters_seasons('LCS 2020 Spring Playoffs'))
