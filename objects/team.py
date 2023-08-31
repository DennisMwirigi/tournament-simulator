from player import Player

class Team:
    def __innit__(self, name:str, games_played:int = 0, goals_for:int = 0, goals_against:int = 0, games_won:int = 0, games_lost:int = 0, games_drawn:int = 0, roster:{Player} = None) -> None:
        self.name = name
        self.games_played = games_played
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.goal_difference = lambda: self.goals_for - self.goals_against
        self.games_won = games_won
        self.games_lost = games_lost
        self.games_drawn = games_drawn
        self.total_points = lambda: (self.games_won * 3) + self.games_drawn
        self.roster = roster
    
    def set_name(self, name:str):
        self.name = name
    
    def get_name(self):
        return self.name

    def get_games_played(self):
        return self.games_played

    def get_goals_for(self):
        return self.goals_for

    def get_goals_against(self):
        return self.goals_against

    def get_goal_difference(self):
        return self.goal_difference
    
    def get_games_won(self):
        return self.games_won
    
    def get_games_lost(self):
        return self.games_won
    
    def get_games_drawn(self):
        return self.games_drawn
    
    def get_total_points(self):
        return self.total_points
    
    def get_roster(self):
        return self.roster

    def won_game(self):
        self.games_won += 1
        self.games_played += 1
    
    def lost_game(self):
        self.games_lost += 1
        self.games_played += 1
    
    def drawn_game(self):
        self.games_drawn += 1
        self.games_played += 1
    
    def add_player(self, P:Player):
        self.roster.append(P)
    
    def remove_player(self, P:Player):
        if P in self.roster:
            self.roster.remove(P)
        else:
            print("Sorry, " + P.name + " does not play for " + self.name)
