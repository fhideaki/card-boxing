from static import card_list, robot_archetypes

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
        deck_source = robot_archetypes[archetype]["deck"]

        for card_id, qty in deck_source["base_cards"].items():
            for _ in range(qty):
                self.deck.append(findCardById(cards, card_id))

        for card_id, qty in deck_source["special_cards"].items():
            for _ in range(qty):
                self.deck.append(findCardById(cards, card_id))