from flask import Blueprint, request, jsonify
from models.battle_engine import start_battle, submit_turn, get_battle_state, BattleError

battle_bp = Blueprint('battle', __name__)


@battle_bp.route('/battles', methods=['POST'])
def create_battle():
    data = request.get_json() or {}
    robot_id = data.get('robot_id')
    num_rounds = data.get('num_rounds', 1)

    if not robot_id:
        return jsonify({'error': 'robot_id é obrigatório'}), 400

    try:
        return jsonify(start_battle(robot_id, num_rounds, player_id=1)), 201
    except BattleError as e:
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        print(f"Erro ao iniciar batalha: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500


@battle_bp.route('/battles/<battle_id>/turn', methods=['POST'])
def play_turn(battle_id):
    data = request.get_json() or {}
    card_id = data.get('card_id')

    if card_id is None:
        return jsonify({'error': 'card_id é obrigatório'}), 400

    try:
        return jsonify(submit_turn(battle_id, card_id)), 200
    except BattleError as e:
        return jsonify({'error': str(e)}), e.status_code
    except Exception as e:
        print(f"Erro ao resolver turno: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500


@battle_bp.route('/battles/<battle_id>', methods=['GET'])
def get_battle(battle_id):
    try:
        return jsonify(get_battle_state(battle_id)), 200
    except BattleError as e:
        return jsonify({'error': str(e)}), e.status_code
