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
                self.teams[team_info[1]] = Team(*team_info)
        self.alignment = [0]
        self.season_boundary = []
        self.brier_scores = []

    def __repr__(self):
        team_table = []
        for _, team in self.teams.items():
            team_table.append((team.rating, "    {:>3}  {}\n".format(team.abbrev, int(team.rating))))
        team_table.sort(key=lambda tup: tup[0], reverse=True)
        table_str = "{} Elo Ratings\n".format(self.league_name)
        for row in team_table:
            table_str += row[1]
        return table_str

    def getTeam(self, team_name):
        return self.teams[team_name]

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
        brier = forecast_delta**2
        self.brier_scores.append(brier)

    def loadGames(self, results, elims=False):
        for result in results:
            t1, t2, t1s, t2s = result
            if not t1s:
                continue
            w_team, l_team = (t1, t2) if int(t1s) > int(t2s) else (t2, t1)
            self.adjustRating(self.getTeam(w_team), self.getTeam(l_team))
            if elims:
                self.align()

    def loadGamesFile(self, gamefile):
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
        alignment = max_games + self.alignment[-1] - 1
        self.alignment.append(alignment)
        return alignment

    def newSeasonReset(self):
        for _, team in self.teams.items():
            new_start = team.rating - (team.rating - 1500)/4
            team.rating = new_start
        season_bound = self.align()
        self.season_boundary.append(season_bound)

    def predict(self, team1, team2):
        win_prob = self.getWinProb(self.getTeam(team1), self.getTeam(team2))
        if win_prob < 0.5:
            team1, team2 = team2, team1
            win_prob = 1 - win_prob
        print("{} {}% over {}".format(team1, int(win_prob*100), team2))

    def printBrier(self):
        print("Brier Score: {:.4f}".format(sum(self.brier_scores)/len(self.brier_scores)))

    def plot(self):
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        fig, ax = plt.subplots(figsize=(15, 5))
        plt.subplots_adjust(left=0.05, right=0.95)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=True, left=False, right=False, labelleft=True)
        plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        plt.title(self.league_name + " Elo Ratings")
        for _, team in self.teams.items():
            line_label = None
            for idx, rh_segment in enumerate(team.rating_history):
                start_idx = self.alignment[idx]
                future_games = max([len(team.rating_history[x]) for x in range(idx, len(self.alignment))])
                if idx != 0 and future_games > 1:
                    prev_end = self.alignment[idx-1]+len(team.rating_history[idx-1]) - 1
                    prev_rating = team.rating_history[idx-1][-1]
                    plt.plot([prev_end, start_idx], [prev_rating, prev_rating], team.color, alpha=0.2)
                x_series = list(range(start_idx, start_idx+len(rh_segment)))
                line_label, = plt.plot(x_series, rh_segment, team.color)
            if not team.color == '#000000':
                line_label.set_label(team.abbrev)
        for bound in self.season_boundary:
            plt.axvline(x=bound, color='k', linewidth=1)
        plt.legend(loc='upper left')
        plt.show()

    def stats(self):
        self.printBrier()
        print(self)
        self.plot()
