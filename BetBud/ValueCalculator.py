# Import team average odds from HLTV Matchpage Average Team Odds
# Requires OOP - Needs to be part of a function or a class

# Value = (Probability * Decimal Odds) -1
# Probability is in decimal from 0 - 1 for example 50% is 0.5
# This entire EV section needs a rewrite to this formula (can probably hardcode to $1 bets for now):
# (Probability of Winning) x (Amount Won per Bet) – (Probability of Losing) x (Amount Lost per Bet)
def get_ev(team, model_probability, team_average_odds):
    ev_value = (model_probability * team_average_odds)
    print(team, ev_value)
    print("The value for {} based on current odds is {}".format(team, ev_value))
    return ev_value
# Example - team1_ev = get_ev(team1, team1_probability, team1_average_odds)
# Example - team2_ev = get_ev(team2, team2_probability, team2_average_odds)


# If your assessed probability (how often you think a team will win) in a certain game
# is higher than the implied probability the wager offers a value betting opportunity.
def get_implied_value(team):
    implied_probability = (1 / team.odds) * 100
    implied_probability = round(implied_probability, 2)
    print(team, implied_probability)
    print("The implied probability for {} based on current odds is {}%".format(team.name, implied_probability))
    return implied_probability
# Example - team1_implied_probability = get_implied_probability(team1, team1_average_odds)


# Find the average margin added by bookies - https://medium.com/@adamchernoff/using-margins-to-identify-real-sharp-money-925f62bdcfd1
def odds_margin(team1, team2):
    team1_true_odds = (1 / team1.odds)
    team2_true_odds = (1 / team2.odds)
    true_odds_total = team1_true_odds + team2_true_odds
    true_odds_total = round(true_odds_total, 2)
    true_odds_total_percent = round(true_odds_total, 2) * 100
    return true_odds_total_percent
    # margin = true_odds_total - 1
    # margin_percent = margin * 100
    # print("The margin for {} based on current odds is {}%".format(team1.name, margin))
    # print("The margin for {} based on current odds is {}%".format(team2.name, margin))
    # return margin, margin_percent


# Kelly Criterion the only (basic )thing needed to decide if its worth a bet
# Kelly Criterion to decide bet size (BP-Q) / B
# B = the Decimal odds (you are betting on) -1
# P = The probability of success in decimal (The % you predict)
# Q = the probability of failure (1 - P)
# Returns percentage of bank roll to wager in decimal 0 - 1 E.G 0.2 means wager 20% of your BR
# Needs try catch, possible to hit divide by 0 error in testing although unlikely in live environment
def kelly_criterion(team, probability):
    B = (team.odds - 1)
    P = probability
    Q = (1 - probability)
    kelly_criterion_result = (B * P - Q) / B
    kelly_criterion_result = round(kelly_criterion_result, 2)
    return kelly_criterion_result
# Example - kelly_criterion(team1_average_odds, probability)


# On call command to decide if you should be or not on a specific game
# If it takes in a command + matchpage it will be complex af best to leave it alone for now
# YOU NEED TO UNHARDCODE THIS - USE FUNCTIONS BETTER
# def bet_or_not():
#     if team1_value > 0:
#         print('Betting on {team1} might be a value bet as it is +{team1_value}EV'.format(team1, team1_value))
#     elif team1_value <= 0:
#         print('Betting on {team1} is not a value bet at -{team1_value}EV'.format(team1, team1_value))
#     elif team2_value > 0:
#             print('Betting on {team2} might be a value bet as it is +{team2_value}EV'.format(team2, team2_value))
#     elif team2_value <= 0:
#             print('Betting on {team2} is not a value bet at -{team2_value}EV'.format(team2, team2_value))
















