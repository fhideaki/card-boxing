from damage_calculator import *
from deck import *
from effects import *
from game_judge import *
from player import *
from robot import *
from static import *
from ui_manager import *
from turn import *

# Criando o gerenciador de rounds
# No esquema do jogo, um round vai ser composto por 3 turnos.

class Round:
    def __init__(self, gamejudge: GameJudge):

        self.gamejudge = gamejudge

        # Contador de turnos
        self.turn_counter = 0

        self.score = {}

    def start_round(self, turns):

        self.gamejudge.log_message(f"------The bell rang! The round is starting!------")
        self.gamejudge.log_message(f"------This round is going to last {turns} turns!------")

        while self.turn_counter < turns:
            self.gamejudge.log_message(f"---Turn {self.turn_counter + 1}---")

            self.turn.execute_first_phase()
            self.turn.execute_second_phase()
            self.turn.execute_third_phase()

            self.turn_counter += 1

        self.score = self.gamejudge.score
        self.gamejudge.log_message(f"------The bell rang! The round is over!------")


        

    



        