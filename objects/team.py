class Team:
    def __init__(self, name: str, games_played: int = 0, goals_for: int = 0, goals_against: int = 0, games_won: int = 0, games_lost: int = 0, games_drawn: int = 0):
        self.name = name
        self.games_played = games_played
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.goal_difference = lambda: self.goals_for - self.goals_against
        self.games_won = games_won
        self.games_lost = games_lost
        self.games_drawn = games_drawn
        self.total_points = lambda: (self.games_won * 3) + self.games_drawn

    def won_game(self):
        self.games_won += 1
        self.games_played += 1

    def lost_game(self):
        self.games_lost += 1
        self.games_played += 1

    def drawn_game(self):
        self.games_drawn += 1
        self.games_played += 1
