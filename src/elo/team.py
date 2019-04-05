class Team(object):
    """A Professional League of Legends Team"""
    def __init__(self, abbrev, name, color, starting_rating=1500):
        self.abbrev = abbrev
        self.name = name
        self.color = color
        self.rating = int(starting_rating)
        self.rating_history = [self.rating]

    def updateRating(self, correction):
        self.rating += correction
        self.rating_history.append(self.rating)

    def __repr__(self):
        return "{}: {}".format(self.name, self.rating)
