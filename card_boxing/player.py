# Imports
from robot import Robot
from deck import Deck
import random

# Criando a classe jogador
class Player:
    def __init__(self, name, archetype):
        self.name = name

        # Robo do jogador
        self.robot = Robot(archetype)

        # Deck base do jogador
        self.deck = Deck(archetype)

        # Cartas descartadas
        self.graveyard = []

        # Mão do jogador
        self.hand = []

        # Deck completo do jogador
        self.game_deck = []

        # Atributos do jogador
        self.initial_constitution = self.robot.constitution
        self.initial_strength = self.robot.strength
        self.initial_agility = self.robot.agility
        self.initial_HP = self.robot.HP
        self.initial_defense = self.robot.defense
        self.initial_attack = self.robot.attack
        self.initial_clinch = self.robot.clinch

    # Adiciona as cartas especiais, caso existam
    def addSpecialCards(self):
        for i in self.robot.part_list:
            if i["special_card"]:
                self.deck.deck.append(i["special_card"])

    # Cria o deck disponível para jogar, retorna uma lista
    def setDeck(self):
        
        # Adiciona as cartas especiais
        self.addSpecialCards()
        self.game_deck = self.deck.deck

        return self.game_deck

    # Compra n cartas
    def getCard(self, num_of_cards):

        for i in range(num_of_cards):
            # Escolhendo um índice aleatório das cartas disponíveis
            random_index = random.randrange(len(self.game_deck))

            # Transformando o item em uma carta
            chosen_card = self.game_deck[random_index]

            # Colocando a carta na mão do jogador
            self.hand.append(chosen_card)
            # Removendo a carta do deck para compra
            self.game_deck.pop(random_index)

    # Mostra a mão
    def showHand(self):
        for i in self.hand:
            print(i)
    
    # Escolhe a carta
    def playCard(self):
        self.showHand()
        played_card = int(input("Choose a card:"))
        return self.hand[played_card]
    
    # Mostra o status atual
    def showStatus(self):
        print(f"Current HP: {self.initial_HP}")
        print(f"Current Constitution: {self.initial_constitution}")
        print(f"Current Strength: {self.initial_strength}")
        print(f"Current Agility: {self.initial_agility}")
        print(f"Current Defense: {self.initial_defense}")
        print(f"Current Attack: {self.initial_attack}")
        print(f"Current Clinch: {self.initial_clinch}")