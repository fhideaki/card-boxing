# Imports
from robot import Robot
from deck import Deck
from rich.console import Console
from rich.table import Table
from ui_manager import UIManager
import random

# Criando a classe jogador
class Player:
    def __init__(self, name, robot_name, archetype, ui_manager: UIManager):
        self.name = name

        self.ui = ui_manager
        
        # Robô do jogador
        self.robot = Robot(archetype, self.ui, robot_name)

        # Deck base do jogador
        self.deck = Deck(archetype)

        # Cartas descartadas
        self.graveyard = []

        # Mão do jogador
        self.hand = []

        # Deck completo do jogador
        self.game_deck = []
        
        # Console para printar as cartas
        self.player_console = Console()

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
        for part in self.robot.slots.values():
            if part is not None:
                
                special_card = part.get("special_card")
                
                if special_card and special_card.get("id") is not None:
                    self.deck.deck.append(special_card)

    # Cria o deck disponível para jogar, retorna uma lista
    def setDeck(self):
        
        # Adiciona as cartas especiais
        self.addSpecialCards()
        self.game_deck = self.deck.deck
        
        # Cria a tabela de cartas
        deck_table = self.ui.createCardsTable(f"Player {self.name}'s Deck")
        # Carrega a tabela
        for card in self.game_deck:
            self.ui.addCardRow(deck_table, card)
        
        self.ui.console.print(deck_table)
        
        return self.game_deck
    
    # Embaralha o deck
    def shuffleDeck(self):
        return random.shuffle(self.game_deck)

    # Compra n cartas
    def getCard(self, num_of_cards):

        for i in range(num_of_cards):
            # Colocando a carta na mão do jogador
            self.hand.append(self.game_deck[i])
            # Removendo a carta do deck para compra
            self.game_deck.pop(i)
        return True

    # Mostra a mão
    def showHand(self):
        hand_table = self.ui.createCardsTable(f"Player {self.name}'s Hand")
        
        for i in self.hand:
            self.ui.addCardRow(hand_table,i)
            
        self.ui.console.print(hand_table)
            
    # Escolhe a carta
    def playCard(self):
        self.showHand()
        played_card = int(input("Choose a card:"))
        return self.hand[played_card]
    
    # Mostra o status atual
    def showCurrentStatus(self):
        # Cria a tabela
        current_stats_table = self.ui.createCurrentStatsTable(f"{self.name}'s {self.robot.robot_name} Robot Stats")
        
        # Monta a tabela
        current_stats_list = [
            f"{self.initial_HP}/{self.robot.HP}",
            f"{self.initial_constitution}/{self.robot.constitution}",
            f"{self.initial_strength}/{self.robot.strength}",
            f"{self.initial_agility}/{self.robot.agility}",
            f"{self.initial_defense}/{self.robot.defense}",
            f"{self.initial_attack}/{self.robot.attack}",
            f"{self.initial_clinch}/{self.robot.clinch}"
        ]

        self.ui.addCurrentStatsRow(current_stats_table, current_stats_list)