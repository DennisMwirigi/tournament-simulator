import random
from team import Team

class Fixture:
    def __init__(self, id:str, home_team:Team = None, away_team:Team = None, leg:int = 0, agg_score:str = None, score:str = None, outcome:str = None) -> None:
        self.id = id # same fixture can be played twice (legs), how to deal wuth that?
        self.home_team = home_team
        self.away_team = away_team
        self.leg = leg
        self.agg_score = agg_score # needs to be lamda func combining scores from the 2 legs played
        self.score = score # parse str to get home & away team goals. home goals always comes first i.e. 5-3, home team score = 5, away = 3
        self.outcome = outcome # win, loss or draw relative to home team - work with score parsing
    
    def play_fixture(self) -> str:
        # randomize score from 1-10 with weights for each team
        score_list = [0] * 6 + [1] * 6 + [2] * 6 + [3] * 6 + [4] * 6 + [5] * 2 + [6] * 2 + [7] * 1 + [8] * 1 + [9] * 1 + [10] * 1
        
        home_score = random.choice(score_list) 
        away_score = random.choice(score_list)
        
        # update team attrs
        self.home_team.goals_for = self.home_team.goals_for + home_score
        self.home_team.goals_against = self.home_team.goals_against + away_score
        
        self.away_team.goals_for = self.away_team.goals_for + away_score
        self.away_team.goals_against = self.away_team.goals_against + home_score
        
        # fixture outcome relative to home team
        self.score = str(home_score) + "-" + str(away_score)
        
        if home_score == away_score:
            self.outcome = "Draw"
            self.home_team.drawn_game()
            self.away_team.drawn_game()
            
        if home_score > away_score:
            self.outcome = "Win"
            self.home_team.won_game()
            self.away_team.lost_game()
            
        if home_score < away_score:
            self.outcome = "Loss"
            self.home_team.lost_game()
            self.away_team.won_game()

'''
2 legs ????
'''