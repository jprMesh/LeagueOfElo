class Team(object):
    """A Professional League of Legends Team"""
    def __init__(self, name, starting_rating=1500):
        self.name = name
        self.rating = starting_rating
        self.rating_history = [starting_rating]

    def updateRating(self, correction):
        self.rating += correction
        self.rating_history.append(self.rating)
