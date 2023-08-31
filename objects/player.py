from team import Team

class Player:
    def __init__(self, name:str, team:Team = None, position:str = None, goals:int = 0, assists:int = 0, clean_sheets:int = 0) -> None:
        self.name = name # play with typing; self.name:str sets name to str even in methods?
        self.team = team
        self.position = position
        self.goals = goals
        self.assists = assists
        self.clean_sheets = clean_sheets

    def set_team(self, team:str):
        self.team = team

    def set_name(self, name:str):
        self.name = name
    
    def set_position(self, position:str):
        self.position = position
    
    def get_team(self):
        return self.team

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position
    
    def scored(self):
        self.goals += 1
    
    def assisted(self):
        self.assists += 1
    
    def clean_sheet(self):
        self.clean_sheets += 1
