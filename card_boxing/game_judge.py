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
    
    def return_conflict_result(self, player1, player2, card_p1, card_p2, result):
        # Essa função precisa retornar todas as variáveis já com os cálculos prontos para o turno continuar.
        # Estágio 0 - Definindo quem é o ganhador e quem é o perdedor do conflito.
        if result['winner'] == 'p1':
            winner = player1
            loser = player2
            winning_card = card_p1
            losing_card = card_p2
            winning_class = card_p1['class']
            losing_class = card_p2['class']
            winning_effect = card_p1.effect()
            losing_effect = card_p2.effect()

        elif result['winner'] == 'p2':
            winner = player2
            loser = player1
            winning_card = card_p2
            losing_card = card_p1
            winning_class = card_p2['class']
            losing_class = card_p1['class']
            winning_effect = card_p2.effect()
            losing_effect = card_p1.effect()

    # Método que bloqueia a compra de cartas por 1 turno (efeito clinch)
    def set_draw_lock(self, player, turns):
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