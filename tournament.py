from objects.team import Team
from objects.fixture import Fixture

def main():
    team1 = Team('united')
    team2 = Team('chelsea')
    
    # simulating 2 legs
    fixt = Fixture(team1, team2)
    
    games = 0
    while games < 2:
        games += 1
        
        print("leg", fixt.leg, "\nscore =", fixt.play_fixture(), "\nagg score =", fixt.agg_score)
        print()
        
        # check team attrs are working correctly
        print("team 1 attrs:")
        print("P:", team1.games_played, "GF:", team1.goals_for, "GA:", team1.goals_against, "GD:", team1.goal_difference())
        print("Won:", team1.games_won, "Drawn:", team1.games_drawn, "Lost:", team1.games_lost)
        print("Total points:", team1.total_points())
        
        print()
        
        print("team 2 attrs:")
        print("P:", team2.games_played, "GF:", team2.goals_for, "GA:", team2.goals_against, "GD:", team2.goal_difference())
        print("Won:", team2.games_won, "Drawn:", team2.games_drawn, "Lost:", team2.games_lost)
        print("Total points:", team2.total_points())
        
        print()
    
    team3 = Team('arsenal', 0, 0, 0, 0, -1, 0)



if __name__ == '__main__':
    main()
