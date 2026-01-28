# Imports
from flask import request, jsonify, Blueprint
from database import get_parts_from_db, get_details, get_type_names, get_robot_with_stats, get_cards_from_db, create_robot_in_db, get_archetypes_from_db, get_full_robots_data
import sqlite3

# Construtor do flask/ Flask constructor
robots_bp = Blueprint('robots', __name__)

# Rota para receber todas as partes do banco de dados
@robots_bp.route('/robots', methods=['GET'])
def get_robots():
    
    # Pega o ID do usuário que vem na URL
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID é obrigatório'}), 400
    
    try:
        robots_data = get_full_robots_data(user_id)

        return jsonify({'robots': robots_data})
    
    except Exception as e:
        print(f"Erro ao buscar robôs: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500

@robots_bp.route('/archetypes', methods=['GET'])
def get_archetypes():

    archetypes_rows = get_archetypes_from_db()

    archetypes_list = [dict(row) for row in archetypes_rows]

    return jsonify(archetypes_list)

@robots_bp.route('/robots', methods=['POST'])
def create_robot():
    data = request.get_json()

    robot_name = data.get('robot_name')
    archetype_id = data.get('archetype_id')
    player_id = 1

    if not robot_name or not archetype_id:
        return jsonify({"message": "Dados incompletos"}), 400
    
    try:
        new_id = create_robot_in_db(robot_name, archetype_id,  player_id)

        return jsonify({
            'message': 'Robô criado com sucesso!',
            'id': new_id
        }), 201

    except Exception as e:
        print(f"Erro ao criar robô: {e}")
        return jsonify({'error': str(e)}), 500
