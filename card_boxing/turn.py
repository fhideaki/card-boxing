from effects import *
from player import Player
from game_judge import GameJudge
from damage_calculator import DamageCalculator

# Criando a classe Game - Ela vai iniciar uma partida
class Turn:
    def __init__(self, player1, player2, gamejudge, damagecalculator):
        self.player1 = player1
        self.player2 = player2
        self.gamejudge = gamejudge
        self.damagecalculator = damagecalculator
    
# Estrutura do turno
    # Primeira fase - Resetando as variáveis
    def execute_first_phase(self):
        # Juiz limpa o log de atividades
        self.gamejudge.clear_turn_records()
        
        # Jogadores perdem invencibilidade
        self.gamejudge.reset_invulnerability(self.player1)
        self.gamejudge.reset_invulnerability(self.player2)
        
        # Se ambos não possuírem cartas em mãos e não possuírem cartas para comprar - O jogo acaba e o resultado vai para os pontos.
        p1_out = self.gamejudge.is_incapacitaded(player1)
        p2_out = self.gamejudge.is_incapacitaded(player2)
        
        if p1_out and p2_out:
            score = self.gamejudge.score
            for player, player_score in score:
                self.gamejudge.log_message(f"The {player.name} has scored {player_score} points.")
            winner = self.gamejudge.return_score_winner()
            self.gamejudge.declare_winner(winner, "Score")
   
            # Se nao possuir cartas em mãos E não possuir cartas para comprar - O jogador está derrotado.
        if p1_out and not p2_out:
            reason = f"{self.p1.name} is incapacitaded to fight!"
            self.gamejudge.declare_winner(self.player2, "Incapacitated Opponent.")        
        if p2_out and not p1_out:
            reason = f"{self.p2.name} is incapacitaded to fight!"
            self.gamejudge.declare_winner(self.player1, "Incapacitated Opponent.")
            
    
    # Segunda fase - Executando o começo do round        
    def execute_second_phase(self):        
        # Jogadores compram as cartas se forem permitidos.
        p1_draw_block = self.player1.draw_blocked
        p2_draw_block = self.player2.draw_blocked
        
        # Se o jogador 1 não estiver bloqueado
        if not p1_draw_block:
            # E se o jogador 1 tiver cartas na mão menos do que os slots da mão livres
            if len(self.player1.hand) < self.player1.max_hand_slots:
                self.player1.getCard(1)

        # Se o jogador 2 não estiver bloqueado
        if not p2_draw_block:
            # E se o jogador 1 tiver cartas na mão menos do que os slots da mão livres
            if len(self.player2.hand) < self.player2.max_hand_slots:
                self.player2.getCard(1)
                
        # Ambos os jogadores escolhem uma carta para jogar
        p1_card = self.player1.playCard()
        p2_card = self.player2.playCard()
        
        # Juiz registra ambas as cartas no turno
        self.gamejudge.register_action(self.player1, p1_card)
        self.gamejudge.register_action(self.player2, p2_card)
        
    # Terceira fase - Executando o conflito entre as cartas
    def execute_third_phase(self):
        # As cartas são colocadas em análise.
            # Criando uma instância da classe Effect
        effects = Effect()

            # Criando as cartas que foram jogadas de acordo com o que o juiz registrou
        card_player1 = self.gamejudge.current_turn_actions[self.player1]
        card_player2 = self.gamejudge.current_turn_actions[self.player2]
        
            # Instanciando os efeitos das cartas em jogo
        card_player1_effect = card_player1['effect']()
        card_player2_effect = card_player2['effect']()
        
            # Analisando o resultado do conflito entre as classes das cartas
        card_conflict_result = self.gamejudge.determine_conflict(card_player1, card_player2)
        
            # Primeira análise condicional de efeitos especiais
            
            
                # Aplicação dos efeitos
        # Resolução dos conflitos das cartas (Jan Ken Pon)
            # Segunda análise dos efeitos condicionais
                # Aplicação dos efeitos
            # Aplicação do resultado de acordo com as cartas
                # Aplicação do dano, caso houver
    # Classe especial de checagem - No caso de aplicação de dano
        # Checar o dano recebido vs Vida disponível
        # Checar se houve queda (vida chegou a 0)
        # Checar se existem cartas disponíveis para pagar o custo
        # Checar se 
