from elo import elo

SEASON = "LCS_2019_Spring"

lcs_ratings = elo.EloRatingSystem(SEASON, "../data/{}/teams.csv".format(SEASON), K=50)
lcs_ratings.loadGames("../data/{}/reg_season.games".format(SEASON))
lcs_ratings.plot()
print(lcs_ratings)