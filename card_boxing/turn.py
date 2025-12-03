from effects import *
from player import Player
from game_judge import GameJudge
from damage_calculator import DamageCalculator
import random

# Criando a classe Game - Ela vai iniciar uma partida
class Turn:
    def __init__(self, player1: Player, player2: Player, gamejudge, damagecalculator):
        self.player1 = player1
        self.player2 = player2
        self.gamejudge = gamejudge
        self.damagecalculator = damagecalculator
        self.gamejudge.create_score(self.player1, self.player2)
        print('Turn created.')

    def game_start(self):
        # Embaralhar o deck dos jogadores
        print('-----------------------Game Start-----------------------')

        self.player1.shuffleDeck()
        print('P1 Deck shuffled')
        self.player2.shuffleDeck()
        print('P2 Deck shuffled')

        # Comprar 3 cartas 
        self.player1.getCard(3)
        print(self.player1.hand)
        print('P1 drew 3 cards')
        self.player2.getCard(3)
        print(self.player2.hand)
        print('P2 drew 3 cards')


# Estrutura do turno
    # Primeira fase - Resetando as variáveis
    def execute_first_phase(self):
        print('-----------------------Phase 1 Start-----------------------')
        # Juiz limpa o log de atividades
        self.gamejudge.clear_turn_records()
        print(self.gamejudge.current_turn_actions)
        print('Records cleaned.')
        
        # Jogadores perdem invencibilidade
        self.gamejudge.reset_invulnerability(self.player1)
        self.gamejudge.reset_invulnerability(self.player2)
        
        # Se ambos não possuírem cartas em mãos e não possuírem cartas para comprar - O jogo acaba e o resultado vai para os pontos.
        p1_out = self.gamejudge.is_incapacitaded(self.player1)
        print(p1_out)
        p2_out = self.gamejudge.is_incapacitaded(self.player2)
        print(p2_out)

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
        print('-----------------------Phase 2 Start-----------------------')      
        # Jogadores compram as cartas se forem permitidos.
        p1_draw_block = self.player1.draw_blocked
        print(p1_draw_block)
        p2_draw_block = self.player2.draw_blocked
        print(p2_draw_block)
        
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
        print(self.gamejudge.current_turn_actions)
        self.gamejudge.register_action(self.player2, p2_card)
        print(self.gamejudge.current_turn_actions)

    # Terceira fase - Executando o conflito entre as cartas
    def execute_third_phase(self):
        print('-----------------------Phase 3 Start-----------------------')
        # As cartas são colocadas em análise.

            # Criando as cartas que foram jogadas de acordo com o que o juiz registrou
        card_player1 = self.gamejudge.current_turn_actions[self.player1]
        print(f'Card Player 1 - {card_player1}')
        card_player2 = self.gamejudge.current_turn_actions[self.player2]
        print(f'Card Player 2 - {card_player2}')
        
        # Criando as variáveis que vão ser utilizadas e modificadas durante o turno.
            # Player 1
        p1_name = self.player1.name
        p1_weaknesses_multiplier = self.damagecalculator.check_weaknesses(card_player2, self.player1)
        p1_resistances_multiplier = self.damagecalculator.check_resistances(card_player2, self.player1)
        p1_base_defense = self.damagecalculator.get_base_defense(self.player1)
        p1_current_action = card_player1['class']

            # Player 2
        p2_name = self.player2.name
        p2_weaknesses_multiplier = self.damagecalculator.check_weaknesses(card_player1, self.player2)
        p2_resistances_multiplier = self.damagecalculator.check_resistances(card_player1, self.player2)
        p2_base_defense = self.damagecalculator.get_base_defense(self.player2)
        p2_current_action = card_player2['class']
            
        # Resolução dos conflitos das cartas (Jan Ken Pon)
        conflict_result = self.gamejudge.determine_conflict(card_player1, card_player2)
        print(conflict_result)

        # Se a carta for Special Guard, pula a parte de dano porque nada vai ser aplicado.
        if card_player1['name'] == 'Special Guard' or card_player2['name'] == 'Special Guard':
            print('Um jogador usou Special Guard')
            
            print(self.player1.initial_HP)
            print(self.player2.initial_HP)
            pass
        # No caso de duas defesas
        elif conflict_result['winning_class'] == 'none':
            print('Ambos jogadores usaram defesa')
            pass
    
            print(self.player1.initial_HP)
            print(self.player2.initial_HP)
        # No caso de uma defesa ganhar
        elif conflict_result['winning_class'] == 'guard':
            # Para uma defesa ganhar, a outra carta necessariamente é um ataque.
            # No caso da carta de defesa for a carta com efeito StopHittingYourself
            print('Uma defesa ganhou')
            if card_player1['name'] == 'Iron Guard':
                print('P1 usou Iron Guard')
                reflected_damage = 0.20 * p1_base_defense
                self.player2.initial_HP -= reflected_damage
                self.gamejudge.log_message(f"Player 1 - {p1_name} - used Iron Guard! Reflected {reflected_damage} points of damage!")
                self.gamejudge.player_down(self.player1, self.player2)
                print(self.player1.initial_HP)
                print(self.player2.initial_HP)

            elif card_player2['name'] == 'Iron Guard':
                print('P2 usou Iron Guard')
                reflected_damage = 0.20 * p2_base_defense
                self.player1.initial_HP -= reflected_damage
                self.gamejudge.log_message(f"Player 2 - {p2_name} - used Iron Guard! Reflected {reflected_damage} points of damage!")
                self.gamejudge.player_down(self.player2, self.player1)
                print(self.player1.initial_HP)
                print(self.player2.initial_HP)
            else:
                print('Defesa normal.')
                
                print(self.player1.initial_HP)
                print(self.player2.initial_HP)
                pass

        # No caso de um clinch ganhar
        elif conflict_result['winning_class'] == 'clinch':
            # Se ambos usarem clinch
            if p1_current_action == 'clinch' and p2_current_action == 'clinch':
                self.gamejudge.set_draw_lock(self.player1)
                print(self.player1.draw_blocked)
                self.gamejudge.set_draw_lock(self.player2)
                print(self.player2.draw_blocked)
                self.gamejudge.log_message("Both players clinched! No drawing cards next turn")

            # Se somente o p1 usar clinch
            elif p1_current_action == 'clinch' and not p2_current_action == 'clinch':
                self.gamejudge.set_draw_lock(self.player2)
                print(self.player2.draw_blocked)

            # Somente o p2 usar clinch
            elif p2_current_action == 'clinch' and not p1_current_action == 'clinch':
                self.gamejudge.set_draw_lock(self.player1)
                print(self.player1.draw_blocked)
            
        # No caso de um ataque ganhar
        elif conflict_result['winning_class'] == 'attack':
            # Ataque contra ataque
            print('Ataque contra ataque')
            if p1_current_action == 'attack' and p2_current_action == 'clinch':
                print('P1 Ataca')
                # Dano base
                base_damage = self.damagecalculator.get_base_damage(self.player1, p2_weaknesses_multiplier, p2_resistances_multiplier)
                print(base_damage)
                if card_player1['name'] == 'Strong Attack':
                    base_damage = 2 * base_damage
                    self.gamejudge.log_message(f"Player 1 - {p1_name} - used Strong Attack! Damage doubled to {base_damage}")
                elif card_player1['name'] == 'Rubber Attack':
                    self.gamejudge.set_draw_lock(self.player2)
                    self.gamejudge.log_message(f"Player 1 - {p1_name} - used Rubber Arm! The attack connected and now Player 2 - {p2_name} is clinched!")
                elif card_player1['name'] == 'Fiery Punch':
                    self.gamejudge.drop_hand_slot(self.player2, 1)
                    self.gamejudge.log_message(f"Player 1 - {p1_name} - used Fiery Punch! Player 2 - {p2_name} lost 1 hand slot!")

                
                # Aumenta o score
                self.gamejudge.give_point(self.player1)
                print('P1 +1 Ponto')

                # Aplica o dano
                print(self.player2.initial_HP)
                self.player2.initial_HP -= base_damage
                print(self.player2.initial_HP)
                self.gamejudge.log_message(f"Player 1 - {p1_name} - Attack connected! {base_damage} points of damage applied!")
                self.gamejudge.player_down(self.player1, self.player2)

            elif p2_current_action == 'attack' and p1_current_action == 'clinch':
                print('P2 Ataca')
                # Dano base
                base_damage = self.damagecalculator.get_base_damage(self.player2, p1_weaknesses_multiplier, p1_resistances_multiplier)
                print(base_damage)
                if card_player2['name'] == 'Strong Attack':
                    base_damage = 2 * base_damage
                    self.gamejudge.log_message(f"Player 2 - {p2_name} - used Strong Attack! Damage doubled to {base_damage}")
                elif card_player2['name'] == 'Rubber Attack':
                    self.gamejudge.set_draw_lock(self.player2)
                    self.gamejudge.log_message(f"Player 2 - {p2_name} - used Rubber Arm! The attack connected and now Player 1 - {p1_name} is clinched!")
                elif card_player2['name'] == 'Fiery Punch':
                    self.gamejudge.drop_hand_slot(self.player2, 1)
                    self.gamejudge.log_message(f"Player 2 - {p2_name} - used Fiery Punch! Player 1 - {p1_name} lost 1 hand slot!")

                
                # Aumenta o score
                self.gamejudge.give_point(self.player2)
                print('P2 +1 Ponto')

                # Aplica o dano
                print(self.player1.initial_HP)
                self.player1.initial_HP -= base_damage
                print(self.player1.initial_HP)
                self.gamejudge.log_message(f"Player 2 - {p2_name} - Attack connected! {base_damage} points of damage applied!")
                self.gamejudge.player_down(self.player2, self.player1)

            # Dois ataques simultâneos
            elif p1_current_action == 'attack' and p2_current_action == 'attack':
                # Player 1 é mais ágil
                if self.player1.initial_agility > self.player2.initial_agility:

                    print(self.player1.initial_agility)
                    print(self.player2.initial_agility)

                    self._apply_attack(self.player1, self.player2, card_player1, p2_weaknesses_multiplier, p2_resistances_multiplier)

                    # Se o Player 2 estiver ainda apto a atacar
                    if not self.gamejudge.is_knocked_out(self.player2):
                        self._apply_attack(self.player2, self.player1, card_player2, p1_weaknesses_multiplier, p1_resistances_multiplier)

                # Player 2 é mais ágil                
                elif self.player2.initial_agility > self.player1.initial_agility:

                    print(self.player1.initial_agility)
                    print(self.player2.initial_agility)       

                    self._apply_attack(self.player2, self.player1, card_player2, p1_weaknesses_multiplier, p1_resistances_multiplier)
                    
                    # Se o Player 1 estiver ainda apto a atacar
                    if not self.gamejudge.is_knocked_out(self.player2):
                        self._apply_attack(self.player1, self.player2, card_player1, p2_weaknesses_multiplier, p2_resistances_multiplier)

                # Os dois player tem a mesma agilidade
                elif self.player1.initial_agility == self.player2.initial_agility:

                    print(self.player1.initial_agility)
                    print(self.player2.initial_agility)
                    # Define a iniciativa aleatoriamente

                    if random.choice([True, False]):
                        first_attacker = self.player1
                        second_attacker = self.player2
                        card_first = card_player1
                        card_second = card_player2
                        weaknesses_first = p1_weaknesses_multiplier
                        resistances_first = p1_resistances_multiplier
                        weaknesses_second = p2_weaknesses_multiplier
                        resistances_second = p2_resistances_multiplier
                        
                        # Log de desempate
                        self.gamejudge.log_message(f"Agility tie! But Player 1 {self.player1.name} was a little faster!")
                    else:
                        first_attacker = self.player2
                        second_attacker = self.player1
                        card_first = card_player2
                        card_second = card_player1
                        weaknesses_first = p2_weaknesses_multiplier
                        resistances_first = p2_resistances_multiplier
                        weaknesses_second = p1_weaknesses_multiplier
                        resistances_second = p1_resistances_multiplier
                        
                        # Log de desempate
                        self.gamejudge.log_message(f"Agility tie! But Player 2 {self.player2.name} was a little faster!")


                    # Primeiro Ataque
                    self._apply_attack(first_attacker, second_attacker, card_first, weaknesses_second, resistances_second)
                    
                    # Checa se o alvo do primeiro ataque ainda está apto para revidar
                    if not self.gamejudge.is_knocked_out(second_attacker):
                        # Segundo Ataque (Revide)
                        self._apply_attack(second_attacker, first_attacker, card_second, weaknesses_first, resistances_first)

    def _apply_attack(self, attacker, target, card_attacker, target_weaknesses_multiplier, target_resistances_multiplier):
        
        print(attacker.initial_HP)
        print(target.initial_HP)

        # Calcular Dano Base
        base_damage = self.damagecalculator.get_base_damage(attacker, target_weaknesses_multiplier, target_resistances_multiplier)

        print(base_damage)

        # Aplicar Efeitos da Carta do Atacante
        if card_attacker['name'] == 'Strong Attack':
            base_damage = 2 * base_damage
            self.gamejudge.log_message(f"Player {attacker.name} - used Strong Attack! Damage doubled to {base_damage}")
        
        elif card_attacker['name'] == 'Rubber Attack':
            self.gamejudge.set_draw_lock(target)
            self.gamejudge.log_message(f"Player {attacker.name} - used Rubber Arm! The attack connected and now Player {target.name} is clinched!")
        
        elif card_attacker['name'] == 'Fiery Punch':
            self.gamejudge.drop_hand_slot(target, 1)
            self.gamejudge.log_message(f"Player {attacker.name} - used Fiery Punch! Player {target.name} lost 1 hand slot!")
        
        # Aumenta o score
        self.gamejudge.give_point(attacker)

        # Aplica o dano no HP do alvo
        target.initial_HP -= base_damage
        self.gamejudge.log_message(f"Player {attacker.name} - Attack connected! {base_damage} points of damage applied!")
        
        print(attacker.initial_HP)
        print(target.initial_HP)
        
        # Checa se o alvo está nocauteado
        self.gamejudge.player_down(attacker, target)
        
        # Retorna o dano aplicado, caso seja necessário para a checagem do segundo ataque
        return base_damage                