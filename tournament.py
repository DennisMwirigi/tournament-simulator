import random
from objects.team import Team
from objects.fixture import Fixture
from objects.group import Group
from objects.ko_stage import RO16, QfStage, SfStage

def main():
    # start off by listing the 32 teams to participate, for now store as pre set dictionary
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
            t.group = group.name # set team's group attribute
    
    # simulate group stage
    for group in Groups.values():
            group.create_fixtures()
    
    for group in Groups.values():
        leg = 1
        
        while leg <= 2:
            for fixture in group.fixture_list:
                fixture.play_fixture()
            leg += 1
    
    # display table
    for group in Groups.values():
        group.sort()
        
        print("Group " + group.name)
        print("----------------------------------------------------------------")
        print(f"Club\t\t   {'MP':<5} {'W':<5} {'D':<5} {'L':<5} {'GF':<5} {'GA':<5} {'GD':<5} Pts")
        print("----------------------------------------------------------------")
        
        pos = 1
        for team in group.team_list:
            print(f"{pos}. {team.name:<15} {team.games_played:<5} {team.games_won:<5} {team.games_drawn:<5} {team.games_lost:<5} {team.goals_for:<5} {team.goals_against:<5} {team.goal_difference():<5} {team.total_points()}")
            pos+=1
        print("----------------------------------------------------------------")       
        print()
    
    # choose teams to progress to ko stage 
    gs_winners = [group.det_prog_teams()["Winner"] for group in Groups.values()] 
    gs_runner_ups = [group.det_prog_teams()["Runner-up"] for group in Groups.values()]
      
    print("Progressing teams:")
    print("Winners:", [x.name for x in gs_winners])
    print("Runner-ups:", [x.name for x in gs_runner_ups])
    print()
    
    ro16_stage = RO16(prev_winners=gs_winners, runner_ups=gs_runner_ups)
    ro16_stage.create_fixtures()
    
    print()
    print("----------------------------------------------------------------")
    print("\t\t\tROUND OF 16")
    print("----------------------------------------------------------------")
    print("Round of 16 fixtures:")
    print([(x.team1.name, x.team2.name) for x in ro16_stage.fixture_list])
    print()
    
    ro16_stage.play_fixtures()
    
    print("Round of 16 winners:")
    print([x.name for x in ro16_stage.progressing_teams], end="")
    
    qf_stage = QfStage(prev_winners=ro16_stage.progressing_teams)
    qf_stage.create_fixtures()
    
    print()
    print("----------------------------------------------------------------")
    print("\t\t\tQUATER FINALS")
    print("----------------------------------------------------------------")
    print("Quater-final fixtures:")
    print([(x.team1.name, x.team2.name) for x in qf_stage.fixture_list])
    print()
    
    qf_stage.play_fixtures()
    
    print("Quater-final winners:")
    print([x.name for x in qf_stage.progressing_teams], end="")
    
    sf_stage = SfStage(prev_winners=qf_stage.progressing_teams)
    sf_stage.create_fixtures()
    
    print()
    print("----------------------------------------------------------------")
    print("\t\t\tSEMI FINALS")
    print("----------------------------------------------------------------")
    print("Semi-final fixtures:")
    print([(x.team1.name, x.team2.name) for x in sf_stage.fixture_list])
    print()
    
    sf_stage.play_fixtures()
    
    print("Semi-final losers:")
    print([x.name for x in sf_stage.losers()])
    print()
    
    print("Semi-final winners:")
    print([x.name for x in sf_stage.progressing_teams])
    print()
    
    # play 3rd place playoff
    third_place_playoff = Fixture(team1=sf_stage.losers()[0], team2=sf_stage.losers()[1])
    
    result = third_place_playoff.play_final()
    
    third_place_team = third_place_playoff.team1 if result[0] > result[1] else third_place_playoff.team2
    
    # play final game
    final_game = Fixture(team1=sf_stage.progressing_teams[0], team2=sf_stage.progressing_teams[1])
    
    final_result = final_game.play_final()
    
    winner = final_game.team1 if final_result[0] > final_result[1] else final_game.team2
    runner_up = final_game.team1 if final_result[0] < final_result[1] else final_game.team2
    
    print()
    print("----------------------------------------------------------------")
    print("\t\t  TOURNAMENT STANDINGS")
    print("----------------------------------------------------------------")
    
    print("3rd placed team is:\t", third_place_team.name, "! ! ! !")
    print()
    
    print("2nd place team is:\t", runner_up.name, "! ! ! ! !")
    print("\n\n")
    
    print("\t     AND THE TOURNAMENT WINNER IS")
    print("\n")
    print("\t     ! ! ! ! ", winner.name.upper(), "! ! ! ! !")


if __name__ == '__main__':
    main()
