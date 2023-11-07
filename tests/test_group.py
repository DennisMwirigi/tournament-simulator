import pytest
from unittest import mock
from objects.group import Group
from objects.fixture import Fixture
from objects.team import Team

teams = []
for i in range(1, 5):
    teams.append(Team("team" + str(i)))

fixtures = []
for i in range(0, 3):
    j = i+1
    while j < len(teams):
        fixtures.append(Fixture(teams[i], teams[j]))
        j+=1

def test_init_no_name():
    with pytest.raises(Exception):
        group = Group()
     
def test_init_with_name():
    group_A = Group("A")
    
    assert group_A.name == "A"
    assert group_A.team_list == []
    assert group_A.fixture_list == []
    
def test_init_valid_params():
    group_A = Group("A", teams, fixtures)
    
    assert group_A.name == "A"
    assert group_A.team_list == teams
    assert group_A.fixture_list == fixtures

def test_init_invalid_params():
    # list attrs type
    with pytest.raises(TypeError) as t_err:
        group_A = Group("A", [1, 2])
    assert str(t_err.value) == "Invalid team in provided team list"
    
    with pytest.raises(TypeError) as t_err:
        group_A = Group("A", teams, [1, 2])
    assert str(t_err.value) == "Invalid fixture in provided fixture list"
    
    # list lengths
    with pytest.raises(Exception) as e_info:
        group_A = Group("A", [Team("team")])
    assert str(e_info.value) == "Error: Each group must consist of 4 teams"
    
    with pytest.raises(Exception) as e_info:
        group_A = Group("A", teams, [Fixture(teams[0], teams[1])])
    assert str(e_info.value) == "Error: Not enough fixtures for group games"
    
    # fixture list comprised of fixtures with teams from team list
    new_fixtures = fixtures.copy()
    new_fixtures[4] = Fixture(team1=Team("Gor Mahia"), team2=Team("Westcastle Utd"))
    
    with pytest.raises(Exception) as e_info:
        group_A = Group("A", teams=teams, fixtures=new_fixtures)
    assert str(e_info.value) == "Error: Each team must play against every other team in the group"

def test_init_duplicates():
    # teams
    dup_team_list = teams.copy()
    dup_team_list[3] = teams[0]
    
    with pytest.raises(Exception) as e_info:
        group = Group("a", teams=dup_team_list)
    assert str(e_info.value) == "Group cannot contain duplicate teams"
    
    # fixtures
    dup_fix_list = fixtures.copy()
    dup_fix_list[3] = fixtures[0]
    
    with pytest.raises(Exception) as e_info:
        group = Group("a", teams=teams, fixtures=dup_fix_list)
    assert str(e_info.value) == "Group cannot contain duplicate fixtures"

def test_add_team():
    # invalid team
    group = Group("A")
    with pytest.raises(TypeError) as e_info:
        group.add_team(1)
    assert str(e_info.value) == "Invalid team provided"
    
    # list length
    group = Group("A", teams=teams)
    with pytest.raises(IndexError) as e_info:
        group.add_team(Team("Celtic"))
    assert str(e_info.value) == "Group consists of a maximum of 4 teams"
    
    # duplicate team
    group = Group("A")
    group.add_team(Team("1"))
    
    with pytest.raises(Exception) as e_info:
        group.add_team(Team("1"))
    assert str(e_info.value) == "Group cannot contain duplicate teams"
    
    # team has been added to team list
    assert len(group.team_list) == 1

def test_create_fixtures():
    group_A = Group("A", teams)
    group_A.create_fixtures()
    
    assert len(group_A.fixture_list) == 6
    assert any([Fixture(teams[0], teams[1]) in group_A.fixture_list])
    assert any([Fixture(teams[0], teams[2]) in group_A.fixture_list])
    assert any([Fixture(teams[0], teams[3]) in group_A.fixture_list])
    assert any([Fixture(teams[1], teams[2]) in group_A.fixture_list])
    assert any([Fixture(teams[1], teams[3]) in group_A.fixture_list])
    assert any([Fixture(teams[2], teams[3]) in group_A.fixture_list])

def test_sort():
    # case 1: by points only
    real = Team("real", 6, 5, 0, 1, 20, 5)
    united = Team("united", 6, 3, 1, 2, 14, 12)
    barca = Team("barca", 6, 2, 1, 3, 10, 11)
    chelsea = Team("chelsea", 6, 1, 0, 5, 3, 19)
    
    group_A = Group("A", [united, chelsea, barca, real])
    group_A.sort()
    
    assert group_A.team_list[0] == real
    assert group_A.team_list[1] == united
    assert group_A.team_list[2] == barca
    assert group_A.team_list[3] == chelsea
    
    # case 2: by points and goal difference
    real = Team("real", 6, 3, 1, 2, 20, 5)
    united = Team("united", 6, 3, 0, 3, 14, 12)
    barca = Team("barca", 6, 3, 0, 3, 10, 11)
    chelsea = Team("chelsea", 6, 2, 1, 3, 3, 19)
    
    group_A = Group("A", [united, chelsea, barca, real])
    group_A.sort()
    
    assert group_A.team_list[0] == real
    assert group_A.team_list[1] == united
    assert group_A.team_list[2] == barca
    assert group_A.team_list[3] == chelsea
    
    # case 3: by goal difference only
    real = Team("real", 6, 3, 0, 3, 20, 5)
    united = Team("united", 6, 3, 0, 3, 14, 12)
    barca = Team("barca", 6, 3, 0, 3, 10, 11)
    chelsea = Team("chelsea", 6, 3, 0, 3, 3, 19)
    
    group_A = Group("A", [united, chelsea, barca, real])
    group_A.sort()
    
    assert group_A.team_list[0] == real
    assert group_A.team_list[1] == united
    assert group_A.team_list[2] == barca
    assert group_A.team_list[3] == chelsea

@mock.patch("objects.fixture.Fixture.play_final", return_value=[2, 3], autospec=True)
def test_det_prog_teams(mock_play_final):
    # case 1: pos 2 & 3 don't have same points and gd
    real = Team("real", 6, 5, 0, 1, 20, 5)
    united = Team("united", 6, 3, 1, 2, 14, 12)
    barca = Team("barca", 6, 2, 1, 3, 10, 11)
    chelsea = Team("chelsea", 6, 1, 0, 5, 3, 19)
    
    group_A = Group("A", [united, chelsea, barca, real])
    group_A.sort()
    
    prog_teams = group_A.det_prog_teams()
    
    assert prog_teams == {"Winner": real, "Runner-up": united}
    mock_play_final.assert_not_called()
    
    # case 2: pos 2 & 3 have same points and gd
    real = Team("real", 6, 3, 1, 2, 20, 5)
    united = Team("united", 6, 3, 0, 3, 14, 12)
    barca = Team("barca", 6, 3, 0, 3, 14, 12)
    chelsea = Team("chelsea", 6, 2, 1, 3, 3, 19)
    
    group_A = Group("A", [united, chelsea, barca, real])
    group_A.sort()
    
    prog_teams = group_A.det_prog_teams()
    
    assert prog_teams["Winner"] == real 
    assert prog_teams["Runner-up"] == barca
    mock_play_final.assert_called_once()