import random
from objects.team import Team

class Fixture:
    def __init__(self, team1: Team = None, team2: Team = None, scores: [] = []) -> None:
        self.team1 = team1
        self.team2 = team2
        self.leg = 1 # implement as a counter
        self.agg_score = []
        # store leg scores in array
        self.scores = scores  # store scores as tuples, sum later for agg_score
        self.result = None
    
    def play_fixture(self) -> str:        
        if self.leg > 2 or len(self.scores) >= 2:
            raise Exception("Error: There cannot be more than 2 legs per fixture")

        # randomize score from 0-10 with weights for each result
        score_list = [0] * 20 + [1] * 20 + [2] * 20 + [3] * 20 + [4] * 20 + [5] * 3 + [6] * 3 + [7] * 1 + [8] * 1 + [9] * 1 + [10] * 1

        team1_score = random.choice(score_list)
        team2_score = random.choice(score_list)

        # update team attrs
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
        
        # store scores in list
        self.scores.append((team1_score, team2_score))

        # fixture outcome relative to home team
        self.result = str(team1_score) + "-" + str(team2_score)
        
        # compute aggr score
        t1_total = 0
        t2_total = 0
        for result in self.scores:
            t1_total += result[0]
            t2_total += result[1]
        
        self.agg_score = str(t1_total) + '-' + str(t2_total)
        
        self.leg += 1

        return self.result
    