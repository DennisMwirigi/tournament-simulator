from objects.team import Team
from objects.fixture import Fixture

# creates and populates group
# creates group fixture list
# sorts group standings
class Group:
    def __init__(self, name: str, teams=None, fixtures=None):
        self.name = name
        self.team_list = teams if teams is not None else []
        self.fixture_list = fixtures if fixtures is not None else []
        
        if not isinstance(name, str):
            raise TypeError("Group name must be of type string")
        
        # when params are provided
        if teams is not None and len(teams) != 0:
            if any([not isinstance(x, Team) for x in teams]):
                raise TypeError("Invalid team in provided team list")
            if len(teams) != 4:
                raise Exception("Error: Each group must consist of 4 teams")
        
        if fixtures is not None and len(fixtures) != 0:
            if any([not isinstance(x, Fixture) for x in fixtures]):
                raise TypeError("Invalid fixture in provided fixture list")
            if len(fixtures) != 6:
                raise Exception("Error: Each team must play against every other team in the group")
    
    def add_team(self, T:Team):
        if not isinstance(T, Team):
            raise TypeError("Invalid team in provided team list")
        if len(self.team_list) >= 4:
            raise IndexError("Group consists of a maximum of 4 teams")
        
        self.team_list.append(T)
    
    def create_fixtures(self):        
        for i in range(0, len(self.team_list)-1):
            j = i+1
            
            while j<len(self.team_list):
                fixture = Fixture(self.team_list[i], self.team_list[j])
                self.fixture_list.append(fixture)
                
                j += 1

    # insertion sort by points, if equal points sort by goal difference
    def sort(self):
        n = len(self.team_list) # is always going to be 4
        
        for i in range(1, n):
            key = self.team_list[i]
            j = i-1
            
            while j>=0 and key.total_points() > self.team_list[j].total_points():
                if key.total_points() == self.team_list[j].total_points(): # check for GD
                    if key.goal_difference() > self.team_list[j].goal_difference():
                        self.team_list[j+1] = self.team_list[j]
 
                if key.total_points() > self.team_list[j].total_points():
                    self.team_list[j+1] = self.team_list[j]
                
                j -= 1
                
            self.team_list[j+1] = key