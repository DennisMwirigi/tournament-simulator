import pytest
from unittest import mock
from objects.fixture import Fixture
from objects.ko_stage import KOStage, RO16, QfStage, SfStage
from objects.team import Team

def test_ko_stage_init_mandatory_params():
    with pytest.raises(Exception):
        kostage = KOStage()
    
def test_ko_stage_init_valid_params():
    kostage = KOStage(prev_winners=[])
    assert kostage.previous_winners == []
    assert kostage.progressing_teams == []
    assert kostage.fixture_list == []

def test_ko_stage_init_invalid_params():
    # prev_winners
    with pytest.raises(TypeError) as e_info:
        kostage = KOStage(prev_winners=[Team("united"), 2])
    assert str(e_info.value) == "Invalid team provided in list"
    
    # prog_teams
    with pytest.raises(TypeError) as e_info:
        kostage = KOStage(prev_winners=[], prog_teams=[1])
    assert str(e_info.value) == "Invalid team provided in list"
    
    with pytest.raises(Exception) as e_info:
        kostage = KOStage(prev_winners=[Team("united")], prog_teams=[Team("united"), Team("chelsea")])
    assert str(e_info.value) == "Teams that are progressing must be from previous winners"
    
    # fixtures
    with pytest.raises(TypeError) as e_info:
        kostage = KOStage(prev_winners=[], prog_teams=[], fixtures=["string"])
    assert str(e_info.value) == "Invalid fixture provided in list"

@mock.patch("objects.ko_stage.KOStage.check_duplicates")
def test_ko_stage_init_no_duplicates(mock_check_duplicates):
    prev_winners = [Team("united"), Team("chelsea")]
    prog_teams = [Team("united")]
    fixtures = [Fixture(team1=Team("united"), team2=Team("chelsea"))]
    
    kostage = KOStage(prev_winners=prev_winners, prog_teams=prog_teams, fixtures=fixtures)
    assert 3 == mock_check_duplicates.call_count
    mock_check_duplicates.assert_has_calls([mock.call(prev_winners, "prev_winners"), mock.call(prog_teams, "prog_teams"), mock.call(fixtures, "fixtures")], any_order=False)
    mock_check_duplicates.reset_mock()
    
    kostage = KOStage(prev_winners=prev_winners, prog_teams=prog_teams)
    assert 2 == mock_check_duplicates.call_count
    mock_check_duplicates.assert_has_calls([mock.call(prev_winners, "prev_winners"), mock.call(prog_teams, "prog_teams")])
    mock_check_duplicates.reset_mock()
    
    kostage = KOStage(prev_winners=prev_winners)
    mock_check_duplicates.assert_called_once_with(prev_winners, "prev_winners")

def test_ko_stage_check_duplicates():
    kostage = KOStage(prev_winners=[])

    # teams
    with pytest.raises(Exception) as e_info:
        kostage.check_duplicates([Team("united"), Team("united")], "prev_winners")
    assert str(e_info.value) == "prev_winners cannot contain duplicate instances of " + str(Team)
    
    # fixtures
    with pytest.raises(Exception) as e_info:
        kostage.check_duplicates([Fixture(team1=Team("united"), team2=Team("arsenal")), Fixture(team1=Team("united"), team2=Team("arsenal"))], "fixtures")
    assert str(e_info.value) == "fixtures cannot contain duplicate instances of " + str(Fixture)

def test_ko_stage_check_fixtures():
    prev_winners = [Team("united"), Team("chelsea")]
    prog_teams = [Team("united")]
    fixtures = [Fixture(team1=Team("united"), team2=Team("chelsea"))]
    
    kostage = KOStage(prev_winners=prev_winners, prog_teams=prog_teams, fixtures=fixtures)
    with pytest.raises(Exception) as e_info:
        kostage.check_fixtures(4)
    assert str(e_info.value) == "Error: Incorrect number of fixtures for KOStage games"
    
    invalid_fixture = Fixture(team1=Team("Gorge"), team2=Team("Bayern"))
    kostage = KOStage(prev_winners=prev_winners, prog_teams=prog_teams, fixtures=[invalid_fixture])
    with pytest.raises(Exception) as e_info:
        kostage.check_fixtures(1)
    assert str(e_info.value) == "Error: Each team must play against every other team in the knockout stage"
    
    # case RO16
    prev_winners = [Team("united", group="a"), Team("chelsea", group="b"), Team("arsenal", group="c"), Team("newcastle", group="d"), Team("city", group="e"), Team("liverpool", group="f"), Team("spurs", group="g"), Team("aston villa", group="h")]
    runner_ups = [Team("swansea", group="a"), Team("nottingham", group="b"), Team("leicester", group="c"), Team("brighton", group="d"), Team("brentford", group="e"), Team("palace", group="f"), Team("west ham", group="g"), Team("wolves", group="h")]
    
    ro16 = RO16(prev_winners=prev_winners, runner_ups=runner_ups)
    ro16.create_fixtures()
    ro16.fixture_list[4] = Fixture(team1=Team("gor mahia"), team2=Team("gorge"))
    
    with pytest.raises(Exception) as e_info:
        ro16.check_fixtures(8)
    assert str(e_info.value) == "Error: Each team must play against every other team in the knockout stage"

@mock.patch("objects.fixture.random.choices", autospec=True)
@mock.patch("objects.fixture.random.choice", autospec=True)
def test_ko_stage_play_fixtures(mock_random_choice, mock_random_choices):    
    # team 1 wins
    mock_random_choice.side_effect=[3,1, 1,0]
    kostage = KOStage(prev_winners=[Team("united"), Team("chelsea")], prog_teams=[], fixtures=[Fixture(team1=Team("united"), team2=Team("chelsea"))])
    kostage.play_fixtures()
    
    assert len(kostage.progressing_teams) == 1
    assert kostage.progressing_teams[0] == Team("united")
    mock_random_choice.reset_mock()
    
    # team 2 wins
    mock_random_choice.side_effect=[1,2, 3,4]
    kostage = KOStage(prev_winners=[Team("united"), Team("chelsea")], prog_teams=[], fixtures=[Fixture(team1=Team("united"), team2=Team("chelsea"))])
    kostage.play_fixtures()
    
    assert len(kostage.progressing_teams) == 1
    assert kostage.progressing_teams[0] == Team("chelsea")
    mock_random_choice.reset_mock()
    
    # draw and need to play final
    #   team 1 wins
    mock_random_choice.side_effect=[3,0, 1,4]
    mock_random_choices.return_value=[2,0]
    kostage = KOStage(prev_winners=[Team("united"), Team("chelsea")], prog_teams=[], fixtures=[Fixture(team1=Team("united"), team2=Team("chelsea"))])
    kostage.play_fixtures()
    
    assert len(kostage.progressing_teams) == 1
    assert kostage.progressing_teams[0] == Team("united")
    mock_random_choice.reset_mock()
    mock_random_choices.reset_mock()
    
    #   team 2 wins
    mock_random_choice.side_effect=[3,0, 1,4]
    mock_random_choices.return_value=[2,3]
    kostage = KOStage(prev_winners=[Team("united"), Team("chelsea")], prog_teams=[], fixtures=[Fixture(team1=Team("united"), team2=Team("chelsea"))])
    kostage.play_fixtures()
    
    assert len(kostage.progressing_teams) == 1
    assert kostage.progressing_teams[0] == Team("chelsea")
    mock_random_choice.reset_mock()
    mock_random_choices.reset_mock()

@mock.patch("objects.fixture.Fixture.play_final", return_value=[2,1])
@mock.patch("objects.fixture.Fixture.play_fixture")
def test_ko_stage_play_fixtures_func_calls(mock_play_fixture, mock_play_final):
    # no playoff decider
    kostage = KOStage(prev_winners=[Team("united"), Team("chelsea")], prog_teams=[], fixtures=[Fixture(team1=Team("united"), team2=Team("chelsea"))])
    kostage.fixture_list[0].agg_score = (3,1)
    kostage.play_fixtures()
    
    assert 2 == mock_play_fixture.call_count
    mock_play_final.assert_not_called()
    mock_play_fixture.reset_mock()
    
    # playoff decider
    kostage = KOStage(prev_winners=[Team("united"), Team("chelsea")], prog_teams=[], fixtures=[Fixture(team1=Team("united"), team2=Team("chelsea"))])
    kostage.fixture_list[0].agg_score = (1,1)
    kostage.play_fixtures()
    
    assert 2 == mock_play_fixture.call_count
    mock_play_final.assert_called_once()    

@mock.patch("objects.ko_stage.random.randrange", autospec=True)
def test_ko_stage_create_fixtures(mock_randrange):
    # does not play against self
    prev_winners = [Team("united"), Team("chelsea"), Team("arsenal"), Team("city")]
    mock_randrange.side_effect=[1,0]
    kostage = KOStage(prev_winners=prev_winners)
    kostage.create_fixtures()
    
    assert kostage.fixture_list[0] == Fixture(team1=Team("united"), team2=Team("chelsea"))
    assert kostage.fixture_list[1] == Fixture(team1=Team("city"), team2=Team("arsenal"))
    assert 2 == mock_randrange.call_count
    mock_randrange.reset_mock()
    
    # play against self first pass through
    prev_winners = [Team("united"), Team("chelsea"), Team("arsenal"), Team("city"), Team("liverpool"), Team("spurs"), Team("swansea"), Team("notts")]
    mock_randrange.side_effect=[0,2,0,1]
    kostage = KOStage(prev_winners=prev_winners)
    kostage.create_fixtures()
    
    assert kostage.fixture_list[0] == Fixture(team1=Team("united"), team2=Team("arsenal"))
    assert kostage.fixture_list[1] == Fixture(team1=Team("city"), team2=Team("chelsea"))
    assert kostage.fixture_list[2] == Fixture(team1=Team("swansea"), team2=Team("spurs"))
    assert kostage.fixture_list[3] == Fixture(team1=Team("liverpool"), team2=Team("notts"))
    assert 4 == mock_randrange.call_count

def test_RO16_init_mandatory_params():
    with pytest.raises(Exception):
        ro16 = RO16()

    prev_winners = [Team("united"), Team("chelsea"), Team("arsenal"), Team("city"), Team("liverpool"), Team("spurs"), Team("swansea"), Team("notts")]
    with pytest.raises(Exception): 
        ro16 = RO16(prev_winners=prev_winners)

def test_RO16_init_invalid_params():
    # list lengths
    prev_winners = [Team("united", group="a"), Team("chelsea", group="b"), Team("arsenal", group="c"), Team("newcastle", group="d"), Team("city", group="e"), Team("liverpool", group="f"), Team("spurs", group="g"), Team("aston villa", group="h")]
    runner_ups = [Team("swansea", group="a"), Team("nottingham", group="b"), Team("leicester", group="c"), Team("brighton", group="d"), Team("brentford", group="e"), Team("palace", group="f"), Team("west ham", group="g"), Team("wolves", group="h")]
    
    # prev_winners
    prev_winners.pop(3)
    with pytest.raises(Exception) as e_info:
        ro16 = RO16(prev_winners=prev_winners, runner_ups=runner_ups)
    assert str(e_info.value) == "7 winning teams have progressed from Group stage instead of 8"
    
    # runner-ups
    prev_winners.append(Team("newcastle", group="d"))
    runner_ups.pop(1)
    with pytest.raises(Exception) as e_info:
        ro16 = RO16(prev_winners=prev_winners, runner_ups=runner_ups)
    assert str(e_info.value) == "7 runner-up teams have progressed from Group stage instead of 8"
    
    # prog_teams
    runner_ups.append(Team("nottingham", group="b"))
    prog_teams = prev_winners.copy()
    prog_teams.pop(0)
    with pytest.raises(Exception) as e_info:
        ro16 = RO16(prev_winners=prev_winners, runner_ups=runner_ups, prog_teams=prog_teams)
    assert str(e_info.value) == "7 teams have progressed to Quater-finals stage instead of 8"
    
    # invalid types; other attrs tested in KOStage
    runner_ups[-1] = 2
    with pytest.raises(Exception) as e_info:
        ro16 = RO16(prev_winners=prev_winners, runner_ups=runner_ups)
    assert str(e_info.value) == "Invalid team provided in list"
    
    # check_fixtures and check_duplicates already tested in KOStage tests

def test_RO16_valid_params():
    prev_winners = [Team("united", group="a"), Team("chelsea", group="b"), Team("arsenal", group="c"), Team("newcastle", group="d"), Team("city", group="e"), Team("liverpool", group="f"), Team("spurs", group="g"), Team("aston villa", group="h")]
    runner_ups = [Team("swansea", group="a"), Team("nottingham", group="b"), Team("leicester", group="c"), Team("brighton", group="d"), Team("brentford", group="e"), Team("palace", group="f"), Team("west ham", group="g"), Team("wolves", group="h")]
    
    # other attrs tested in KOStage
    ro16 = RO16(prev_winners=prev_winners, runner_ups=runner_ups)
    assert ro16.runner_ups == runner_ups
    
    # check inheritance
    assert issubclass(RO16, KOStage)

@mock.patch("objects.ko_stage.random.randrange", side_effect=[1,1,1,1,1,1,1,0, 0,1,1,1,1,1,1,1,0], autospec=True)    
def test_RO16_create_fixtures(mock_randrange):
    prev_winners = [Team("united", group="a"), Team("chelsea", group="b"), Team("arsenal", group="c"), Team("newcastle", group="d"), Team("city", group="e"), Team("liverpool", group="f"), Team("spurs", group="g"), Team("aston villa", group="h")]
    runner_ups = [Team("swansea", group="a"), Team("nottingham", group="b"), Team("leicester", group="c"), Team("brighton", group="d"), Team("brentford", group="e"), Team("palace", group="f"), Team("west ham", group="g"), Team("wolves", group="h")]
    
    # runner-up not from same group
    runner_ups_copy = runner_ups.copy()
    ro16 = RO16(prev_winners=prev_winners, runner_ups=runner_ups_copy)
    ro16.create_fixtures()
    assert 8 == mock_randrange.call_count
    for i in range(8):
        j = i+1 if i<=6 else 0
        assert ro16.fixture_list[i].team1 == prev_winners[i]
        assert ro16.fixture_list[i].team2 == runner_ups[j]
    mock_randrange.reset_mock()
    
    # runner-up from same group
    runner_ups_copy = runner_ups.copy()
    ro16 = RO16(prev_winners=prev_winners, runner_ups=runner_ups_copy)
    ro16.create_fixtures()
    # extra call as teams cannot be from same group
    assert 9 == mock_randrange.call_count

def test_QfStage_init_invalid_params():
    prev_winners = [Team("united", group="a"), Team("chelsea", group="b"), Team("arsenal", group="c"), Team("newcastle", group="d"), Team("city", group="e"), Team("liverpool", group="f"), Team("spurs", group="g"), Team("aston villa", group="h")]
    prog_teams = prev_winners[:3]
    
    # prev_winners
    prev_winners.pop(0)
    with pytest.raises(Exception) as e_info:
        qf = QfStage(prev_winners=prev_winners)
    assert str(e_info.value) == "7 winning teams have progressed from Round of 16 stage instead of 8"
    
    # prog_teams
    prev_winners.append(Team("united"))
    with pytest.raises(Exception) as e_info:
        qf = QfStage(prev_winners=prev_winners, prog_teams=prog_teams)
    assert str(e_info.value) == "3 teams have progressed to Semi-finals stage instead of 4"
    
    # check_fixtures already tested in KOStage tests

def test_QfStage_init_valid_params():
    prev_winners = [Team("united", group="a"), Team("chelsea", group="b"), Team("arsenal", group="c"), Team("newcastle", group="d"), Team("city", group="e"), Team("liverpool", group="f"), Team("spurs", group="g"), Team("aston villa", group="h")]
    prog_teams = prev_winners[:4]
    
    # attrs already tested in KOStage
    qfstage = QfStage(prev_winners=prev_winners, prog_teams=prog_teams)
    
    # check inheritance
    assert issubclass(qfstage.__class__, KOStage)
    
    # check_fixtures already tested in KOStage tests

def test_SfStage_init_invalid_params():
    prev_winners = [Team("united"), Team("chelsea"), Team("arsenal"), Team("newcastle")]
    prog_teams = prev_winners[:3]
    
    # prev_winners
    prev_winners.pop(0)
    with pytest.raises(Exception) as e_info:
        semis = SfStage(prev_winners=prev_winners)
    assert str(e_info.value) == "3 winning teams have progressed from Quater-final stage instead of 4"
    
    # prog_teams
    prev_winners.append(Team("united"))
    with pytest.raises(Exception) as e_info:
        semis = SfStage(prev_winners=prev_winners, prog_teams=prog_teams)
    assert str(e_info.value) == "3 teams have progressed to the Final instead of 2"
    
    # check_fixtures already tested in KOStage tests

def test_SfStage_init_valid_params():
    prev_winners = [Team("united"), Team("chelsea"), Team("arsenal"), Team("newcastle")]
    prog_teams = prev_winners[:2]
    
    # other attrs already tested in KOStage
    semis = SfStage(prev_winners=prev_winners, prog_teams=prog_teams)
    assert semis.losers() == [Team("arsenal"), Team("newcastle")]
    
    # check inheritance
    assert issubclass(semis.__class__, KOStage)
    
    # check_fixtures already tested in KOStage tests