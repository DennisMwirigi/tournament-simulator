'''
simulates running of ko stage which includes:
    - taking teams from their respective brackets from ro16 to semis
        - simulate playing the games over 2 legs
    - play final
'''
import random
from objects.fixture import Fixture

class KOStage:
    def __init__(self, prev_winners:list, prog_teams:list = None, fixtures:list = None) -> None:
        self.previous_winners = prev_winners
        self.progressing_teams = prog_teams if prog_teams is not None else []
        self.fixture_list = fixtures if fixtures is not None else []
    
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
            
            # prev_winners.pop(index)
            
            fixture = Fixture(team1=team, team2=opponent)
            self.fixture_list.append(fixture)
            
            prev_winners.remove(team)
            prev_winners.remove(opponent)
            
        if len(prev_winners) != 0:
            fixture = Fixture(team1=prev_winners[0], team2=prev_winners[1])
            self.fixture_list.append(fixture)
            
            prev_winners.remove(prev_winners[0])
            prev_winners.remove(prev_winners[0])
        
class RO16(KOStage):
    # prev_winners and runner-ups get updated from previous stage
    # prog_teams is updated for next stage
    def __init__(self, prev_winners:list, runner_ups:list, prog_teams:list = None, fixtures:list = None) -> None:
        super().__init__(prev_winners, prog_teams, fixtures)
        self.runner_ups = runner_ups
        
        if len(prev_winners) != 8:
            raise Exception(len(prev_winners), "winning teams have progressed from Group stage instead of 8")
        if len(runner_ups) != 8:
            raise Exception(len(runner_ups), "runner-up teams have progressed from Group stage instead of 8")
    
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

class SfStage(KOStage):
    # winners gets updated from previous stage with 4 teams
    # losers is updated for next stage, as well as winners
    #    - losers play 3rd place playoff fixture
    #    - winners play final
    def __init__(self, prev_winners, prog_teams=None, losers=None, fixtures=None) -> None:
        super().__init__(prev_winners, prog_teams, fixtures)
        self.losers = lambda: [x for x in prev_winners if x not in self.progressing_teams]
        
        if len(prev_winners) != 4:
            raise Exception(str(len(prev_winners)) + " winning teams have progressed from Quater-final stage instead of 4")