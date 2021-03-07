from abc import ABC, abstractmethod


class RatingSystem(ABC):
    """Abstract rating system class"""
    def __init__(self):
        self.brier = []
        self.up_down = []

    @abstractmethod
    def predict(self, t1_rating:int, t2_rating:int):
        """
        @brief Get the probability that team1 will beat team2.
        @return win probability between 0 and 1.
        """
        pass

    @abstractmethod
    def process_outcome(self, t1_rating:int, t2_rating:int, t1_score:int, t2_score:int):
        """
        @brief Process the outcome of a match.
        @return Rating adjustments for t1 and t2, sequentially.
        """
        pass

    def getBrier(self):
        brier = sum(self.brier)/len(self.brier)
        return f"Brier Score: {brier:.4f}"

    def getUpDown(self):
        up = sum(self.up_down)
        down = len(self.up_down) - up
        pct = up/(up+down)*100
        return f"Up Down Record: {up} - {down} ({pct:.2f}%)"


class Elo(RatingSystem):
    """Elo rating system"""
    def __init__(self, K=30, score_mult=True):
        super().__init__()
        self.K = K
        self.score_mult = score_mult

    def predict(self, t1_rating:int, t2_rating:int):
        rating_diff = t1_rating - t2_rating
        win_prob = 1 / (10**(-rating_diff/400) + 1)
        return win_prob

    def process_outcome(self, t1_rating:int, t2_rating:int, t1_score:int, t2_score:int):
        def score_multiplier(wr, lr):
            if wr == lr:
                return 0.25
            return ((wr-lr)*wr/(wr+lr))**0.7

        def process_winner(winner_rating, loser_rating, winner_score, loser_score):
            forecast_delta = 1 - self.predict(winner_rating, loser_rating)
            self.up_down.append(forecast_delta < .5)
            self.brier.append(forecast_delta**2)
            match_score_mult = 1 if not self.score_mult else score_multiplier(winner_score, loser_score)
            rating_delta = self.K * forecast_delta * match_score_mult
            return (rating_delta, -rating_delta)

        # In a tie, the lower ranked team is considered the winner.
        if t1_score > t2_score or (t1_score == t2_score and t1_rating < t2_rating):
            t1, t2 = process_winner(t1_rating, t2_rating, t1_score, t2_score)
        else:
            t2, t1 = process_winner(t2_rating, t1_rating, t2_score, t1_score)
        return (t1, t2)


class Naive(RatingSystem):
    """Naive rating system will always predict 100% chance of higher rated team winning"""
    def __init__(self, K=5):
        super().__init__()
        self.K = K

    def predict(self, t1_rating:int, t2_rating:int):
        return int(t1_rating > t2_rating)

    def process_outcome(self, t1_rating:int, t2_rating:int, t1_score:int, t2_score:int):
        def process_winner(winner_rating, loser_rating, winner_score, loser_score):
            forecast_delta = 1 - self.predict(winner_rating, loser_rating)
            self.up_down.append(forecast_delta < .5)
            self.brier.append(forecast_delta**2)
            return (self.K * forecast_delta, -self.K * forecast_delta)

        if t1_score > t2_score or (t1_score == t2_score and t1_rating < t2_rating):
            t1, t2 = process_winner(t1_rating, t2_rating, t1_score, t2_score)
        else:
            t2, t1 = process_winner(t2_rating, t1_rating, t2_score, t1_score)
        return (t1, t2)


