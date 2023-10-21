import random
from objects.team import Team

class Fixture:
    def __init__(self, team1: Team, team2: Team, leg: int = 1, agg_score = None, scores = None) -> None:
        self.team1 = team1
        self.team2 = team2
        self.leg = leg # implement as a counter
        self.agg_score = agg_score if agg_score is not None else ()
        # store leg scores in array
        self.scores = scores if scores is not None else []  # store scores as tuples, sum later for agg_score
        self.result = None
        
        if not isinstance(team1, Team) and not isinstance(team2, Team):
            raise TypeError("team attribute must be of type " + str(Team))
        if not isinstance(leg, int):
            raise TypeError("leg attribute must be of type int")
        if agg_score is not None and not isinstance(agg_score, tuple):
            raise TypeError("aggregate score attribute must be of type tuple")
        if scores is not None and not isinstance(scores, list):
            raise TypeError("scores attribute must be of type list")
        if leg < 1:
            raise Exception("Cannot have a fixture with less than one leg")
    
    def play_fixture(self) -> str:        
        if self.leg > 2 or len(self.scores) >= 2:
            raise Exception("Error: There cannot be more than 2 legs per fixture")

        # randomize score from 0-10 with weights for each result
        score_list = [0] * 20 + [1] * 20 + [2] * 20 + [3] * 20 + [4] * 20 + [5] * 3 + [6] * 3 + [7] * 1 + [8] * 1 + [9] * 1 + [10] * 1

        team1_score = random.choice(score_list)
        team2_score = random.choice(score_list)
        
        # store scores in list
        self.scores.append((team1_score, team2_score))

        # fixture outcome relative to home team
        self.result = str(team1_score) + "-" + str(team2_score)
        
        # update team attrs
        self.update_team_attrs(team1_score, team2_score)
        
        # compute aggr score
        self.compute_agg_score()
        
        self.leg += 1 

        return self.result
    
    def update_team_attrs(self, team1_score: int, team2_score: int) -> None:
        self.team1.goals_for += team1_score
        self.team1.goals_against += team2_score

        self.team2.goals_for += team2_score
        self.team2.goals_against += team1_score
        
        if team1_score == team2_score:
            self.team1.drawn_game()
            self.team2.drawn_game()

        if team1_score > team2_score:
            self.team1.won_game()
            self.team2.lost_game()

        if team1_score < team2_score:
            self.team1.lost_game()
            self.team2.won_game()
    
    def compute_agg_score(self) -> None:
        t1_total = 0
        t2_total = 0
        for result in self.scores:
            t1_total += result[0]
            t2_total += result[1]
        
        self.agg_score = (t1_total, t2_total)
    
    def play_final(self) -> None:
        # randomize score from 0-10 with weights for each result
        score_list = [0] * 20 + [1] * 20 + [2] * 20 + [3] * 20 + [4] * 20 + [5] * 3 + [6] * 3 + [7] * 1 + [8] * 1 + [9] * 1 + [10] * 1
        
        scores = [None, None]
        # cannot end in a draw
        while scores[0] == scores[1]:
            scores = random.choices(population=score_list, k=2)
        
        team1_score = scores[0]
        team2_score = scores[1]
        
        # fixture outcome relative to home team
        self.result = str(team1_score) + "-" + str(team2_score)

        return self.result