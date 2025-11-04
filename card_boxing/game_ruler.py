<<<<<<< HEAD
# Imports
from player import Player
from static import conflicts
import random

# Classe para resolver o conflito. O principal é entregar um multiplicador de dano.
class CardResolver:
    def __init__(self):
        pass

    # Adicionando os multiplicadores de resistências e fraquezas
    def apply_resistances_and_weaknesses(self, base_damage, attack_type, defender_robot):
        
        # Conta quantas vezes o tipo aparece nas resistências/fraquezas
        weakness_count = defender_robot.weaknesses.count(attack_type)
        resistance_count = defender_robot.resistances.count(attack_type)

        # Aplica multiplicadores cumulativos. Cada contador significa um adicional de +0.5 (50%)
        adjusted_damage = base_damage * (1 + (0.5 * weakness_count)) - (1 + (0.5 ** resistance_count))

        return adjusted_damage
    
    # Método para resolver os conflitos de cartas
    def resolveConflict(self, card1, card2):
        # Pega a classe de cada carta jogada
        c1 = card1["class"]
        c2 = card2["class"]
        # Entrega um resultado baseado na tabela de conflitos.
        base_outcome = conflicts[c1][c2]

        # Dicionário base que entrega o resultado
        result = {
            "winner": None,
            "action": None,
            "multiplier": None
        }

        # Casos Básicos - Sem cartas especiais
        if base_outcome == "ATTACK":
            result["winner"] = "p1" if c1 == "ATTACK" else "p2"
            result["action"] = base_outcome
            result["multiplier"] = card1["meta"]["atk"] - card2["meta"]["def"] if c1 == "ATTACK" else card2["meta"]["atk"] - card1["meta"]["def"]
        elif base_outcome == "GUARD":
            result["winner"] = "p1" if c1 == "GUARD" else "p2"
            result["action"] = base_outcome
            result["multiplier"] = card1["meta"]["def"] - card2["meta"]["atk"] if c1 == "GUARD" else card2["meta"]["def"] - card1["meta"]["atk"]
        elif base_outcome == "CLINCH":
            result["winner"] = "p1" if c1 == "CLINCH" else "p2"
            result["action"] = base_outcome
            result["multiplier"] = card1["meta"]["cli"] - card2["meta"]["def"] if c1 == "CLINCH" else card2["meta"]["cli"] - card1["meta"]["def"]

        # Casos especiais
        result = self.handle_special_cases(card1, card2, result)

        return result

    def handle_special_cases(self, card1, card2, result):

        c1_name, c2_name = card1["name"], card2["name"]

        # Strong Attack causa double damage se o oponente clinchar
        if c1_name == "Strong Attack" and card2["class"] == "CLINCH":
            result["multiplier"] = 2

        if c2_name == "Strong Attack" and card1["class"] == "CLINCH":
            result["multiplier"] = 2

        # Special Guard bloqueia tudo
        if c1_name == "Special Guard":
            result["multiplier"] = 0

        if c2_name == "Special Guard":
            result["multiplier"] = 0

        return result

class GameRuler:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.resolver = CardResolver()
        self.score = {"p1": 0, "p2": 0}

    # Método para 1 turno
    def playTurn(self):
        # Exibição do status atual
        self.player1.showStatus()
        self.player2.showStatus()

        # Compra de cartas
        while len(self.player1.hand) < 4:
            self.player1.getCard(1)

        while len(self.player2.hand) < 4:
            self.player2.getCard(1)

        # Escolhendo a carta do jogador 1
        card_player1 = self.player1.playCard()

        # Escolhendo a carta do jogador 2
        card_player2 = self.player2.playCard()

        # Resolução de ações
        result = self.resolver.resolveConflict(card_player1, card_player2)

        # Cálculo do dano
        if result["action"] == "ATTACK":
            if result["winner"] == "p1":

                base_damage = self.player1.initial_attack
                modified_damage = base_damage * result["multiplier"]
                full_damage = self.resolver.apply_resistances_and_weaknesses(modified_damage, card_player1["type"], self.player2.robot)
                self.player2.initial_HP -= full_damage - (self.player2.initial_defense * 0.5)
                self.score["p1"] += 1

            elif result["winner"] == "p2":

                base_damage = self.player2.initial_attack
                modified_damage = base_damage * result["multiplier"]
                full_damage = self.resolver.apply_resistances_and_weaknesses(modified_damage, card_player2["type"], self.player1.robot)
                self.player1.initial_HP -= full_damage - (self.player1.initial_defense * 0.5)
                self.score["p2"] += 1

        elif result["action"] == "GUARD":
            if result["winner"] == "p1":

                base_damage = self.player1.initial_defense
                modified_damage = base_damage * result["multiplier"]
                full_damage = self.resolver.apply_resistances_and_weaknesses(modified_damage, card_player1["type"], self.player2.robot)
                self.player2.initial_HP -= full_damage - (self.player2.initial_defense * 0.9)
                self.score["p1"] += 1

            elif result["winner"] == "p2":

                base_damage = self.player2.initial_defense
                modified_damage = base_damage * result["multiplier"]
                full_damage = self.resolver.apply_resistances_and_weaknesses(modified_damage, card_player2["type"], self.player1.robot)
                self.player1.initial_HP -= full_damage - (self.player1.intial_defense * 0.9)
                self.score["p2"] += 1

        elif result["action"] == "CLINCH":
            if result["winner"] == "p1":

                self.player2.hand.pop(random.randrange(len(self.player2.hand)))
                self.score["p1"] += 1

            elif result["winner"] == "p2":

                self.player2.hand.pop(random.randrange(len(self.player1.hand)))
                self.score["p2"] += 1

        # Exibição do novo status
        print(f"{card_player1}")
        print(f"{card_player2}")
        self.player1.showStatus()
=======
# Imports
from player import Player
from static import conflicts
import random

# Classe para resolver o conflito. O principal é entregar um multiplicador de dano.
class CardResolver:
    def __init__(self):
        pass

    # Adicionando os multiplicadores de resistências e fraquezas
    def apply_resistances_and_weaknesses(self, base_damage, attack_type, defender_robot):
        
        # Conta quantas vezes o tipo aparece nas resistências/fraquezas
        weakness_count = defender_robot.weaknesses.count(attack_type)
        resistance_count = defender_robot.resistances.count(attack_type)

        # Aplica multiplicadores cumulativos. Cada contador significa um adicional de +0.5 (50%)
        adjusted_damage = base_damage * (1 + (0.5 * weakness_count)) - (1 + (0.5 ** resistance_count))

        return adjusted_damage
    
    # Método para resolver os conflitos de cartas
    def resolveConflict(self, card1, card2):
        # Pega a classe de cada carta jogada
        c1 = card1["class"]
        c2 = card2["class"]
        # Entrega um resultado baseado na tabela de conflitos.
        base_outcome = conflicts[c1][c2]

        # Dicionário base que entrega o resultado
        result = {
            "winner": None,
            "action": None,
            "multiplier": None
        }

        # Casos Básicos - Sem cartas especiais
        if base_outcome == "ATTACK":
            result["winner"] = "p1" if c1 == "ATTACK" else "p2"
            result["action"] = base_outcome
            result["multiplier"] = card1["meta"]["atk"] - card2["meta"]["def"] if c1 == "ATTACK" else card2["meta"]["atk"] - card1["meta"]["def"]
        elif base_outcome == "GUARD":
            result["winner"] = "p1" if c1 == "GUARD" else "p2"
            result["action"] = base_outcome
            result["multiplier"] = card1["meta"]["def"] - card2["meta"]["atk"] if c1 == "GUARD" else card2["meta"]["def"] - card1["meta"]["atk"]
        elif base_outcome == "CLINCH":
            result["winner"] = "p1" if c1 == "CLINCH" else "p2"
            result["action"] = base_outcome
            result["multiplier"] = card1["meta"]["cli"] - card2["meta"]["def"] if c1 == "CLINCH" else card2["meta"]["cli"] - card1["meta"]["def"]

        # Casos especiais
        result = self.handle_special_cases(card1, card2, result)

        return result

    def handle_special_cases(self, card1, card2, result):

        c1_name, c2_name = card1["name"], card2["name"]

        # Strong Attack causa double damage se o oponente clinchar
        if c1_name == "Strong Attack" and card2["class"] == "CLINCH":
            result["multiplier"] = 2

        if c2_name == "Strong Attack" and card1["class"] == "CLINCH":
            result["multiplier"] = 2

        # Special Guard bloqueia tudo
        if c1_name == "Special Guard":
            result["multiplier"] = 0

        if c2_name == "Special Guard":
            result["multiplier"] = 0

        return result

class GameRuler:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.resolver = CardResolver()
        self.score = {"p1": 0, "p2": 0}

    # Método para 1 turno
    def playTurn(self):
        # Exibição do status atual
        self.player1.showStatus()
        self.player2.showStatus()

        # Compra de cartas
        while len(self.player1.hand) < 4:
            self.player1.getCard(1)

        while len(self.player2.hand) < 4:
            self.player2.getCard(1)

        # Escolhendo a carta do jogador 1
        card_player1 = self.player1.playCard()

        # Escolhendo a carta do jogador 2
        card_player2 = self.player2.playCard()

        # Resolução de ações
        result = self.resolver.resolveConflict(card_player1, card_player2)

        # Cálculo do dano
        if result["action"] == "ATTACK":
            if result["winner"] == "p1":

                base_damage = self.player1.initial_attack
                modified_damage = base_damage * result["multiplier"]
                full_damage = self.resolver.apply_resistances_and_weaknesses(modified_damage, card_player1["type"], self.player2.robot)
                self.player2.initial_HP -= full_damage - (self.player2.initial_defense * 0.5)
                self.score["p1"] += 1

            elif result["winner"] == "p2":

                base_damage = self.player2.initial_attack
                modified_damage = base_damage * result["multiplier"]
                full_damage = self.resolver.apply_resistances_and_weaknesses(modified_damage, card_player2["type"], self.player1.robot)
                self.player1.initial_HP -= full_damage - (self.player1.initial_defense * 0.5)
                self.score["p2"] += 1

        elif result["action"] == "GUARD":
            if result["winner"] == "p1":

                base_damage = self.player1.initial_defense
                modified_damage = base_damage * result["multiplier"]
                full_damage = self.resolver.apply_resistances_and_weaknesses(modified_damage, card_player1["type"], self.player2.robot)
                self.player2.initial_HP -= full_damage - (self.player2.initial_defense * 0.9)
                self.score["p1"] += 1

            elif result["winner"] == "p2":

                base_damage = self.player2.initial_defense
                modified_damage = base_damage * result["multiplier"]
                full_damage = self.resolver.apply_resistances_and_weaknesses(modified_damage, card_player2["type"], self.player1.robot)
                self.player1.initial_HP -= full_damage - (self.player1.intial_defense * 0.9)
                self.score["p2"] += 1

        elif result["action"] == "CLINCH":
            if result["winner"] == "p1":

                self.player2.hand.pop(random.randrange(len(self.player2.hand)))
                self.score["p1"] += 1

            elif result["winner"] == "p2":

                self.player2.hand.pop(random.randrange(len(self.player1.hand)))
                self.score["p2"] += 1

        # Exibição do novo status
        print(f"{card_player1}")
        print(f"{card_player2}")
        self.player1.showStatus()
>>>>>>> 3933bfcd65d48d4548136038859706bdf05ff8ed
        self.player2.showStatus()