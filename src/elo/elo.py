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
            team_table.append((team.rating, f"  {team.abbrev:>3}  {int(team.rating)}\n"))
        team_table.sort(key=lambda tup: tup[0], reverse=True)
        table_str = "{} Elo Ratings\n".format(self.league_name)
        for row in team_table:
            table_str += row[1]
        return table_str

    def get_active_teams_ratings(self):
        team_table = []
        for _, team in self.teams.items():
            if team.inactive:
                continue
            team_table.append((team.rating, f"  {team.abbrev:>3}  {int(team.rating)}\n"))
        team_table.sort(key=lambda tup: tup[0], reverse=True)
        table_str = "{} Elo Ratings\n".format(self.league_name)
        for row in team_table:
            table_str += row[1]
        return table_str

    def getTeam(self, team_name):
        team = self.teams.get(team_name)
        if not team:
            for _, t in self.teams.items():
                if team_name == t.abbrev:
                    team = t
                    break
        if not team:
            raise ValueError("Team does not exist")
        return team


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
        winning_team.updateRating(self.K * forecast_delta)
        losing_team.updateRating(self.K * -forecast_delta)
        self.brier_scores.append(forecast_delta**2)

    def loadGames(self, results, align=False):
        for result in results:
            t1, t2, t1s, t2s = result
            if not t1s:
                continue
            w_team, l_team = (t1, t2) if int(t1s) > int(t2s) else (t2, t1)
            self.adjustRating(self.getTeam(w_team), self.getTeam(l_team))
            if align:
                self.align()

    def align(self):
        max_games = max([len(self.teams[team].rating_history[-1]) for team in self.teams])
        for _, team in self.teams.items():
            if len(set(team.rating_history[-1])) == 1:
                team.inactive = True
            else:
                team.inactive = False
            game_diff = max_games - len(team.rating_history[-1])
            team.rating_history[-1].extend([team.rating] * game_diff)

    def newSeasonReset(self):
        self.align()
        for _, team in self.teams.items():
            if not team.inactive:
                team.rating = team.rating*0.75 + 1500*0.25
            team.rating_history.append([team.rating])

    def predict(self, team1, team2):
        win_prob = self.getWinProb(self.getTeam(team1), self.getTeam(team2))
        if win_prob < 0.5:
            team1, team2 = team2, team1
            win_prob = 1 - win_prob
        print(f"{team1} {int(win_prob*100)}% over {team2}")

    def printBrier(self):
        brier = sum(self.brier_scores)/len(self.brier_scores)
        print(f"Brier Score: {brier:.4f}")

    def stats(self):
        self.printBrier()
        print(self.get_active_teams_ratings())
        data, colors = self.export_data()
        EloPlotter.matplotlib_plot(self.league_name, data, colors)

    def export_data(self):
        data = {}
        colors = {}
        for team in self.teams:
            abbrev = self.teams[team].abbrev
            colors[abbrev] = self.teams[team].color
            data[abbrev] = self.teams[team].rating_history
        return data, colors

class EloPlotter(object):
    """Plots elo over time"""
    @staticmethod
    def matplotlib_plot(league, data, colors):
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        import matplotlib.patheffects as path_effects
        from statistics import median

        fig, ax = plt.subplots(figsize=(15, 5))
        plt.subplots_adjust(left=0.05, right=0.95)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=False, left=False, right=False, labelleft=True)
        plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        plt.title(f"{league} Elo Ratings")

        label_positions = []
        end_idx = 0
        for team in data:
            team_data = data[team]
            start_idx = 0
            for split_data in team_data:
                end_idx = start_idx + len(split_data) - 1
                plt.axvline(x=end_idx, color='k', linewidth=1)
                x_series = list(range(start_idx, end_idx+1))
                start_idx = end_idx
                if len(set(split_data)) != 1:
                    plt.plot(x_series, split_data, colors[team])
            if len(set(team_data[-1])) != 1:
                label_positions.append((team_data[-1][-1], team))

        def distribute_labels(label_positions):
            median = median([val[0] for val in label_positions])
            label_positions.sort(key=lambda tup: abs(median-tup[0]))
            used_min = 9999
            used_max = 0
            adjusted_positions = []
            for item in label_positions:
                score = item[0]
                if score > used_max or score < used_min:
                    adjusted_positions.append(item)
                    used_max = max(used_max, score+15)
                    used_min = min(used_min, score-15)
                else:
                    if used_max - score < score - used_min:
                        adjusted_positions.append((used_max+1, item[1]))
                        used_max += 16
                    else:
                        adjusted_positions.append((used_min-1, item[1]))
                        used_min -= 16
            return adjusted_positions
        
        adjusted_positions = distribute_labels(label_positions)
        for team in adjusted_positions:
            text = plt.text(end_idx+1, team[0], team[1], color=colors[team[1]], weight='bold')
        plt.show()
