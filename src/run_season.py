from elo import elo

def LCS():
    SEASON = "LCS 2019 Spring"

    lcs_ratings = elo.EloRatingSystem(SEASON, "../data/{}/teams.csv".format(SEASON), K=50)
    lcs_ratings.loadGames("../data/{}/reg_season.games".format(SEASON))
    lcs_ratings.predict('FLY', 'GGS')
    lcs_ratings.predict('TSM', 'FOX')
    lcs_ratings.loadGames("../data/{}/playoffs.games".format(SEASON))
    lcs_ratings.predict('C9', 'TSM')
    lcs_ratings.predict('TL', 'FLY')
    print(lcs_ratings)
    lcs_ratings.plot()

def LEC():
    LEAGUE = "LEC"

    ratings = elo.EloRatingSystem(LEAGUE, "../data/{}/teams.csv".format(LEAGUE), K=50)
    ratings.loadGames("../data/LEC/LEC 2018 Summer/reg_season.games")
    ratings.loadGames("../data/LEC/LEC 2018 Summer/playoffs.games")
    ratings.newSeasonReset()
    ratings.loadGames("../data/LEC/LEC 2019 Spring/reg_season.games")
    print(ratings)
    ratings.plot()

LCS()
LEC()