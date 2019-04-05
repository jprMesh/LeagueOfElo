class EloRatingSystem(object):
    """Elo Rating System for a single league"""
    def __init__(self, teamfile, K=20):
        self.K = K
        self.teams = {}
        with open(teamfile, 'r') as teams:
            for team in teams:
                team_abbrev = team.split(',')[0].strip()
                team_name = team.split(',')[1].strip()
                self.teams[team_abbrev] = Team(team_name)

    def getTeam(self, team_name):
        pass

    def getWinProbability(self, team1, team2):
        """
        Get the probability that team1 will beat team2.
        @return win probability between 0 and 1.
        """
        rating_diff = team1.rating - team2.rating
        win_prob = 1 / (10**(-rating_diff/400) + 1)
        return win_prob

    def adjustRating(self, winning_team, losing_team):
        """
        Adjust the model's understanding of two teams based on the outcome of a
        match between the two teams.
        """
        forecast_delta = 1 - self.getWinProbability(winning_team, losing_team)
        correction = self.K * forecast_delta
        winning_team.updateRating(correction)
        losing_team.updateRating(-correction)
