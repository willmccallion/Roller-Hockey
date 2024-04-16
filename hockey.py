PLAYOFF_NUM = 4

class Teams:
    def __init__(self) -> None:
        self.all_teams = []

    def _update_ranks(self):
        for i in range(len(self.all_teams)):
            if i != len(self.all_teams) - 1:
                if self.all_teams[i].get_points() < self.all_teams[i+1].get_points():
                    temp = self.all_teams[i]
                    self.all_teams[i] = self.all_teams[i+1]
                    self.all_teams[i+1] = temp
    
    def new_team(self, name):
        self.all_teams.append(Team(name))

    def final(self,home,away,score, ot=False):
        home_score = score.split("-")[0]
        away_score = score.split("-")[1]

        for team in self.all_teams:
            #Home team
            if team.get_name().lower() == home.lower():
                team.set_gf(home_score)
                team.set_ga(away_score)
                if home_score > away_score:
                    team.win()
                elif away_score > home_score and ot:
                    team.ot_loss()
                else:
                    team.loss()
            #Away team
            elif team.get_name().lower() == away.lower():
                team.set_gf(away_score)
                team.set_ga(home_score)
                if away_score > home_score:
                    team.win()
                elif home_score > away_score and ot:
                    team.ot_loss()
                else:
                    team.loss()
            
        self._update_ranks()
    
    def __str__(self) -> str:
        s = ""
        rank = 1
        for team in self.all_teams:
            team.set_rank(rank)

            s += f"{team}\n"
            rank += 1
        return s
            
                
class Team:
    def __init__(self, name) -> None:
        self.name = name
        self.rank = 1
        self.record = [0,0,0]
        self.gf = 0
        self.ga = 0
        self.pts = 0

    def win(self):
        self.record[0] += 1
        self.pts += 2
    
    def loss(self):
        self.record[1] += 1
    
    def ot_loss(self):
        self.record[2] += 1
        self.pts += 1

    def get_name(self):
        return self.name

    def set_gf(self,gf):
        self.gf += int(gf)
    
    def set_ga(self,ga):
        self.ga += int(ga)

    def get_gf(self):
        return self.gf

    def get_ga(self):
        return self.ga
    
    def set_rank(self,rank):
        self.rank = rank

    def get_rank(self):
        return self.rank
    
    def get_points(self):
        return self.pts
    
    def __str__(self) -> str:
        if self.rank <= PLAYOFF_NUM:
            return f"Rank: {self.rank:2} | Name: {self.name:>10} |  Record: {self.record[0]}/{self.record[1]}/{self.record[2]} | PTS: {self.pts} | GF: {self.gf} | GA: {self.ga}"
        else:
            return f"Rank: {self.rank:2} | Name: {self.name:>10} |  Record: {self.record[0]}/{self.record[1]}/{self.record[2]} | PTS: {self.pts} | GF: {self.gf} | GA: {self.ga}"