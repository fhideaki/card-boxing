import random
import uuid

from config import DECK_SIZE
from database import get_full_robots_data, get_robot_deck_from_db, get_cards_from_db

from .player import Player
from .turn import Turn
from .game_judge import GameJudge
from .damage_calculator import DamageCalculator
from .null_ui import NullUIManager
from .i18n import CARD_NAME_PT, CARD_DESCRIPTION_PT

# Partidas em andamento, guardadas em memória (sem persistência em disco - ver plano/riscos aceitos)
BATTLES = {}

AI_ARCHETYPES = ['atk', 'def', 'bal']
TURNS_PER_ROUND = 3


class BattleError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


def build_card_lookup():
    rows = get_cards_from_db()
    lookup = {}
    for row in rows:
        lookup[row['id']] = {
            'id': row['id'],
            'name': row['name'],
            'class': row['class'],
            'type': (row['type_name'] or '').lower(),
            'description': row['description'],
            'effect': None,
        }
    return lookup


def strip_card(card):
    if card is None:
        return None
    nome_en = card.get('name')
    return {
        'id': card.get('id'),
        'name': CARD_NAME_PT.get(nome_en, nome_en),
        'class': card.get('class'),
        'type': card.get('type'),
        'description': CARD_DESCRIPTION_PT.get(nome_en, card.get('description')),
    }


def start_battle(robot_id, num_rounds, player_id=1):
    try:
        num_rounds = int(num_rounds)
    except (TypeError, ValueError):
        num_rounds = 1
    num_rounds = max(1, num_rounds)

    robots = get_full_robots_data(player_id)
    robot = next((r for r in robots if r['id'] == robot_id), None)
    if robot is None:
        raise BattleError("Robô não encontrado para este jogador.", 404)

    deck_rows = get_robot_deck_from_db(robot_id)
    total = sum(row['quantity'] for row in deck_rows)
    if total != DECK_SIZE:
        raise BattleError(f"O deck do robô precisa ter {DECK_SIZE} cartas (atual: {total}).", 400)

    card_lookup = build_card_lookup()
    deck_list = []
    for row in deck_rows:
        card = card_lookup.get(row['id'])
        if card is None:
            continue
        for _ in range(row['quantity']):
            deck_list.append(dict(card))

    ui = NullUIManager()
    damagecalculator = DamageCalculator(ui)
    gamejudge = GameJudge(ui, damagecalculator)

    player1 = Player(
        name="Jogador",
        robot_name=robot['name'],
        archetype=robot['archetype'],
        ui_manager=ui,
        base_stats={
            'constitution': robot['stats']['constitution'],
            'strength': robot['stats']['strength'],
            'agility': robot['stats']['agility'],
            'hp': robot['stats']['hp'],
        },
        resistances=[r.lower() for r in robot['resistencias']],
        weaknesses=[w.lower() for w in robot['fraquezas']],
        explicit_deck=deck_list,
    )
    player1.setDeck()

    ai_archetype = random.choice(AI_ARCHETYPES)
    player2 = Player(
        name="IA",
        robot_name=f"Robô IA ({ai_archetype.upper()})",
        archetype=ai_archetype,
        ui_manager=ui,
    )
    player2.setDeck()

    turn = Turn(player1, player2, gamejudge, damagecalculator)
    turn.game_start()
    turn.execute_first_phase()
    if not gamejudge.game_over:
        turn.execute_draw_phase()

    battle_id = uuid.uuid4().hex
    BATTLES[battle_id] = {
        'robot_id': robot_id,
        'player1': player1,
        'player2': player2,
        'turn': turn,
        'gamejudge': gamejudge,
        'ui': ui,
        'num_rounds': num_rounds,
        'turns_per_round': TURNS_PER_ROUND,
    }

    return serialize_state(battle_id, BATTLES[battle_id])


def submit_turn(battle_id, card_id):
    battle = BATTLES.get(battle_id)
    if battle is None:
        raise BattleError("Batalha não encontrada.", 404)

    gamejudge = battle['gamejudge']
    if gamejudge.game_over:
        raise BattleError("Esta batalha já terminou.", 409)

    player1 = battle['player1']
    player2 = battle['player2']
    turn = battle['turn']
    ui = battle['ui']

    if not any(card['id'] == card_id for card in player1.hand):
        raise BattleError("Essa carta não está na sua mão.", 400)

    if not player2.hand:
        raise BattleError("A IA não tem cartas para jogar.", 409)

    # IA escolhe uma carta válida aleatória da própria mão
    ai_card = random.choice(player2.hand)

    log_start = len(ui.messages)
    gamejudge.increase_turn()

    turn.execute_play_phase(card_id, ai_card['id'])

    # Guardar as cartas jogadas antes que o próximo execute_first_phase limpe o registro do turno
    player_card_played = dict(gamejudge.current_turn_actions[player1])
    opponent_card_played = dict(gamejudge.current_turn_actions[player2])

    third_result = turn.execute_third_phase()
    conflict_result = third_result['conflict_result'] or {}
    damage_dealt = third_result['damage_dealt']

    # Limite de turnos vindo da quantidade de "rounds" escolhida na Home - decide por score se ninguém nocauteou até lá
    if not gamejudge.game_over:
        turn_limit = battle['num_rounds'] * battle['turns_per_round']
        if gamejudge.turn >= turn_limit:
            p1_score = gamejudge.score[player1]
            p2_score = gamejudge.score[player2]
            if p1_score == p2_score:
                gamejudge.log_message(f"Limite de turnos atingido ({turn_limit} turnos). Placar empatado em {p1_score}-{p2_score}.")
                gamejudge.game_over = True
                gamejudge.win_reason = "Decisão por pontos."
            else:
                winner = player1 if p1_score > p2_score else player2
                gamejudge.declare_winner(winner, "Decisão por pontos.")

    resolved_turn = {
        'player_card': strip_card(player_card_played),
        'opponent_card': strip_card(opponent_card_played),
        'conflict_winner': {'p1': 'player', 'p2': 'ai', 'tie': 'draw'}.get(conflict_result.get('winner')),
        'damage_to_player': round(damage_dealt.get(player1, 0), 2),
        'damage_to_opponent': round(damage_dealt.get(player2, 0), 2),
        'log': list(ui.messages[log_start:]),
    }

    # Prepara o próximo turno, se a partida continuar
    if not gamejudge.game_over:
        turn.execute_first_phase()

    if not gamejudge.game_over:
        turn.execute_draw_phase()

    return serialize_state(battle_id, battle, resolved_turn=resolved_turn)


def get_battle_state(battle_id):
    battle = BATTLES.get(battle_id)
    if battle is None:
        raise BattleError("Batalha não encontrada.", 404)
    return serialize_state(battle_id, battle)


def serialize_state(battle_id, battle, resolved_turn=None):
    player1 = battle['player1']
    player2 = battle['player2']
    gamejudge = battle['gamejudge']
    ui = battle['ui']
    turns_per_round = battle['turns_per_round']
    num_rounds = battle['num_rounds']

    turns_played = gamejudge.turn
    next_turn = turns_played + 1
    display_round = min(((next_turn - 1) // turns_per_round) + 1, num_rounds)
    display_turn_in_round = ((next_turn - 1) % turns_per_round) + 1

    winner = None
    if gamejudge.game_over:
        if gamejudge.winner is None:
            winner = 'draw'
        elif gamejudge.winner is player1:
            winner = 'player'
        else:
            winner = 'ai'

    state = {
        'battle_id': battle_id,
        'status': 'finished' if gamejudge.game_over else 'in_progress',
        'round': display_round,
        'turn': display_turn_in_round,
        'num_rounds': num_rounds,
        'turns_per_round': turns_per_round,
        'player': {
            'robot_id': battle['robot_id'],
            'name': player1.robot.robot_name,
            'hp': round(max(player1.initial_HP, 0), 2),
            'max_hp': player1.robot.HP,
            'hand': [strip_card(c) for c in player1.hand],
            'deck_remaining': len(player1.game_deck),
            'graveyard_count': len(player1.graveyard),
        },
        'opponent': {
            'name': player2.robot.robot_name,
            'archetype': player2.robot.archetype,
            'hp': round(max(player2.initial_HP, 0), 2),
            'max_hp': player2.robot.HP,
            'hand_count': len(player2.hand),
            'deck_remaining': len(player2.game_deck),
            'graveyard_count': len(player2.graveyard),
        },
        'winner': winner,
        'win_reason': gamejudge.win_reason,
        'log': list(ui.messages),
    }

    if resolved_turn is not None:
        state['resolved_turn'] = resolved_turn

    return state
