class Team(object):
    """A Professional League of Legends Team"""
    def __init__(self, abbrev, name, color="#000000", starting_rating=1500):
        self.abbrev = abbrev
        self.name = name
        self.color = color
        self.rating = int(starting_rating)
        self.rating_history = [[self.rating]]
        self.games_played = 0
        self.inactive = False

    def updateRating(self, correction):
        self.rating += correction
        self.rating_history[-1].append(self.rating)
        self.games_played += 1

    def __repr__(self):
        return "{}: {}".format(self.name, self.rating)
