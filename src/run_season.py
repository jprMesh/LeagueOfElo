from elo import elo

def LCS():
    LEAGUE = "LCS"

    lcs = elo.EloRatingSystem(LEAGUE, "../data/{}/teams.csv".format(LEAGUE), K=30)
    lcs.loadGames("../data/LCS/LCS 2018 Spring/reg_season.games")
    lcs.loadGames("../data/LCS/LCS 2018 Spring/playoffs.games")
    lcs.newSeasonReset()
    lcs.loadGames("../data/LCS/LCS 2018 Summer/reg_season.games")
    lcs.loadGames("../data/LCS/LCS 2018 Summer/playoffs.games")
    lcs.newSeasonReset()
    lcs.loadGames("../data/LCS/LCS 2019 Spring/reg_season.games")
    lcs.loadGames("../data/LCS/LCS 2019 Spring/playoffs.games")
    lcs.predict('C9', 'TSM')
    lcs.predict('TL', 'FLY')
    print(lcs)
    lcs.printBrier()
    lcs.plot()

def LEC():
    LEAGUE = "LEC"

    lec = elo.EloRatingSystem(LEAGUE, "../data/{}/teams.csv".format(LEAGUE), K=30)
    lec.loadGames("../data/LEC/LEC 2018 Summer/reg_season.games")
    lec.loadGames("../data/LEC/LEC 2018 Summer/playoffs.games")
    lec.newSeasonReset()
    lec.loadGames("../data/LEC/LEC 2019 Spring/reg_season.games")
    print(lec)
    lec.plot()

LCS()
#LEC()