import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import random

# Defining the Player class for representing a player's stats
class Player:
    def __init__(self, name, bowling, batting, fielding, running, experience):
        self.name = name
        self.bowling = bowling
        self.batting = batting
        self.fielding = fielding
        self.running = running
        self.experience = experience

        
# Definig the Team Class to describe the team's name and players
class Teams:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.captain = None
        self.batting_lineup = []

    def Captain(self, player):
        self.captain = player

    def Next_player(self):
        return self.batting_lineup.pop(0)

    def choose_bowler(self):
        return random.choice(self.players)
    
# Defining the Field Class which describes the condition of pitch, size ,etc
class Field:
    def __init__(self, size, audience_size, pitch_conditions, home_advantage):
        self.size = size
        self.audience_size = audience_size
        self.pitch_conditions = pitch_conditions
        self.home_ground_advantage= home_advantage


# Defining the Umpire class which represents the match umpire
class Umpire:
    def __init__(self):
        self.score = 0
        self.wickets = 0
        self.overs = 0

    def Prediction(self, batsman, bowler):
        run_prob = batsman.batting * (1 - bowler.bowling)
        out_declared = random.random() > run_prob
        if out_declared:
            self.wickets += 1
            return 'wicket'
        else:
            runs = random.randint(0, 6)
            self.score += runs
            if runs == 0:
                return 'dot_ball'
            elif runs == 4:
                return 'four'
            elif runs == 6:
                return 'six'
            else:
                return 'run'
            

# Defining the Commentary class which provides commentary during match  
class Commentary:
    def __init__(self):  #Initializing the commentary
        self.events = {
            'BOUNDARY': ["Found the gap for four runs!","The ball races to the boundary!" ],
            'SIX': ["Smashed it out of the stadium!","A magnificient shot for six!"],
            'WICKET': ["Bowled him!", "Cleaned up the stumps!", "Caught behind!", "Howzat!!"],
            'DOT_BALL': ["Dot ball. Great balling!", "The batsman fails to score.", "Getting tough for the batsman. That is some class balling"],
            'RUN': ["Quick single taken.", "Batsmen runs between the wicket."],
            'OVER_ENDS': ["End of the over.", "Bowling change for the next over."]
        }


    #Giving commentary based on the match status
    def provide_commentary(self, umpire, batting_squad, bowling_squad, over, ball, last_event):
        commentary = f"Over {over}.{ball}: "
        
        if last_event:
            commentary += self.events[last_event][random.randint(0, len(self.events[last_event]) - 1)]
            commentary += " "

        commentary += f"{batting_squad.name} {umpire.score}/{umpire.wickets}"

        if ball == 6:
            commentary += f" | {bowling_squad.name} needs {umpire.score + 1} to win."

        return commentary
    

# Defining the Match class to describe a match
class Match:
    def __init__(self, team1, team2, field):
        self.team1 = team1
        self.team2 = team2
        self.field = field
        self.umpire = Umpire()
        self.commentator = Commentary()

    def start_innings(self, batting_team, bowling_team): #Simulating one inning
        last_event = None
        for over in range(1, 21):  # Simulate 20 overs match
            if not batting_team.batting_lineup:
                print(f"All out! {batting_team.name} inning ends with a score of {self.umpire.score}/{self.umpire.wickets} after {over-1} overs.")
                return

            bowler = bowling_team.choose_bowler()
            for ball in range(1, 7):  # Simulate 6 balls per over
                if not batting_team.batting_lineup:
                    print(f"All out! {batting_team.name} inning ends with a score of {self.umpire.score}/{self.umpire.wickets} after {over-1} overs.")
                    return

                batsman = batting_team.Next_player()
                outcome = self.umpire.Prediction(batsman, bowler)
                last_event = self.outcomes(outcome, batsman, bowler)
                commentary = self.commentator.provide_commentary(self.umpire, batting_team, bowling_team, over, ball, last_event)
                print(commentary)
                if self.umpire.wickets == len(batting_team.players)-1 or (over == 20 and ball == 6) or not batting_team.batting_lineup:
                    print(f"{batting_team.name} inning ends with a score of {self.umpire.score}/{self.umpire.wickets} after {over}.{ball} overs.")
                    return
            last_event = 'over_ends'


    #Start match
    def kickoff_match(self):
        print(f"Welcome to the cricket match between {self.team1.name} and {self.team2.name}! It's a lovely weather here and great ground to kickoff the match")

        # Simulate first inning
        print(f"\n{self.team1.name} is batting:")
        self.start_innings(self.team1, self.team2)
        print("\n----- Innings Break -----\n")

        # Simulate second inning
        print(f"\n{self.team2.name} is batting:")
        self.start_innings(self.team2, self.team1)

        # Determine the winner
        if self.team1.batting_lineup and not self.team2.batting_lineup:
            print(f"\n{self.team1.name} wins the match!")
        elif self.team2.batting_lineup and not self.team1.batting_lineup:
            print(f"\n{self.team2.name} wins the match!")
        else:
            print("\nMatch ended in a draw!")

            
    #Match updating status
    def outcomes(self, outcome, batsman, bowler):

        if outcome == 'WICKET':
            return 'wicket'
        elif outcome == 'SIX':
            return 'SIX'
        elif outcome == 'BOUNDARY':
            return 'boundary'
        elif outcome == 'DOT_BALL':
            return 'dot_ball'
        elif outcome == 'RUN':
            return 'run'
        

# Definig CricketMatch to design GUI for simulator
class CricketGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Match Simulator")
        self.root.configure(bg="#f0f0f0")
        
        self.start_button = tk.Button(root, text="Start Match", command=self.start_match, bg="#3366cc", fg="white")
        self.start_button.pack(pady=10)
        
        self.output_text = scrolledtext.ScrolledText(root, width=80, height=20 ,bg="black", fg="white")
        self.output_text.pack(padx=10, pady=5)
        
    def start_match(self):
        self.output_text.delete("1.0", tk.END)

        #Defining team 1 players
        player1 = Player("MS Dhoni", 0.7, 0.9, 0.99, 0.85, 0.95)
        player2 = Player("Virat Kohli", 0.6, 0.95, 0.9, 0.8, 0.91)
        player3 = Player("Jasprit Bumrah", 0.4, 0.89, 0.8, 0.8, 0.8)
        player4 = Player("Rohit Sharma", 0.7, 0.85, 0.95, 0.88, 0.92)
        player5 = Player("Dinesh Karthik", 0.8, 0.8, 0.85, 0.75, 0.9)
        player6 = Player("Sachin Tendulkar", 0.85, 0.77, 0.97, 0.86, 0.85)
        player7 = Player("Yuvraj Singh", 0.9, 0.85, 0.97, 0.89, 0.92)
        player8 = Player("Bhuvaneshwar", 0.79, 0.77, 0.88, 0.78, 0.88)
        player9 = Player("Chahal", 0.85, 0.75, 0.85, 0.75, 0.85)
        player10 = Player("Mohammed Shami", 0.85, 0.82, 0.87, 0.85, 0.89)
        player11 = Player("Ashwin", 0.84, 0.9, 0.75, 0.86, 0.92)

        

        #Defining team 2 players
        player12 = Player("Eoin Morgan", 0.2, 0.8, 0.85, 0.7, 0.88)
        player13 = Player("David Warner", 0.1, 0.9, 0.8, 0.7, 0.9)
        player14 = Player("Pat Cummins", 0.9, 0.2, 0.8, 0.5, 0.8)
        player15 = Player("Ross Taylor", 0.2, 0.8, 0.75, 0.6, 0.85)
        player16 = Player("Kagiso Rabada", 0.8, 0.2, 0.7, 0.6, 0.85)
        player17 = Player("Kane Williamson", 0.1, 0.85, 0.75, 0.7, 0.9)
        player18 = Player("Steve Smith", 0.2, 0.85, 0.8, 0.75, 0.92)
        player19 = Player("Mitchelle Starc", 0.8, 0.2, 0.8, 0.6, 0.88)
        player20 = Player("Ben Stokes", 0.2, 0.85, 0.75, 0.7, 0.9)
        player21 = Player("Trent Boult", 0.8, 0.2, 0.7, 0.5, 0.85)
        player22 = Player("Faf du Plessis", 0.2, 0.85, 0.9, 0.75, 0.9)


        team1 = Teams("India", [player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11])
        team2 = Teams("Australia", [player12, player13, player14, player15, player16, player17, player18, player19, player20, player21, player22])

        #Assigning Captains
        team1.Captain(player1)
        team2.Captain(player12)
        team1.batting_lineup = team1.players.copy()
        team2.batting_lineup=team2.players.copy()

        field = Field(1, 1, 0.8, 0.3) #Field Stats

        match = Match(team1, team2, field) #Match object
        
        import sys
        sys.stdout = Redirector(self.output_text)
        
        match.kickoff_match() #Starting of match 

class Redirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        
    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
    def flush(self):
        pass    


#Main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = CricketGUI(root)
    root.mainloop()