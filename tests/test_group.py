import pytest
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
            
def test_init_no_params():
    group_A = Group()
    
    assert group_A.team_list == []
    assert group_A.fixture_list == []
    
def test_init_valid_params():
    group_A = Group(teams, fixtures)
    
    assert group_A.team_list == teams
    assert group_A.fixture_list == fixtures

def test_init_invalid_params():
    # list attrs type
    with pytest.raises(TypeError) as t_err:
        group_A = Group([1, 2])
    assert str(t_err.value) == "Invalid team in provided team list"
    
    with pytest.raises(TypeError) as t_err:
        group_A = Group(teams, [1, 2])
    assert str(t_err.value) == "Invalid fixture in provided fixture list"
    
    # list lengths
    with pytest.raises(Exception) as e_info:
        group_A = Group([Team("team")])
    assert str(e_info.value) == "Error: Each group must consist of 4 teams"
    
    with pytest.raises(Exception) as e_info:
        group_A = Group(teams, [Fixture(teams[0], teams[1])])
    assert str(e_info.value) == "Error: Each team must play against every other team in the group"

def test_create_fixtures():
    group_A = Group(teams)
    group_A.create_fixtures()
    
    assert len(group_A.fixture_list) == 6
    assert [Fixture(teams[0], teams[1]) in group_A.fixture_list]
    assert [Fixture(teams[0], teams[2]) in group_A.fixture_list]
    assert [Fixture(teams[0], teams[3]) in group_A.fixture_list]
    assert [Fixture(teams[1], teams[2]) in group_A.fixture_list]
    assert [Fixture(teams[1], teams[3]) in group_A.fixture_list]
    assert [Fixture(teams[2], teams[3]) in group_A.fixture_list]

def test_sort():
    real = Team("real", 6, 6, 0, 0, 20, 5)
    united = Team("united", 6, 3, 0, 3, 14, 12)
    barca = Team("barca", 6, 3, 0, 3, 10, 11)
    chelsea = Team("chelsea", 6, 0, 0, 6, 3, 19)
    
    group_A = Group([united, chelsea, barca, real])
    group_A.sort()
    
    assert group_A.team_list[0] == real
    assert group_A.team_list[1] == united
    assert group_A.team_list[2] == barca
    assert group_A.team_list[3] == chelsea