import random
from objects.team import Team
from objects.fixture import Fixture
from objects.group import Group

def main():
    # start off by listing the 32 teams to participate, for now store as pre set enums
    Teams = {
        "United": Team("United"),
        "Chelsea": Team("Chelsea"),
        "Liverpool": Team("Liverpool"),
        "Arsenal": Team("Arsenal"),
        "Barcelona": Team("Barcelona"),
        "Madrid": Team("Madrid"),
        "Atletico": Team("Atletico"),
        "Sevilla": Team("Sevilla"),
        "Bayern": Team("Bayern"),
        "Dortmund": Team("Dortmund"),
        "Schalke": Team("Schalke"),
        "Berlin": Team("Berlin"),
        "PSG": Team("PSG"),
        "Monaco": Team("Monaco"),
        "Marseille": Team("Marseille"),
        "Lyon": Team("Lyon"),
        "Benfica": Team("Benfica"),
        "Porto": Team("Porto"),
        "Milan": Team("Milan"),
        "Inter": Team("Inter"),
        "Napoli": Team("Napoli"),
        "Lazio": Team("Lazio"),
        "Feyenoord": Team("Feyenoord"),
        "Galatasary": Team("Galatasaray"),
        "Salzburg": Team("Salzburg"),
        "Ajax": Team("Ajax"),
        "Olympiacos": Team("Olympiacos"),
        "Celtic": Team("Celtic"),
        "Spoting": Team("Sporting"),
        "Harambee": Team("Harambee"),
        "Gorge": Team("Gorge"),
        "Whitecaps": Team("Whitecaps")
    }
    
    # randomize into 8 groups of 4 teams
    Groups = {
        "A": Group(name="A"),
        "B": Group(name="B"),
        "C": Group(name="C"),
        "D": Group(name="D"),
        "E": Group(name="E"),
        "F": Group(name="F"),
        "G": Group(name="G"),
        "H": Group(name="H")
    }
    
    teams = list(Teams.values())

    while len(teams) > 0:
        for group in Groups.values():
            index = random.randrange(len(teams))
            t = teams[index]
            teams.pop(index)
            group.add_team(t)
    
    # simulate group stage
    for group in Groups.values():
            group.create_fixtures()
    
    for group in Groups.values():
        leg = 1
        
        while leg <= 2:
            for fixture in group.fixture_list:
                fixture.play_fixture()
            leg += 1
    
    for group in Groups.values():
        group.sort()
        
        # display table -> make func, add formatting
        print(group.name)
        
        for team in group.team_list:
            print(team.name, team.games_played, team.games_won, team.games_drawn, team.games_lost, team.goals_for, team.goals_against, team.goal_difference(), team.total_points())               
        print()
    
    # choose teams to progress to ko stage
    # if Groups["A"].team_list[1].total_points() == Groups["A"].team_list[2].total_points() and Groups["A"].team_list[1].goal_difference() == Groups["A"].team_list[2].goal_difference():
    # play playoff fixture, winner progresses
    playoff = Fixture(team1=Groups["A"].team_list[1], team2=Groups["A"].team_list[2])
    
    # cannot be a draw
    
    print(playoff.play_final())
        
# '''
# *** goes in actual tourna simulator 
# simulates running of group stage which includes:
#     - playing fixtures
#     - determining which teams progress to next stage
#         - top 2 teams of each group
#         - if teams no. 2 & 3 have the same points & gd -> play winning playoff fixture -> randomizer may come out as a draw, need a win
# '''
# class GroupStage:
#     def __init__(self, groups:{Group} = None) -> None:
#         self.groups = groups
    
#     def add_groups(self, G:Group):
#         self.groups.append(G)

if __name__ == '__main__':
    main()
