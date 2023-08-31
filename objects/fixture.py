from team import Team

class Fixture:
    def __init__(self, id:str, home_team:Team = None, away_team:Team = None, leg:int = 0, agg_score:str = None, score:str = None, outcome:str = None) -> None:
        self.id = id
        self.home_team = home_team
        self.away_team = away_team
        self.leg = leg
        self.agg_score = agg_score # needs to be lamda func combining scores from the 2 legs played
        self.score = score # parse str to get home & away team goals. home goals always comes first i.e. 5-3, home team score = 5, away = 3
        self.outcome = outcome # win, lose or draw relative to home team - work with score parsing
