from team import Team
from fixture import Fixture

# creates and populates group
# creates group fixture list
# sorts group standings
class Group:
    def __init__(self, teams:{Team} = None, group_table:{Team} = None, fixtures:{Fixture} = None) -> None:
        self.teams = teams
        self.group_table = group_table
        self.fixture_list = fixtures
    
    def add_team(self, T:Team):
        self.teams.append(T)
    
    def create_fixtures(self):
        teams = self.teams
    
    def sort(self):
        table = self.group_table

'''
*** goes in actual tourna simulator 
simulates running of group stage which includes:
    - playing fixtures
    - determining which teams progress to next stage
        - top 2 teams of each group
        - if teams no. 2 & 3 have the same points & gd -> play playoff fixture
'''
class GroupStage:
    def __init__(self, groups:{Group} = None) -> None:
        self.groups = groups
    
    def add_groups(self, G:Group):
        self.groups.append(G)