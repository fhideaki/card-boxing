from damage_calculator import *
from deck import *
from effects import *
from game_judge import *
from player import *
from robot import *
from static import *
from ui_manager import *
from turn import *
from round import *

# Criando a classe Game que vai levar todos os objetos, e vai fazer com que eles executem x rounds de y turnos.
class Game:
    def __init__(self, player1: Player, player2: Player, num_rounds, num_turns_per_round):
        
        self.player1 = player1
        self.player2 = player2

        self.num_rounds = num_rounds
        self.num_turns_per_round = num_turns_per_round

        self.ui = UIManager()

        self.damagecalculator = DamageCalculator(self.ui)

        self.gamejudge = GameJudge(self.ui, self.damagecalculator)

        self.score = {}

        self.round_counter = 0

        self.round = Round(self.gamejudge)

        self.turn = Turn(self.player1, self.player2, self.gamejudge, self.damagecalculator)

    def game_start(self):

        self.gamejudge.log_message("Gooooood Evening ladies and gentleman!! Welcome to the most feracious fight of the world, the Robot Mayhem Arena!!!!!!!!")
        self.gamejudge.log_message("(crowd cheering noises)")

        self.gamejudge.log_message(f"In the Red corner, weighting {self.player1.initial_constitution} of pure destruction is {self.player1.robot.robot_name}! And his coach {self.player1.name} assisting in the corner.")
        self.gamejudge.log_message(f"In the Blue corner, weighting {self.player2.initial_constitution} of metal hardened through many bouts is {self.player2.robot.robot_name}! And his coach {self.player2.name} assisting in the corner.")

        self.gamejudge.log_message("Leeeeeeeeet's get ready to RUMBLEEEEEEEEEEEEEEEEEEEE")

        if self.round_counter == 0:
            self.turn.game_start()

        self.gamejudge.log_message(f"------The rounds are going to last {self.num_turns_per_round} turns!------")

        while self.round_counter < self.num_rounds:

            self.gamejudge.log_message(f"---Round {self.round_counter + 1}---")

            self.round.start_round(self.num_turns_per_round)

            self.round_counter += 1

            for player, score in self.round.score.items():
                self.score[player] += score

