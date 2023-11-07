'''
simulates running of ko stage which includes:
    - taking teams from their respective brackets from ro16 to semis
        - simulate playing the games over 2 legs
    - play final
'''
import random
from objects.fixture import Fixture
from objects.team import Team

class KOStage:
    def __init__(self, prev_winners:list, prog_teams:list = None, fixtures:list = None) -> None:
        self.previous_winners = prev_winners
        self.progressing_teams = prog_teams if prog_teams is not None else []
        self.fixture_list = fixtures if fixtures is not None else []
        
        # no list should contain duplicates
        # prev_winners and prog_teams must contain Teams
        if any([not isinstance(x, Team) for x in prev_winners]):
            raise TypeError("Invalid team provided in list")
        self.check_duplicates(prev_winners, "prev_winners")
        
        if prog_teams is not None and len(prog_teams) != 0:
            if any([not isinstance(x, Team) for x in prog_teams]):
                raise TypeError("Invalid team provided in list")
            
            # prog_teams must be a subset of prev_winners
            if not all(x in prev_winners for x in prog_teams):
                raise Exception("Teams that are progressing must be from previous winners")
            
            self.check_duplicates(prog_teams, "prog_teams")
    
            
        # fixtures must contain Fixtures
        if fixtures is not None and len(fixtures) != 0:
            if any([not isinstance(x, Fixture) for x in fixtures]):
                raise TypeError("Invalid fixture provided in list")
            self.check_duplicates(fixtures, "fixtures")
            
    # check for duplicates
    def check_duplicates(self, list, list_name):
        for i in range(len(list)-1):
                j = i+1
                
                while j<len(list):
                    if list[i] == list[j]:
                        raise Exception(list_name + " cannot contain duplicate instances of " + str(type(list[i])))
                    j+=1
    
    # util function to perform check for fixtures
    def check_fixtures(self, list_length:int):
        if self.fixture_list is not None and len(self.fixture_list) != 0:
            if len(self.fixture_list) != list_length:
                    raise Exception("Error: Incorrect number of fixtures for " + type(self).__name__ + " games")
            if len(self.fixture_list) == list_length:
                # teams must be from team_list
                fixture_teams = []
                for x in self.fixture_list:
                    if x.team1 not in fixture_teams:
                        fixture_teams.append(x.team1)
                    if x.team2 not in fixture_teams:
                        fixture_teams.append(x.team2)
                
                if type(self).__name__ == "RO16":
                    if not all(x in self.previous_winners or self.runner_ups for x in fixture_teams):
                        raise Exception("Error: Each team must play against every other team in the knockout stage")
                else:
                    if not all(x in self.previous_winners for x in fixture_teams):
                        raise Exception("Error: Each team must play against every other team in the knockout stage")
    
    # winners progress to the next stage
    def play_fixtures(self):
        for fixture in self.fixture_list:
            leg = 1
            
            while leg <= 2:
                fixture.play_fixture()
                leg += 1
            
            if fixture.agg_score[0] == fixture.agg_score[1]:
                result = fixture.play_final()
                
                if result[0] > result[1]:
                    self.progressing_teams.append(fixture.team1)
                else:
                    self.progressing_teams.append(fixture.team2)
            
            if fixture.agg_score[0] > fixture.agg_score[1]:
                self.progressing_teams.append(fixture.team1)
            
            if fixture.agg_score[0] < fixture.agg_score[1]:
                self.progressing_teams.append(fixture.team2)
    
    # random, any team vs any other team
    def create_fixtures(self):
        prev_winners = self.previous_winners.copy()
        for team in prev_winners:
            index = random.randrange(len(prev_winners))
            opponent = prev_winners[index]
        
            # cannot play against self
            while team == opponent:
                index = random.randrange(len(prev_winners))
                opponent = prev_winners[index]
                        
            fixture = Fixture(team1=team, team2=opponent)
            self.fixture_list.append(fixture)
            
            prev_winners.remove(team)
            prev_winners.remove(opponent)
            
        if len(prev_winners) != 0:
            fixture = Fixture(team1=prev_winners[0], team2=prev_winners[1])
            self.fixture_list.append(fixture)
            
            prev_winners.remove(prev_winners[0])
            prev_winners.remove(prev_winners[0])
        
        print("\n")
        
class RO16(KOStage):
    # prev_winners and runner-ups get updated from previous stage
    # prog_teams is updated for next stage
    def __init__(self, prev_winners:list, runner_ups:list, prog_teams:list = None, fixtures:list = None) -> None:
        super().__init__(prev_winners, prog_teams, fixtures)
        self.runner_ups = runner_ups
        
        if len(prev_winners) != 8:
            raise Exception(str(len(prev_winners)) + " winning teams have progressed from Group stage instead of 8")
        
        # runner-ups must contain Teams
        if any([not isinstance(x, Team) for x in runner_ups]):
            raise TypeError("Invalid team provided in list")
        
        if len(runner_ups) != 8:
            raise Exception(str(len(runner_ups)) + " runner-up teams have progressed from Group stage instead of 8")
        
        if prog_teams is not None and len(prog_teams) != 8:
            raise Exception(str(len(prog_teams)) + " teams have progressed to Quater-finals stage instead of 8")
        
        self.check_fixtures(8)
        
        # no duplicates
        self.check_duplicates(runner_ups, "runner_ups")
        
    # winners cannot face each other
    # runner-ups cannot face each other
    # teams from same group cannot face each other
    def create_fixtures(self):
        prev_winners = self.previous_winners.copy()
        for winner in prev_winners:
            index = random.randrange(len(self.runner_ups))
            runner_up = self.runner_ups[index]
            # teams cannot be from same group
            while winner.group == runner_up.group:
                index = random.randrange(len(self.runner_ups))
                runner_up = self.runner_ups[index]
            
            self.runner_ups.pop(index)
            
            fixture = Fixture(team1=winner, team2=runner_up)
            self.fixture_list.append(fixture)
            
class QfStage(KOStage):
    # winners get updated from previous stage with 8 teams
    def __init__(self, prev_winners, prog_teams=None, fixtures=None) -> None:
        super().__init__(prev_winners, prog_teams, fixtures)
        
        if len(prev_winners) != 8:
            raise Exception(str(len(prev_winners)) + " winning teams have progressed from Round of 16 stage instead of 8")
        
        if prog_teams is not None and len(prog_teams) != 4:
            raise Exception(str(len(prog_teams)) + " teams have progressed to Semi-finals stage instead of 4")
        
        self.check_fixtures(4)

class SfStage(KOStage):
    # winners gets updated from previous stage with 4 teams
    # losers is updated for next stage, as well as winners
    #    - losers play 3rd place playoff fixture
    #    - winners play final
    def __init__(self, prev_winners, prog_teams=None, fixtures=None) -> None:
        super().__init__(prev_winners, prog_teams, fixtures)
        self.losers = lambda: [x for x in prev_winners if x not in self.progressing_teams and len(self.progressing_teams) == 2]
                
        if len(prev_winners) != 4:
            raise Exception(str(len(prev_winners)) + " winning teams have progressed from Quater-final stage instead of 4")
        
        if prog_teams is not None and len(prog_teams) != 2:
            raise Exception(str(len(prog_teams)) + " teams have progressed to the Final instead of 2")
        
        self.check_fixtures(2)