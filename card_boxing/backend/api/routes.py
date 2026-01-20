# Imports
from flask import request, jsonify, Blueprint, redirect, render_template, url_for, flash, send_file
from database.operations import *
from models.static import *
import sqlite3
from models.robot import *
from models.deck import *
from routes.parts import parts_bp

# Construtor do flask/ Flask constructor
api = Blueprint('api', __name__)

api.register_blueprint(parts_bp)

# Rota de Registro de Jogador
@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Dados incompletos."}), 400

    username = data['username']
    password = data['password']
    
    # **IMPORTANTE:** Sua função create_user precisa retornar (True/False, Mensagem)
    success, message = create_user(username, password) 
    
    if success:
        return jsonify({"message": "Usuário registrado com sucesso. Pode logar."}), 201
    else:
        # Ex: Usuário já existe, falha no DB, etc.
        return jsonify({"message": message}), 409 

# Rota de Login
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Dados incompletos."}), 400

    username = data['username']
    password = data['password']
    
    # **IMPORTANTE:** Sua função check_password precisa retornar True ou False
    is_valid = check_password(username, password)

    if is_valid:
        # Em um jogo real, você criaria uma sessão ou token aqui
        return jsonify({"message": f"Acesso concedido. Bem-vindo, {username}!"}), 200
    else:
        return jsonify({"message": "Credenciais inválidas. Tente novamente."}), 401

# Rota para buscar os robôs do jogador
@api.route("/robots", methods=["GET"])
def get_user_robots():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    conn = sqlite3.connect('card_game.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Buscar todos os robôs do jogador
    cursor.execute("""
        SELECT r.id, r.robot_name, r.archetype_id, a.archetype_name,
               a.base_constitution, a.base_strength, a.base_agility, a.base_hp
        FROM robots r
        JOIN robot_archetypes a ON r.archetype_id = a.id
        WHERE r.player_id = ?
    """, (user_id,))

    robots = cursor.fetchall()

    robots_list = []

    for robot in robots:
        robot_id = robot["id"]

        # Buscar partes equipadas para esse robô
        cursor.execute("""
            SELECT p.part_name, p.description, p.type, p.stat_constitution_mod,
                   p.stat_strength_mod, p.stat_agility_mod, p.stat_hp_mod,
                   s.slot_name
            FROM robot_equipped_parts rep
            JOIN robot_parts p ON rep.part_id = p.id
            JOIN robot_slots s ON rep.slot_id = s.id
            WHERE rep.robot_id = ?
        """, (robot_id,))
        
        parts = cursor.fetchall()

        robot_dict = {
            "id": robot["id"],
            "name": robot["robot_name"],
            "archetype": robot["archetype_name"],
            "stats": {
                "constitution": robot["base_constitution"],
                "strength": robot["base_strength"],
                "agility": robot["base_agility"],
                "hp": robot["base_hp"]
            },
            "parts": [
                {
                    "slot": p["slot_name"],
                    "name": p["part_name"],
                    "icon": "default.png",
                    "type": p["type"],
                    "mods": {
                        "constitution": p["stat_constitution_mod"],
                        "strength": p["stat_strength_mod"],
                        "agility": p["stat_agility_mod"],
                        "hp": p["stat_hp_mod"]
                    }
                }
                for p in parts
            ]
        }

        robots_list.append(robot_dict)

    conn.close()
    return jsonify({"robots": robots_list})

# Envio dos arquétipos e dos dados base
@api.route("/archetypes", methods=["GET"])
def get_archetypes():
    return jsonify(robot_archetypes)

# Rota para verificar cada arquétipo
@api.route("/archetypes/<string:archetype_key>/preview")
def archetype_preview(archetype_key):
    archetype = robot_archetypes.get(archetype_key)

    if not archetype:
        return jsonify({"error": "Arquétipo não encontrado"}), 404

    base = archetype["base_stats"]
    secondary = calculate_secondary_stats(base)

    deck = build_deck(archetype["deck"], card_list)

    return jsonify({
        "key": archetype_key,
        "label": archetype["label"],
        "image": archetype["image"],
        "base_stats": base,
        "secondary_stats": secondary,
        "deck":deck
    })

# Rota para criar um "preview" de todos os robôs para o frontend acessar e pegar os atributos.
@api.route("/archetypes/all/preview")
def all_archetypes_preview():
    all_previews = []

    # Iteramos sobre o dicionário robot_archetypes
    for archetype_key, data in robot_archetypes.items():
        base = data["base_stats"]
        
        # Reutiliza suas funções existentes
        secondary = calculate_secondary_stats(base)
        deck = build_deck(data["deck"], card_list)

        # Monta o objeto formatado para cada um
        preview = {
            "key": archetype_key,
            "label": data["label"],
            "image": data["image"],
            "base_stats": base,
            "secondary_stats": secondary,
            "deck": deck
        }
        all_previews.append(preview)

    # Retorna a lista completa de objetos
    return jsonify(all_previews)

# Rota para criar o robô
@api.route('/robots/create', methods=["POST"])
def create_robot():
    data = request.get_json()
    
    robot_name = data.get('robot_name')
    player_id = data.get('player_id')
    archetype_key = data.get('archetype_key')

    if not all([robot_name, player_id, archetype_key]):
        return jsonify({"message": "Dados incompletos"}), 400
    
    insert_robot_in_db(robot_name, player_id, archetype_key)
    
    return jsonify({"message": "Robô criado com sucesso!"}), 201
