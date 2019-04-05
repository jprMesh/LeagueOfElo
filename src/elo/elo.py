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
        self.alignment = [0]

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
                if game == "#Align#":
                    self.align()
                    continue
                t1, t1s, t2s, t2 = game.split()
                w_team = self.getTeam(t1 if int(t1s) else t2)
                l_team = self.getTeam(t2 if int(t1s) else t1)
                self.adjustRating(w_team, l_team)

    def align(self):
        max_games = 0
        for _, team in self.teams.items():
            max_games = max(max_games, len(team.rating_history[-1]))
            team.rating_history.append([team.rating])
        self.alignment.append(max_games + self.alignment[-1] - 1)

    def newSeasonReset(self):
        for _, team in self.teams.items():
            new_start = team.rating - (team.rating - 1500)/4
            team.rating = new_start
        self.align()

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
        plt.title(self.league_name + " Elo Ratings")
        for _, team in self.teams.items():
            for idx, rh_segment in enumerate(team.rating_history):
                start_idx = self.alignment[idx]
                if idx != 0 and rh_segment[0] == team.rating_history[idx-1][-1]:
                    future_games = max([len(team.rating_history[x]) for x in range(idx, len(self.alignment))])
                    if future_games > 1:
                        prev_end = self.alignment[idx-1]+len(team.rating_history[idx-1]) - 1
                        plt.plot([prev_end, start_idx], [rh_segment[0], rh_segment[0]], team.color, alpha=0.2)
                x_series = list(range(start_idx, start_idx+len(rh_segment)))
                plt.plot(x_series, rh_segment, team.color)
        plt.show()

