# Imports
from static import card_list

# Método para encontrar uma carta pelo ID
def findCardById(card_list, card_id):
    for card_data in card_list:
        if card_data.get("id") == card_id:
            return card_data
    return None

# Criando a classe deck.
class Deck:
    def __init__(self, archetype):

        self.deck = []

        cards = card_list

        # Criando o deck básico do jogador com 3 cartas de cada tipo.
        for i in range(3):
            self.deck.append(
                findCardById(cards, 2)
                )
        for i in range(3):
            self.deck.append(
                findCardById(cards, 1)
                )
        for i in range(3):
            self.deck.append(
                findCardById(cards, 3)
                )
        
        # Colocando uma carta especial para cada arquétipo diferente
        if archetype == "ATK":
            for i in range(2):
                self.deck.append(
                    findCardById(cards, 4)
                    )
        elif archetype == "DEF":
            for i in range(2):
                self.deck.append(
                    findCardById(cards, 5)
                    )
        elif archetype == "BAL":
            self.deck.append(
                findCardById(cards, 4)
                )
            self.deck.append(
                findCardById(cards, 5)
                )