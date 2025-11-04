<<<<<<< HEAD
# Imports
from robot import Robot
from deck import Deck
from rich.console import Console
from rich.table import Table
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

    # Método para criar a estrutura da tabela de partes
    def _create_cards_table(self, title):
        # Cria a tabela
        cards_table = Table(title=title)
        
        #Cria as colunas da tabela
        cards_table.add_column("ID")
        cards_table.add_column("Card Name")        
        cards_table.add_column("Class")  
        cards_table.add_column("Type")
        cards_table.add_column("Description")

        return cards_table
    
    # Método para formatar cada linha da tabela
    def _add_card_row(self, cards_table, card):
        
#         resistances_display = ", ".join(part["resistances"]) if part["resistances"] else "N/A"
#         weaknesses_display = ", ".join(part["weaknesses"]) if part["weaknesses"] else "N/A"
        
        cards_table.add_row(
            str(card["id"]),
            card["name"],
            card["class"],
            card["type"],
            card["description"]
#             ", ".join(part["resistances"]) if part["resistances"] else "N/A",
#             ", ".join(part["weaknesses"]) if part["weaknesses"] else "N/A"
        )

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
        deck_table = self._create_cards_table(f"Player {self.name}'s Deck")
        # Carrega a tabela
        for card in self.game_deck:
            self._add_card_row(deck_table, card)
        
        self.player_console.print(deck_table)
        
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
        hand_table = self._create_cards_table(f"Player {self.name}'s Hand")
        
        for i in self.hand:
            self._add_card_row(hand_table,i)
            
        self.player_console.print(hand_table)
            
    # Escolhe a carta
    def playCard(self):
        self.showHand()
        played_card = int(input("Choose a card:"))
        return self.hand[played_card]
    
    # Mostra o status atual
    def showStatus(self):
        # Cria a tabela
        stats_table = Table(title="Current Stats Table")
                
        #Cria as colunas da tabela
        stats_table.add_column("HP")
        stats_table.add_column("Con")        
        stats_table.add_column("Str")  
        stats_table.add_column("Agi")
        stats_table.add_column("Def")
        stats_table.add_column("Atk")
        stats_table.add_column("Cli")
        
        # Monta a tabela
        stats_table.add_row(
            f"{self.initial_HP}/{self.robot.HP}",
            f"{self.initial_constitution}/{self.robot.constitution}",
            f"{self.initial_strength}/{self.robot.strength}",
            f"{self.initial_agility}/{self.robot.agility}",
            f"{self.initial_defense}/{self.robot.defense}",
            f"{self.initial_attack}/{self.robot.attack}",
            f"{self.initial_clinch}/{self.robot.clinch}"
        )

        self.player_console.print(stats_table)
        
=======
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
>>>>>>> 3933bfcd65d48d4548136038859706bdf05ff8ed
