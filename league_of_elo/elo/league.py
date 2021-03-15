from .team import *
from .rating_system import RatingSystem
from statistics import mean
import re


class League(object):
    """League class manages teams and historical ratings"""
    def __init__(self, league_name:str, rating_system:RatingSystem):
        self.league_name = league_name
        self.rating_system = rating_system
        self.teams = {}
        self.teams_by_region = {}
        self.alignment = [0]
        self.season_boundary = []
        self.seasons = []

    def __repr__(self):
        team_table = []
        for _, team in self.teams.items():
            team_table.append((team.getRating(), f"  {team.abbrev:>3}  {int(team.getRating())}\n"))
        team_table.sort(key=lambda tup: tup[0], reverse=True)
        table_str = "{} Elo Ratings\n".format(self.league_name)
        for row in team_table:
            table_str += row[1]
        return table_str

## Public
    def getActiveTeamsRatings(self):
        team_table = []
        for _, team in self.teams.items():
            if team.inactive:
                continue
            team_table.append((team.getRating(), f"  {team.abbrev:>3}  {int(team.getRating())}\n"))
        team_table.sort(key=lambda tup: tup[0], reverse=True)
        table_str = "{} Elo Ratings\n".format(self.league_name)
        for row in team_table:
            table_str += row[1]
        return table_str

    def loadTeams(self, teamfile, region):
        self.teams_by_region[region] = []
        with open(teamfile, 'r') as teams:
            for team in teams:
                team_info = Team.info(*list(map(str.strip, team.split(','))))
                self._addTeam(team_info, region)

    def loadGames(self, results, playoffs=False, using_ids=False):
        for result in results:
            t1, t2, t1s, t2s, date, match_round = result
            if not t1s or not match_round:
                continue
            try:
                if using_ids:
                    t1 = self._getTeam(team_id=t1)
                    t2 = self._getTeam(team_id=t2)
                else:
                    t1 = self._getTeam(team_name=t1)
                    t2 = self._getTeam(team_name=t2)
            except ValueError:
                print(f"Unknown team. Ignoring match. {t1}, {t2}")
                continue

            winloss_args = (t1.getRating(), t2.getRating(), int(t1s), int(t2s))
            t1_updated, t2_updated = self.rating_system.process_outcome(*winloss_args)
            t1.updateRating(t1_updated)
            t2.updateRating(t2_updated)

    def loadRosters(self, rosters):
        pass

    def newSeasonReset(self, season_name, rating_reset=None):
        try:
            self.seasons.append(season_name[re.search('\d\d\d\d', season_name).start():])
        except:
            self.seasons.append(season_name)
        self._align()
        for region, teams in self.teams_by_region.items():
            regional_avg = self._getRegionalAverage(region)
            for t in teams:
                team = self._getTeam(team_id=t)
                if rating_reset:
                    team.team_rating = team.getRating()*0.75 + regional_avg*0.25
                team.rating_history.append([team.getRating()])

    def printStats(self):
        print(self.rating_system.getBrier())
        print(self.rating_system.getUpDown())

    def genPlots(self, docs_path, no_open):
        self._align()
        data, colors, seasons = self._exportData()
        #EloPlotter.matplotlib_plot(self.league_name, data, colors)
        EloPlotter.plotly_plot(self.league_name, data, colors, seasons, docs_path, no_open)

## Private
    def _addTeam(self, team_info, region='Default'):
        try:
            existing_team = self._getTeam(team_id=team_info.id)
        except ValueError:
            self.teams_by_region[region].append(team_info.id)
            self.teams[team_info.id] = Team(*team_info)
        else:
            existing_team.names.extend([team_info.name, team_info.abbrev])

    def _getTeam(self, team_name=None, team_id=None, default=None):
        team = self.teams.get(team_name)
        if not team:
            for _, t in self.teams.items():
                if team_name in t.names or team_id == t.team_id:
                    team = t
                    break
        if not team:
            if not default:
                raise ValueError(f'Team does not exist: {team_name}')
            else:
                print(f"Using dummy team instead of {team_name}")
                team = default
        return team

    def _align(self):
        max_games = max([len(self.teams[team].rating_history[-1]) for team in self.teams])
        for _, team in self.teams.items():
            if len(set(team.rating_history[-1])) == 1:
                team.inactive = True
            else:
                team.inactive = False
            game_diff = max_games - len(team.rating_history[-1])
            team.rating_history[-1].extend([team.getRating()] * game_diff)

    def _getRegionalAverage(self, region):
        ratings = [self._getTeam(t).getRating() for t in self.teams_by_region[region]]
        return mean(ratings)

    def _exportData(self):
        data = {}
        inactive = {}
        colors = {}
        for _, team in sorted(self.teams.items(), key=lambda item: item[1].getRating()):
            abbrev = team.abbrev
            colors[abbrev] = team.color
            if team.inactive:
                inactive[abbrev] = team.rating_history
            else:
                data[abbrev] = team.rating_history
        data.update(inactive)
        return data, colors, self.seasons


class EloPlotter(object):
    """Plots elo over time"""
    @staticmethod
    def matplotlib_plot(league, data, colors):
        import matplotlib.pyplot as plt
        import matplotlib.ticker as ticker
        import matplotlib.patheffects as path_effects

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
            from statistics import median
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

    @staticmethod
    def plotly_plot(league, data, colors, seasons, docs_path, no_open):
        import plotly.graph_objects as go
        import numpy as np

        split_lens = [len(split_len) for split_len in data[list(data.keys())[0]]]
        split_bounds = np.cumsum(split_lens) - 1
        fig = go.Figure(layout_xaxis_showticklabels=False,
                        layout_yaxis_title='Elo Rating',
                        layout_legend_traceorder='grouped+reversed')

        first_inactive = True
        for team, rating_hist in data.items():
            end_rating = rating_hist[-1][-1]
            for split, split_data in enumerate(rating_hist):
                if len(set(split_data)) == 1:
                    rating_hist[split] = [None] * len(split_data)
            team_data = sum(rating_hist, []) # flatten array
            x_series = list(range(0, len(team_data)))
            team_inactive = team_data[-1] == None
            fig.add_trace(go.Scatter(
                x=x_series,
                y=team_data,
                name=f'{team}: {int(end_rating)}' if not team_inactive else 'Inactive',
                text=team,
                hoverinfo='text+x+y',
                line={'color':colors[team]},
                showlegend=False if (team_inactive and not first_inactive) else True,
                legendgroup='inactive' if team_inactive else 'active'))
            if team_inactive:
                first_inactive = False

        # Draw split boundaries
        for idx, split_bound in enumerate(split_bounds):
            fig.add_shape(
                type="rect",
                xref="x",
                yref="paper",
                x0=split_bound,
                y0=0,
                x1=split_bound+1,
                y1=1,
                fillcolor="DarkGray",
                opacity=0.5,
                layer="above",
                line_width=0)
            if idx >= len(seasons):
                continue
            fig.add_annotation(
                xref="x",
                yref="paper",
                showarrow=False,
                x=(split_bound + split_bounds[idx+1])/2,
                y=0.04*(idx%2),
                text=seasons[idx])

        with open(docs_path / f'{league}_elo.html', 'w') as div_file:
            div_file.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
        if not no_open:
            fig.show()
