from .team import Team

class EloRatingSystem(object):
    """Elo Rating System for a single league"""
    def __init__(self, league, teamfile, K=20):
        self.league_name = league
        self.K = K
        self.teams = {}
        with open(teamfile, 'r') as teams:
            for team in teams:
                team_info = list(map(str.strip, team.split(',')))
                self.teams[team_info[0]] = Team(*team_info)

    def __repr__(self):
        team_table = []
        for _, team in self.teams.items():
            team_table.append((team.rating, "    {:>3}  {}\n".format(team.abbrev, int(team.rating))))
        team_table.sort(key=lambda tup: tup[0], reverse=True)
        table_str = "{} Elo Ratings\n".format(self.league_name)
        for row in team_table:
            table_str += row[1]
        return table_str

    def getTeam(self, team_abv):
        return self.teams[team_abv]

    def getWinProb(self, team1, team2):
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
        forecast_delta = 1 - self.getWinProb(winning_team, losing_team)
        correction = self.K * forecast_delta
        winning_team.updateRating(correction)
        losing_team.updateRating(-correction)

    def loadGames(self, gamefile):
        with open(gamefile, 'r') as games:
            for game in games:
                game = game.strip()
                if not game:
                    continue
                t1, t1s, t2s, t2 = game.split()
                w_team = self.getTeam(t1 if int(t1s) else t2)
                l_team = self.getTeam(t2 if int(t1s) else t1)
                self.adjustRating(w_team, l_team)

    def predict(self, team1, team2):
        win_prob = self.getWinProb(self.getTeam(team1), self.getTeam(team2))
        if win_prob < 0.5:
            team1, team2 = team2, team1
            win_prob = 1 - win_prob
        print("{} {}% over {}".format(team1, int(win_prob*100), team2))

    def plot(self):
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        fig, ax = plt.subplots()
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(3))
        plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)
        plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        for _, team in self.teams.items():
            plt.plot(team.rating_history, team.color)
        plt.show()

