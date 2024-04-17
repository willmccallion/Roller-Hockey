from tournament import Tournament
TOURNAMENT = Tournament()
def add():
    name = input("What is the team name: ")
    TOURNAMENT.new_team(name)

def new_game():
    valid_names = TOURNAMENT.get_teams()
    home = input("Home team: ")
    while home not in valid_names:
        home = input("Home team: ")
    away = input("Away team: ")
    while away == home or away not in valid_names:
        away = input("Away team: ")
    
    final_score = input("Final score ({home}-{away})")
    confirm_score = input("Confirm final score: ")
    while final_score != confirm_score:
        final_score = input("Final score ({home}-{away})")
        confirm_score = input("Confirm final score: ")
    
    home_score = int(final_score.split("-")[0])
    away_score = int(final_score.split("-")[1])
    overtime = False
    if home_score + 1 == away_score or home_score == away_score + 1:
        ot_user = input("Overtime (Y/N): ")
        while ot_user.lower() not in ['y','n']:
            ot_user = input("Overtime (Y/N): ")
        if ot_user.lower() == "y":
            overtime = True

    TOURNAMENT.final(home,away,final_score,overtime)

def get_input():
    valid = ["add","game","exit"]
    user_input = input("Add/Game/Exit\n")
    
    while user_input not in valid:
        user_input = input("Add/Game/Exit\n")
    
    if user_input.lower() == valid[2]:
        return True
    elif user_input.lower() == valid[1]:
        new_game()
    elif user_input.lower() == valid[0]:
        add()
    return False

def main():
    quit = False
    while not quit:
        print(TOURNAMENT)
        quit = get_input()

if __name__ == "__main__":
    main()