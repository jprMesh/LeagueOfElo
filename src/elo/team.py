import numpy as np


class Team(object):
    """A Professional League of Legends Team"""
    def __init__(self, team_id, abbrev, name, color="#868686", starting_rating=1500):
        self.team_id = team_id
        self.abbrev = abbrev
        self.name = name
        self.names = [name, abbrev]
        self.color = color
        self.team_rating = int(starting_rating)
        self.rating_history = [[self.team_rating]]
        self.games_played = 0
        self.inactive = False

    def getRating(self):
        return self.team_rating

    def updateRating(self, correction):
        self.team_rating += correction
        self.rating_history[-1].append(self.team_rating)
        self.games_played += 1

    def __repr__(self):
        return "{}: {}".format(self.name, self.team_rating)


class DummyTeam(Team):
    """
    A dummy team that always has the given rating and doesn't change.
    Can be used as a proxy opponent when playing against unknown teams.
    """
    def __init__(self, starting_rating=1500):
        super().__init__(-1, None, 'DummyTeam', None, starting_rating)

    def updateRating(self, correction):
        pass


class PlayerTeam(Team):
    """A Professional League of Legends Team"""
    def __init__(self, team_id, abbrev, name, color="#000000", starting_rating=1500):
        super().__init__(team_id, abbrev, name, color, starting_rating)
        self.top = []
        self.jng = []
        self.mid = []
        self.bot = []
        self.sup = []

    def __repr__(self):
        team_string = f"{self.name}: {self.team_rating}\n\t"
        team_string += f"top: {self.top}\n\t"
        team_string += f"jng: {self.jng}\n\t"
        team_string += f"mid: {self.mid}\n\t"
        team_string += f"bot: {self.bot}\n\t"
        team_string += f"sup: {self.sup}\n\t"
        return team_string

    def clearRoster(self):
        self.top = []
        self.jng = []
        self.mid = []
        self.bot = []
        self.sup = []

    def addPlayer(self, role, player):
        if role == 'Top Laner':
            self.top.append(player)
        if role == 'Jungler':
            self.jng.append(player)
        if role == 'Mid Laner':
            self.mid.append(player)
        if role == 'Bot Laner':
            self.bot.append(player)
        if role == 'Support':
            self.sup.append(player)

    def getRating(self):
        rating = (
            0.25 * self.team_rating +
            0.15 * np.average(list(map(Player.getRating, self.top))) +
            0.15 * np.average(list(map(Player.getRating, self.jng))) +
            0.15 * np.average(list(map(Player.getRating, self.mid))) +
            0.15 * np.average(list(map(Player.getRating, self.bot))) +
            0.15 * np.average(list(map(Player.getRating, self.sup))))
        return rating

    def updateRating(self, correction):
        super(PlayerTeam, self).updateRating(correction)
        for player in self.top + self.jng + self.mid + self.bot + self.sup:
            player.updateRating(correction)


class Player(object):
    """A Professional League of Legends Player"""
    def __init__(self, name, starting_rating=1500):
        self.name = name
        self.names = [name]
        self.rating = int(starting_rating)
        self.rating_history = [[self.rating]]
        self.games_played = 0
        self.inactive = False

    def getRating(self):
        return self.rating

    def updateRating(self, correction):
        self.rating += correction
        self.rating_history[-1].append(self.rating)
        self.games_played += 1

    def __repr__(self):
        return "{}: {}".format(self.name, self.rating)
