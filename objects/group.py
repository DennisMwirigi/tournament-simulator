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
            # no duplicates
            for i in range(len(teams)-1):
                j = i+1
                
                while j<len(teams):
                    if teams[i] == teams[j]:
                        raise Exception("Group cannot contain duplicate teams")
                    j+=1
        
        if fixtures is not None and len(fixtures) != 0:
            if any([not isinstance(x, Fixture) for x in fixtures]):
                raise TypeError("Invalid fixture in provided fixture list")
            if len(fixtures) != 6:
                raise Exception("Error: Not enough fixtures for group games")
            if len(fixtures) == 6:
                # teams must be from team_list
                fixture_teams = []
                for x in fixtures:
                    if x.team1 not in fixture_teams:
                        fixture_teams.append(x.team1)
                    if x.team2 not in fixture_teams:
                        fixture_teams.append(x.team2)
                
                if not all(x in teams for x in fixture_teams):
                    raise Exception("Error: Each team must play against every other team in the group")
                
            # no duplicates
            for i in range(len(fixtures)-1):
                j = i+1
                
                while j<len(fixtures):
                    if fixtures[i] == fixtures[j]:
                        raise Exception("Group cannot contain duplicate fixtures")
                    j+=1
    
    def add_team(self, T:Team):
        if not isinstance(T, Team):
            raise TypeError("Invalid team provided")
        if len(self.team_list) >= 4:
            raise IndexError("Group consists of a maximum of 4 teams")
        if T in self.team_list:
            raise Exception("Group cannot contain duplicate teams")
        
        self.team_list.append(T)
    
    def create_fixtures(self):        
        for i in range(len(self.team_list)-1):
            j = i+1
            
            while j<len(self.team_list):
                fixture = Fixture(self.team_list[i], self.team_list[j])
                self.fixture_list.append(fixture)
                
                j += 1

    # insertion sort by points, if equal points sort by goal difference
    def sort(self):        
        for i in range(1, len(self.team_list)):
            j = i
            
            while j > 0:
                if self.team_list[j-1].total_points() < self.team_list[j].total_points():
                    next = self.team_list[j-1]
                    self.team_list[j-1] = self.team_list[j]
                    self.team_list[j] = next
                    
                if self.team_list[j-1].total_points() == self.team_list[j].total_points(): # check for GD
                    if self.team_list[j-1].goal_difference() < self.team_list[j].goal_difference():
                        next = self.team_list[j-1]
                        self.team_list[j-1] = self.team_list[j]
                        self.team_list[j] = next
                
                j -= 1
    
    # determine top 2 teams to progress out of the group stage
    # return winner and runner-up in dict
    def det_prog_teams(self) -> dict:
        outcome = {"Winner": self.team_list[0], "Runner-up": self.team_list[1]}
        
        # if teams no. 2 & 3 have the same points & gd -> play winning playoff fixture
        if self.team_list[1].total_points() == self.team_list[2].total_points() and self.team_list[1].goal_difference() == self.team_list[2].goal_difference():
            playoff = Fixture(team1=self.team_list[1], team2=self.team_list[2])
            result = playoff.play_final()
            
            if result[1] > result[0]:
                outcome["Runner-up"] = self.team_list[2]
        
        return outcome