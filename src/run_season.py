from elo import elo

def LCS():
    SEASON = "LCS_2019_Spring"

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
    SEASON = "LEC_2019_Spring"

    ratings = elo.EloRatingSystem(SEASON, "../data/{}/teams.csv".format(SEASON), K=50)
    ratings.loadGames("../data/{}/reg_season.games".format(SEASON))
    ratings.predict('SK', 'SPY')
    ratings.predict('FNC', 'VIT')
    # ratings.loadGames("../data/{}/playoffs.games".format(SEASON))
    # ratings.predict('FNC', 'SPY')
    # ratings.predict('OG', 'G2')
    print(ratings)
    ratings.plot()
