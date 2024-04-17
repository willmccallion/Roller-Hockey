PLAYOFF_NUM = 4

class Tournament:
    def __init__(self) -> None:
        self.all_teams = []

    def _swap(self,first,last):
        self.all_teams[first], self.all_teams[last] = self.all_teams[last], self.all_teams[first]

    def _save(self):
        s = "rank,name,w,ot_w,ot_l,l,gp,pts,gf,ga\n"
        rank = 1
        for team in self.all_teams:
            s += f"{rank},{team.get_name()},{team.get_wins()},{team.get_ot_wins()},{team.get_ot_losses()},{team.get_losses()},{team.get_gp()},{team.get_points()},{team.get_gf()},{team.get_ga()}\n"
            rank += 1

        with open("stats.csv", "w") as f:
            f.write(s)

    def _update_ranks(self):
        for i in range(len(self.all_teams)):
            for j in range(i+1,len(self.all_teams)):
                #Points
                if self.all_teams[i].get_points() < self.all_teams[j].get_points():
                    self._swap(i,j)
                elif self.all_teams[i].get_points() == self.all_teams[j].get_points():
                    #Games played:
                    if self.all_teams[i].get_gp() > self.all_teams[j].get_gp():
                        self._swap(i,j)
                    elif self.all_teams[i].get_gp() == self.all_teams[j].get_gp():
                        #Plus minus
                        if self.all_teams[i].get_gf() - self.all_teams[i].get_ga() < self.all_teams[j].get_gf() - self.all_teams[j].get_ga():
                            self._swap(i,j)
                        elif self.all_teams[i].get_gf() - self.all_teams[i].get_ga() == self.all_teams[j].get_gf() - self.all_teams[j].get_ga():
                            #Goals for
                            if self.all_teams[i].get_gf() < self.all_teams[j].get_gf():
                                self._swap(i,j)
                            elif self.all_teams[i].get_gf() == self.all_teams[j].get_gf():
                                #Goals against
                                if self.all_teams[i].get_ga() > self.all_teams[j].get_ga():
                                    self._swap(i,j)

        self._save()
        
    def new_team(self, name):
        self.all_teams.append(Team(name))
        self._update_ranks()

    def final(self,home,away,score, ot=False):
        home_score = score.split("-")[0]
        away_score = score.split("-")[1]

        for team in self.all_teams:
            #Home team
            if team.get_name().lower() == home.lower():
                team.set_gf(home_score)
                team.set_ga(away_score)
                if home_score > away_score and ot:
                    team.ot_win()
                elif away_score > home_score and ot:
                    team.ot_loss()
                elif home_score > away_score:
                    team.win()
                else:
                    team.loss()
            #Away team
            elif team.get_name().lower() == away.lower():
                team.set_gf(away_score)
                team.set_ga(home_score)
                if away_score > home_score and ot:
                    team.ot_win()
                elif home_score > away_score and ot:
                    team.ot_loss()
                elif away_score > home_score:
                    team.win()
                else:
                    team.loss()
            
        self._update_ranks()

    def get_teams(self):
        team_names = []
        for team in self.all_teams:
            team_names.append(team.get_name())
        return team_names
    
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
        self.record = [0,0,0,0]
        self.gf = 0
        self.ga = 0
        self.pts = 0
        self.gp = 0

    def win(self):
        self.record[0] += 1
        self.pts += 3
        self.gp += 1
    
    def ot_win(self):
        self.record[1] += 1
        self.pts += 2
        self.gp += 1
    
    def loss(self):
        self.record[3] += 1
        self.gp += 1
    
    def ot_loss(self):
        self.record[2] += 1
        self.pts += 1
        self.gp += 1

    def get_wins(self):
        return self.record[0]

    def get_losses(self):
        return self.record[3]
    
    def get_ot_wins(self):
        return self.record[1]
    
    def get_ot_losses(self):
        return self.record[2]

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
    
    def get_gp(self):
        return self.gp
    
    def set_rank(self,rank):
        self.rank = rank

    def get_rank(self):
        return self.rank
    
    def get_points(self):
        return self.pts
    
    def __str__(self) -> str:
        if self.gp > 0:
            return f"{self.rank:>4} | {self.name:>11} |  {self.record[0]:2}-{self.record[1]:2}-{self.record[2]:2}-{self.record[3]:2} | {self.gp:>2} | {self.pts:3} | {(self.pts/3)/self.gp:.2f} | {self.gf:2} | {self.ga:2} | {self.gf-self.ga:>3} |"
        else:
            return f"{self.rank:>4} | {self.name:>11} |  {self.record[0]:2}-{self.record[1]:2}-{self.record[2]:2}-{self.record[3]:2} | {self.gp:>2} | {self.pts:3} | 0.00 | {self.gf:2} | {self.ga:2} | {self.gf-self.ga:>3} |"