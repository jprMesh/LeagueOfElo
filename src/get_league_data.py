import mwclient
from leaguepedia_login import login, key

site = mwclient.Site('lol.gamepedia.com', path='/')
site.login(login, key)

r = site.api('cargoquery',
        limit='max',
        tables="MatchSchedule=MS",
        fields = "MS.Team1,MS.Team2,MS.Winner, MS.ShownName",
        where= 'MS.ShownName="LCS 2019 Summer"',
        order_by = "MS.DateTime_UTC DESC")

x = [(y['title']['Team1'], y['title']['Team2'], y['title']['Winner']) for y in r['cargoquery']]
print(x)
print(len(x))