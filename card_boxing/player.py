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

        # Número máximo de cartas na mão
        self.max_hand_slots = 3
        # Atributo privado com o mínimo de uma carta na mão
        self._max_hand_slots: int = 1

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

        # Contador de Quedas Totais
        self.fall_counter = 0

        # Contador de Quedas por Round - (Vai ser resetado com o round)
        self.falls = 0
        
        # Modificador de invencibilidade
        self.is_invincible = False
        
        # Modificador de compra de cartas
        self.draw_blocked = False

    # Permite ler o valor dos slots
    @property 
    def max_hand_slots(self) -> int:
        return self._max_hand_slots
    
    # Valida que o valor do atributo nunca seja menor do que 1
    @max_hand_slots.setter
    def max_hand_slots(self, value: int):
        
        if value < 1:
            self.ui.printMessage(f"Minimum slots for player {self.name}'s hand: 1 Slot")
            self._max_hand_slots = 1
        else:
            self._max_hand_slots = value
            
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
        # Retorna o game_deck já com todas as cartas inseridas
        return self.game_deck
    
    # Checa se o game deck tem n cartas possíveis para compra
    def checkGameDeck(self, quantity):
        # Retorna True se existe mais cartas para serem compradas no game deck do que o que foi pedido
        return len(self.game_deck) >= quantity
    
    # Embaralha o deck
    def shuffleDeck(self):
        return random.shuffle(self.game_deck)

    # Compra n cartas
    def getCard(self, num_of_cards):
        # Checagem se o game deck tem n cartas disponíveis
        if not self.checkGameDeck(num_of_cards):
            # Se não tiver, ele vai transformar num_of_cards na mesma quantidade de cards restantes.
            num_of_cards = len(self.game_deck)
            # Avisa quantas cartas estão disponíveis para compra no caso do game deck ser insuficiente.
            self.ui.printMessage(f"Only {num_of_cards} cards available. ")
        
        # Compra de cartas
        cards_drawn = 0
        while cards_drawn < num_of_cards:
            # Checa se a mão está cheia
            if len(self.hand) >= self.max_hand_slots:
                self.ui.printMessage(f"Player {self.name}'s hand is full!'")
                break
                
            # Checa se o deck ficou vazio durante a compra
            if not self.game_deck:
                break

            # Compra a carta do topo do baralho (índice 0)
            card = self.game_deck.pop(0)
            self.hand.append(card)
            
            cards_drawn += 1
        
        return True

    # Mostra a mão
    def showHand(self):
        hand_table = self.ui.createCardsTable(f"Player {self.name}'s Hand")
        
        for i in self.hand:
            self.ui.addCardRow(hand_table,i)
            
        self.ui.console.print(hand_table)

    # Mostra o cemitério
    def showGraveyard(self):
        graveyard_table = self.ui.createCardsTable(f"Player {self.name}'s Graveyard")
        
        for i in self.graveyard:
            self.ui.addCardRow(graveyard_table,i)
            
        self.ui.console.print(graveyard_table)
            
    # Escolhe a carta
    def chooseCard(self):
        self.showHand()
        chosen_card = int(input("Choose a card:"))
        return self.hand[chosen_card]
    
    def playCard(self):
        chosen_card = self.chooseCard()
        self.hand.remove(chosen_card)
        self.graveyard.append(chosen_card)
        return chosen_card
    
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
        
