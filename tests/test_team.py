import pytest
from objects.team import Team

def test_init_with_name():
    team = Team("united")
    assert team.name == "united"
    assert team.games_played == 0
    assert team.goals_for == 0
    assert team.goals_against == 0
    assert team.goal_difference() == 0
    assert team.games_won == 0
    assert team.games_lost == 0
    assert team.games_drawn == 0
    assert team.total_points() == 0

def test_init_no_name():
    with pytest.raises(Exception):
        team = Team()

def test_init_invalid_sum_games_played():
    with pytest.raises(Exception) as exc_info:
        team = Team("united", 2, 4, 3, 1, 1, 1)
    assert str(exc_info.value) == "Total games played must equal sum of games won, lost and drawn"

def test_init_negative_values():
    with pytest.raises(Exception) as exc_info1:
        team = Team("united", -1)
    assert str(exc_info1.value) == "Goals for and against, games played, won, lost, and drawn cannot have negative values"
    
    with pytest.raises(Exception) as exc_info2:
        team = Team("united", 0, -1)
    assert str(exc_info2.value) == "Goals for and against, games played, won, lost, and drawn cannot have negative values"
    
    with pytest.raises(Exception) as exc_info3:
        team = Team("united", 0, 0, -1)
    assert str(exc_info3.value) == "Goals for and against, games played, won, lost, and drawn cannot have negative values"
    
    with pytest.raises(Exception) as exc_info4:
        team = Team("united", 0, 0, 0, -1)
    assert str(exc_info4.value) == "Goals for and against, games played, won, lost, and drawn cannot have negative values"
    
    with pytest.raises(Exception) as exc_info5:
        team = Team("united", 0, 0, 0, 0, -1)
    assert str(exc_info5.value) == "Goals for and against, games played, won, lost, and drawn cannot have negative values"
    
    with pytest.raises(Exception) as exc_info6:
        team = Team("united", 0, 0, 0, 0, 0, -1)
    assert str(exc_info6.value) == "Goals for and against, games played, won, lost, and drawn cannot have negative values"

def test_init_invalid_param_types():
    with pytest.raises(TypeError) as t_err1:
        team = Team(1)
    assert str(t_err1.value) == "Team name must be of type string"
    
    with pytest.raises(TypeError) as t_err2:
        team = Team("united", 1.79)
    assert str(t_err2.value) == "All team attributes other than name must be of type int"
    
    with pytest.raises(TypeError) as t_err3:
        team = Team("united", 0, ("tuple"))
    assert str(t_err3.value) == "All team attributes other than name must be of type int"
    
    with pytest.raises(TypeError) as t_err4:
        team = Team("united", 0, 0, "str")
    assert str(t_err4.value) == "All team attributes other than name must be of type int"
    
    with pytest.raises(TypeError) as t_err5:
        team = Team("united", 0, 0, 0, ["list"])
    assert str(t_err5.value) == "All team attributes other than name must be of type int"
    
    with pytest.raises(TypeError) as t_err6:
        team = Team("united", 0, 0, 0, 0, {"A":"dict"})
    assert str(t_err6.value) == "All team attributes other than name must be of type int"
    
    with pytest.raises(TypeError) as t_err7:
        team = Team("united", 0, 0, 0, 0, 0, {'set'})
    assert str(t_err7.value) == "All team attributes other than name must be of type int"

def test_init_valid_params():
    team = Team("united", 3, 5, 6, 1, 1, 1)
    assert team.name == "united"
    assert team.games_played == 3
    assert team.goals_for == 5
    assert team.goals_against == 6
    assert team.goal_difference() == -1
    assert team.games_won == 1
    assert team.games_lost == 1
    assert team.games_drawn == 1
    assert team.total_points() == 4

def test_won_game():
    team = Team("united")
    team.won_game()
    assert team.games_played == 1
    assert team.games_won == 1
    assert team.total_points() == 3

def test_lost_game():
    team = Team("united")
    team.lost_game()
    assert team.games_played == 1
    assert team.games_lost == 1
    assert team.total_points() == 0

def test_drawn_game():
    team = Team("united")
    team.drawn_game()
    assert team.games_played == 1
    assert team.games_drawn == 1
    assert team.total_points() == 1