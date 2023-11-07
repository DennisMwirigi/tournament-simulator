import pytest
from objects.fixture import Fixture
from objects.team import Team
from unittest import mock

team1 = Team("team1")
team2 = Team("team2")
    
def test_init_with_teams():
    fixt = Fixture(team1, team2)
    assert fixt.team1 == team1
    assert fixt.team2 == team2
    assert fixt.leg == 1
    assert fixt.agg_score == ()
    assert fixt.scores == []
    assert fixt.result == None

def test_init_no_teams():
    with pytest.raises(TypeError):
        fixt = Fixture()
        
    with pytest.raises(TypeError):   
        fixt = Fixture(team1)

def test_init_invalid_param_types():
    with pytest.raises(TypeError) as t_err1:
        fixt = Fixture("", "")
    assert str(t_err1.value) == "team attribute must be of type " + str(Team)
    
    with pytest.raises(TypeError) as t_err2:
        fixt = Fixture(team1, team2, "str")
    assert str(t_err2.value) == "leg attribute must be of type int"
    
    with pytest.raises(TypeError) as t_err3:
        fixt = Fixture(team1, team2, 1, 3)
    assert str(t_err3.value) == "aggregate score attribute must be of type tuple"
    
    with pytest.raises(TypeError) as t_err4:
        fixt = Fixture(team1, team2, 1, (5, 3), {"a": "dict"})
    assert str(t_err4.value) == "scores attribute must be of type list"

def test_init_negative_leg_value():
    with pytest.raises(Exception) as exc_info:
        fixt = Fixture(team1, team2, -1)
    assert str(exc_info.value) == "Cannot have a fixture with less than one leg"

def test_init_play_self():
    with pytest.raises(Exception) as e_info:
        fixt = Fixture(team1=team1, team2=team1)
    assert str(e_info.value) == "Team cannot play against itself"

def test_init_valid_params():
    fixt = Fixture(team1, team2, 2, (5, 3), [(2, 1), (3, 2)])
    assert fixt.team1 == team1
    assert fixt.team2 == team2
    assert fixt.leg == 2
    assert fixt.agg_score == (5, 3)
    assert fixt.scores == [(2, 1), (3, 2)]
    assert fixt.result == None

def test_equality():
    team_1 = Team("United")
    team_2 = Team("Chelsea")
    team_3 = Team("Arsenal")
    
    fixt1 = Fixture(team_1, team_2)
    fixt2 = Fixture(team_1, team_2)
    fixt3 = Fixture(team_1, team_3)
    fixt4 = Fixture(team_2, team_3)
    
    assert fixt1 == fixt2
    assert fixt2 != fixt3 # same 1st team, different 2nd
    assert fixt2 != fixt4 # different 1st and 2nd team
    assert fixt3 != fixt4 # different 1st, same 2nd

def test_play_fixture_exception():
    # case 1: self.leg > 2
    fixt = Fixture(team1, team2, 3)
    
    with pytest.raises(Exception) as exc_info:
        fixt.play_fixture()
    assert str(exc_info.value) == "Error: There cannot be more than 2 legs per fixture"
    
    # case 2: len(self.scores) >= 2
    fixt2 = Fixture(team1, team2, 2, (), [(1, 1), (2, 0)])
    
    with pytest.raises(Exception) as e:
        fixt2.play_fixture()
    assert str(e.value) == "Error: There cannot be more than 2 legs per fixture"

@mock.patch('objects.fixture.Fixture.update_team_attrs')
@mock.patch('objects.fixture.Fixture.compute_agg_score')
@mock.patch('objects.fixture.random.choice', return_value=3, autospec=True)
def test_play_fixture(mock_random_choice, mock_compute_agg_score, mock_update_team_attrs):
    score_list = [0] * 20 + [1] * 20 + [2] * 20 + [3] * 20 + [4] * 20 + [5] * 3 + [6] * 3 + [7] * 1 + [8] * 1 + [9] * 1 + [10] * 1
    
    fixt = Fixture(team1, team2)
    fixt.play_fixture()
    
    assert 2 == mock_random_choice.call_count
    mock_random_choice.assert_has_calls([mock.call(score_list), mock.call(score_list)])
    
    assert fixt.scores == [(3, 3)]
    assert fixt.result == "3-3"
    
    mock_update_team_attrs.assert_called_once_with(3, 3)
    mock_compute_agg_score.assert_called_once()
    
    assert fixt.leg == 2

def test_update_team_attrs():
    fixt = Fixture(team1, team2)
    team1_score = 5
    team2_score = 3
    
    fixt.update_team_attrs(team1_score, team2_score)
    assert team1.goals_for == team1_score
    assert team1.goals_against == team2_score
    assert team2.goals_for == team2_score
    assert team2.goals_against == team1_score

@mock.patch('objects.team.Team.drawn_game')
@mock.patch('objects.team.Team.won_game')
@mock.patch('objects.team.Team.lost_game')
def test_func_calls_update_team_attrs(mock_lost_game, mock_won_game, mock_drawn_game):
    # case 1: drawn game
    fix_1 = Fixture(team1, team2)
    team1_score = 3
    team2_score = 3
    
    fix_1.update_team_attrs(team1_score, team2_score)
    assert mock_drawn_game.call_count == 2
    
    # case 2: t1_score > t2_score
    fix_2 = Fixture(team1, team2)
    team1_score = 4
    team2_score = 3
    
    fix_2.update_team_attrs(team1_score, team2_score)
    mock_won_game.assert_called_once()
    mock_lost_game.assert_called_once()
    
    mock_won_game.reset_mock()
    mock_lost_game.reset_mock()
    
    # case 3: t1_score < t2_score
    fix_3 = Fixture(team1, team2)
    team1_score = 3
    team2_score = 4
    
    fix_3.update_team_attrs(team1_score, team2_score)
    mock_lost_game.assert_called_once()
    mock_won_game.assert_called_once()
    
def test_compute_agg_score():
    fixt = Fixture(team1, team2, 2, (), [(3, 2), (2, 5)])
    fixt.compute_agg_score()
    
    assert fixt.agg_score == (5, 7)

@mock.patch('objects.fixture.random.choices', side_effect=[[1, 1], [2, 1]], autospec=True)
def test_play_final(mock_random_choices):
    score_list = [0] * 20 + [1] * 20 + [2] * 20 + [3] * 20 + [4] * 20 + [5] * 3 + [6] * 3 + [7] * 1 + [8] * 1 + [9] * 1 + [10] * 1
      
    fixt = Fixture(team1, team2)
    fixt.play_final()
    
    assert 2 == mock_random_choices.call_count
    mock_random_choices.assert_has_calls([mock.call(population=score_list, k=2), mock.call(population=score_list, k=2)])