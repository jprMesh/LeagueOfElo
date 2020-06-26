<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
<style type="text/css">
    .main-content {
        max-width: 90rem;
    }
</style>

# Fundamentals

Elo is a rating system developed to rate chess players, but it's a good system for rating players or teams in any zero-sum game. League of Legends is a zero sum game because there is always a winner and a loser, so it should work for League as well.

The implementation of this model is based on [FiveThirtyEight's NFL team elo rating system model](https://fivethirtyeight.com/methodology/how-our-nfl-predictions-work/). There are two key points to note here:
1. For each match, the model generates a prediction and the teams gain or lose points based on how correct the model was. Because predicting match outcomes is integral to the model, it tunes itself over time to predict matches as optimally as possible.
2. Teams all start out at a 1500 rating. In between seasons, teams ratings regress 25% toward the mean (1500) to adjust for any changes in roster, meta, coaching, etc. It also tells the model that there is more uncertainty at the beginning of each new season.

The model makes predictions about how likely a team is to take victory over another team based on the following formula that takes into account Team 1's rating $$T_1$$ and Team 2's rating $$T_2$$.

$$
P(T_1) = \frac{1} {10^ {\frac{-(T_1 - T_2)} {400}} + 1}
$$

The prediction is expressed as a probability that one team beats the other, with the opposite being true for the other team in the match. After the match concludes, the model will calculate an adjustment value based on its earlier prediction and a few other factors, which will be discussed later. The winning team gains the adjustment value to its rating, and the losing team loses that many points. The formula for the adjustment value is 

$$
Adj = KM(1-P(T_W))
$$

where $$K$$ is a fixed parameter in the model, $$M$$ is the match score adjustment, and $$T_W$$ is the winning team.

## K Parameter

The main parameter to be tuned in an elo model is the K parameter, which determines relatively how much a team will gain or lose from winning or losing a game. A higher K parameter causes the model to be more volatile and bias more toward recent results over long-term standing.

In traditional sports, baseball models use a low K because there's more variability and more games in a season, so long-term results are more indicative of a team's overall skill than short-term results. Football on the other hand uses a higher K value because there are fewer games in a season and each game im more important and there's less variability. Similar to football, the League of Legends leagues have few games in a season, so the ratings need to react quickly.

## Brier Scores

A Brier score is a metric of how accurate the model's predictions are. The formula for a Brier score for one prediction is $$B = (1 - P(T_W))^2$$. So if a model predicts that a matchup is a 50-50 tossup, the Brier score will be 0.25 no matter the outcome. Better predictions will yield lower Brier scores, so the goal in calibrating the model is to make the average Brier score as low as possible.

Brier scores were added to the model to calibrate for the optimal K parameter. This optimal value turned out to be about 30, which is a pretty high K parameter and is actually the exact same K parameter used by 538 in their NFL model.

# Model Specifics

A few minor changes were made to the base elo model to adjust for the nature of the leagues being modeled.

## Match Score Adjustment

Many matches in playoffs and in some regions' regular season games are played as a best-of-X format, where teams play multiple games and the first team to win a majority of the allotted games wins the match. In these cases, we want to adjust the rating change based on how dominant the victory was. The formula for the modifier is

$$
M = \left( \frac{W(W-L)} {W+L} \right) ^{0.7}
$$

where the *W* is the winner's match score and *L* is the loser's match score. What this effectively means is that a team that wins a match 3-0 will gain *2.15x* what they would have otherwise gained for a single game victory. A 3-1 victory would yield a *1.33x* modifier, and a 3-2 victory yields a *0.70x* modifier. This compensates teams appropriately for being more or less dominant than expected.

## Alignment

Since some teams play more games than others due to playoffs and tiebreakers, the model has an alignment mechanism to fill forward the ratings of the teams that haven't played as many games as others, this lets the graph show more accurate picture of the ratings through time.

# League Models

The following charts shows the Elo ratings of teams over time. Any team renamings/rebrands show the most recent name for the entire team history. The legend on the right of each chart shows the most recent rating for each team and separates the currently active teams from the inactive teams. The zoom tool allows closer inspection of sections of the graph by clicking and dragging around the area of interest. It should be noted that predictions in LCK and LPL are generally better because they use Bo3s in their regular season rather than Bo1s.

International competitions have an interesting way of modifying a whole region's overall rating due to the zero-sum aspect of Elo rating system. Teams that improve their rating will take that point gain back to their regional league, while teams whose ratings drop will take that loss back to their regional league. Effectively, the winning regions steal points from the losing regions, which accumulates over time into some regions having higher averages than others.

## Global

{% include_relative NA_EU_KR_CN_INT_elo.html %}

## LCS

{% include_relative NA_elo.html %}

## LEC

{% include_relative EU_elo.html %}

## LCK

Of note here is that the LCK regular season uses Bo3s rather than Bo1s.

{% include_relative KR_elo.html %}

## LPL

The LPL also uses Bo3s in the regular season.

{% include_relative CN_elo.html %}

---

Big thanks to [Leaguepedia](https://lol.gamepedia.com/Help:API_Documentation) for maintaining databases with all the data used here!
