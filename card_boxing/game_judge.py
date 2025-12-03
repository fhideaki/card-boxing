# Imports
from player import Player
from deck import Deck
from robot import Robot
from static import conflicts_table
from ui_manager import UIManager
from typing import Dict, Any, Tuple, List, TYPE_CHECKING
import random

# Criando uma classe "juiz" para conferir os status do deck e do robô de cada jogador.
class GameJudge:
    def __init__(self, ui_manager: UIManager, damage_calculator):
        # Inicializando o gerenciador de UI
        self.ui = ui_manager
        self.ui.printMessage('Judge created.')

        # Inicializando a calculadora de danos
        self.damage_calculator = damage_calculator

        # Dados temporários (renovados por turno)
        self.current_turn_actions = {}
        self.turn_damage_log = {}

        # Controladores de jogo
        self.turn = 0
        self.round = 0
        self.score = {}

    # Métodos auxiliares
        # Método para printar as mensagens para o jogo
    def log_message(self, message):
        self.ui.printMessage(f"Turn {self.turn} - {message}")
        
    # Métodos para registrar informações
        # Registrar carta lançada
    def register_action(self, player, card):
        # Registra a carta jogada
        self.current_turn_actions[player] = card

        # Mostra a mensagem
        self.log_message(f"Judge: {player.name} played '{card.get('name')}'.") 

        # Registrar o dano que vai ser aplicado
    def register_damage_dealt(self, player, damage):
        self.turn_damage_log[player] = damage

        # Limpa os registros do turno
    def clear_turn_records(self):
        self.turn_damage_log = {}
        self.current_turn_actions = {}

        # Aumentar 1 turno
    def increase_turn(self):
        self.turn += 1

        # Aumentar 1 round
    def increase_round(self):
        self.round += 1
        
        # Criar o score do jogo
    def create_score(self, player1, player2):
        self.score[player1] = 0
        self.score[player2] = 0
        
        # Aumentar 1 ponto para o jogador
    def give_point(self, player):
        self.score[player] += 1
        
        # Retornar o vencedor por score
    def return_score_winner(self):
        return max(self.score, key=self.score.get)

    # Métodos para checagem de ações
        # Conferir se clinch foi utilizado
    def has_used_clinch(self, player):
        return self.check_card_class(player, "clinch")

        # Conferir qual o tipo da carta utilizada
    def check_card_class(self, player, card_class) -> bool:
        if player in self.current_turn_actions:
            card = self.current_turn_actions[player]
            return card.get("class") == card_class
        return False
        
        # Conferir se a ação causou dano
    def check_successful_attack(self, player) -> bool:
        return any(damage > 0 for damage in self.turn_damage_log.values())

        # Checa se o jogador não pode comprar cartas no próximo turno
    def is_draw_locked(self, player) -> bool:
        return player.draw_blocked

    # Métodos que alteram estado
        # Método para definir status de invulnerável
    def set_invulnerability(self, player):
        player.is_invincible = True
        self.log_message(f"Judge: {player.name} invulnerability enabled!")
        
        # Método para remover status de invulnerável
    def reset_invulnerability(self, player):
        player.is_invincible = False
        self.log_message(f"Judge: {player.name} invulnerability disabled!")

        # Método para retornar True se estiver invulnerável
    def is_invulnerable(self, player):
        return player.is_invincible

        # Método para determinar quem ganha a disputa das cartas
    def determine_conflict(self, card_p1: Dict[str, Any], card_p2: Dict[str, Any]) -> Dict[str, Any]:
        
        # Obtém a classe da carta
        class_p1 = card_p1.get('class')
        class_p2 = card_p2.get('class')
        
        # Cria a chave de busca 
        key = (class_p1, class_p2)
        
        # Busca o resultado na tabela
        result = conflicts_table.get(key)
        
        return result

    # Método que retorna um dicionário com as informações do conflito antes de calcular dano e com base no resultado das cartas.    
    def return_conflict_result(self, player1, player2, card_p1, card_p2, result):

        winner = None
        loser = None

        if result['winner'] == 'p1':
            type = 'win'
            winner = player1
            loser = player2

        elif result['winner'] == 'p2':
            type = 'win'
            winner = player2
            loser = player1

        elif result['winner'] == 'tie':
            if result['winning_class'] == 'attack':
                type = 'attack_draw'
            elif result['winning_class'] == 'clinch':
                type = 'clinch_draw'
            elif result['winning_class'] == 'guard':
                type = 'guard_draw'

        result = {
            'type': type,

            'winner': winner,
            'loser': loser,

            'p1': {
                'player': player1,
                'card': card_p1,
                'class': card_p1['class'],
                'effect': card_p1['effect'],
                'speed': player1.initial_agility
            },

            'p2': {
                'player': player2,
                'card': card_p2,
                'class': card_p2['class'],
                'effect': card_p2['effect'],
                'speed': player2.initial_agility
            }
        }

        return result
    
    # Método para resolver o conflito de acordo com o dicionário passado como argumento
    def resolve_conflict_after_result(self, conflict_result):
        # Variáveis iniciais
        type = conflict_result['type']

        # Dicionário dos jogadores
        p1 = conflict_result['p1']
        p2 = conflict_result['p2']

        # Acesso aos objetos Player
        player1 = p1['player']
        player2 = p2['player']

        # No caso de não empate
        winner = conflict_result['winner']
        loser = conflict_result[ 'loser']

        # No caso de vitória
        if type == 'win':
            self.resolve_win(conflict_result)
        elif type == 'attack_draw':
            self.resolve_attack_draw(conflict_result)
        elif type == 'clinch_draw':
            self.resolve_clinch_draw(conflict_result)
        elif type == 'guard_draw':
            self.resolve_guard_draw(conflict_result)

    # Método que bloqueia a compra de cartas por 1 turno (efeito clinch)
    def set_draw_lock(self, player):
        player.draw_blocked = True
        
    # Método que bloqueia a compra de cartas por 1 turno (efeito clinch)
    def reset_draw_lock(self, player):
        player.draw_blocked = False

    #     # Método para aplicar dano
    # def apply_damage(self, player, damage):
    #     # Checa invulnerabilidade
    #     if player.is_invincible:
    #         self.log_message(f"Judge: {player.name} is invulnerable, no damage applied.")
    #         return True

    #     # Aplicando dano ao robô
    #     if damage > 0:
    #         player.initial_HP -= damage
    #         self.log_message(f"Judge: {player.name} received {damage} damage! HP left: {player.initial_HP}")

        # Método para dropar um slot da mão do jogador
    def drop_hand_slot(self, player, num_slots):
        current_limit = player.max_hand_slots
        new_limit = max(0, current_limit - num_slots)

        player.max_hand_slots = new_limit
        
        self.log_message(f"Judge: Cards in hand limit of the {player.name} player dropped {num_slots}. New limit: {player.max_hand_slots}.")
        
    # Método para checar a HP do robô.
    def is_knocked_out(self, player) -> bool:
        # Retorna True se a vida estiver menor ou igual a 0
        return player.initial_HP <= 0

    # Método para checar se o jogador tem cartas disponíveis no deck
    def is_deck_out(self, player) -> bool:
        # Retorna True se o jogador não tiver cartas jogáveis
        return len(player.game_deck) <= 0
    
    # Método para checar se o jogador tem cartas disponíveis na mão
    def is_hand_out(self, player) -> bool:
        # Retorna True se o jogador não tiver cartas jogáveis
        return len(player.hand) <= 0
    
    # Método para checar se o jogador está incapacitado
    def is_incapacitaded(self, player) -> bool:
        return self.is_deck_out(player) and self.is_hand_out(player)

    # Método para retornar o custo de cartas pagas por queda
    def apply_ko_cost(self, player):
        fall_counter = player.fall_counter

        # Calculando o custo que deve ser pago a cada queda 
        fall_cost = (fall_counter + 1) * 2
        player.fall_counter += 1

        # Retorna o custo que deve ser pago e modifica o contador de quedas do jogador.
        return int(fall_cost)

    # Método para aplicar KO
    def apply_ko(self, player, fall_cost: int) -> bool:
        # Retorna True se o número de cartas restantes no baralho for menor do que o custo.
        return len(player.game_deck) < fall_cost
    
    # Método para declarar vencedor
    def declare_winner(self, winner, reason):
        self.log_message("---GAME OVER---")
        self.log_message(f"Winner: {winner.name}")
        self.log_message(reason)
        
        raise SystemExit("Game Over, Thanks for playing!")
        
    # Método para verificar se o jogador caiu, e se ele consegue se levantar
    def player_down(self, attacker, target):
        if self.is_knocked_out(target):
            print(f'{target.name} is down!')

            if self.is_incapacitaded(target):
                self.declare_winner(attacker, "K.O.")
            else:
                ko_cost = self.apply_ko_cost(target)
                print(f'Cost to get up {ko_cost}')
                if self.apply_ko(target, ko_cost):
                    self.declare_winner(attacker, "K.O.")
                else:
                    if not self.discard_from_deck(target, ko_cost):
                        self.declare_winner(attacker, "K.O.")
                    else: 
                        self.discard_from_deck(target, ko_cost)
        return

    # Método para resetar o contador de quedas
    def reset_player_falls(self, player):
        player.falls = 0

    # Método para somar uma queda ao contador
    def add_fall(self, player):
        player.falls +=1

    # Método para conferir se o jogador atingiu o número de quedas limite no round.
    def check_falls(self, player, num_falls) -> bool:
        # Retorna True se o jogador acumular 3 quedas no round.
        return player.falls == num_falls
    
    # Método para descartar tanto da mão quanto do deck
    def discard_from_deck(self, player, num_cards):
        total_cards = len(player.game_deck) + len(player.hand)

        # Se já não há cartas o suficiente para serem descartadas
        if num_cards >= total_cards:
            self.log_message(f"Player {player.name} does not have enough cards to discard.")
            return False
        
        # Descartando primeiro do deck
        cards_to_discard_from_deck = num_cards
        print(f'Cartas a descartar do deck {cards_to_discard_from_deck}')

        for card in range(cards_to_discard_from_deck):
            random_card = random.choice(player.game_deck)
            player.game_deck.remove(random_card)
            player.graveyard.append(random_card)

        # Descarte da mão se necessário
        remaining_to_discard = num_cards - cards_to_discard_from_deck

        cards_to_discard_from_hand = 0

        if remaining_to_discard > 0:
            cards_to_discard_from_hand = remaining_to_discard

            for card in range(cards_to_discard_from_hand):
                random_card = random.choice(player.hand)
                player.hand.remove(random_card)
                player.graveyard.append(random_card)
        self.log_message(f"Player {player.name} discarded {cards_to_discard_from_deck} cards from deck and {cards_to_discard_from_hand} cards from hand.")
        return True    
        
    # Método para retirar uma carta da mão do jogador
    def discard_from_hand(self, player, num_cards):
        if num_cards < len(player.hand):
            for card in range(num_cards):
                random_card = random.choice(player.hand)
                player.hand.remove(random_card)
                player.graveyard.append(random_card)
            self.log_message(f"Player {player.name} discarded {num_cards} cards.")
        else:
            for card in len(player.hand):
                random_card = random.choice(player.hand)
                player.hand.remove(random_card)
                player.graveyard.append(random_card)
            self.log_message(f"Player {player.name} discarded {num_cards} cards.")

    # Reseta o placar
    def reset_score(self, player):
        player.score = 0
    
    # Adiciona um ponto ao placar do jogador
    def add_point(self, player):
        player.score += 1