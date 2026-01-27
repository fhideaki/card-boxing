# Imports
from flask import request, jsonify, Blueprint, redirect, render_template, url_for, flash, send_file
from database.operations import *
from models.static import *
import sqlite3
from models.robot import *
from models.deck import *
from routes.parts import parts_bp
from routes.cards import cards_bp
from routes.robots import robots_bp

# Construtor do flask/ Flask constructor
api = Blueprint('api', __name__)

api.register_blueprint(parts_bp)
api.register_blueprint(cards_bp)
api.register_blueprint(robots_bp)

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

# # Envio dos arquétipos e dos dados base
# @api.route("/archetypes", methods=["GET"])
# def get_archetypes():
#     return jsonify(robot_archetypes)

# # Rota para verificar cada arquétipo
# @api.route("/archetypes/<string:archetype_key>/preview")
# def archetype_preview(archetype_key):
#     archetype = robot_archetypes.get(archetype_key)

#     if not archetype:
#         return jsonify({"error": "Arquétipo não encontrado"}), 404

#     base = archetype["base_stats"]
#     secondary = calculate_secondary_stats(base)

#     deck = build_deck(archetype["deck"], card_list)

#     return jsonify({
#         "key": archetype_key,
#         "label": archetype["label"],
#         "image": archetype["image"],
#         "base_stats": base,
#         "secondary_stats": secondary,
#         "deck":deck
#     })

# # Rota para criar um "preview" de todos os robôs para o frontend acessar e pegar os atributos.
# @api.route("/archetypes/all/preview")
# def all_archetypes_preview():
#     all_previews = []

#     # Iteramos sobre o dicionário robot_archetypes
#     for archetype_key, data in robot_archetypes.items():
#         base = data["base_stats"]
        
#         # Reutiliza suas funções existentes
#         secondary = calculate_secondary_stats(base)
#         deck = build_deck(data["deck"], card_list)

#         # Monta o objeto formatado para cada um
#         preview = {
#             "key": archetype_key,
#             "label": data["label"],
#             "image": data["image"],
#             "base_stats": base,
#             "secondary_stats": secondary,
#             "deck": deck
#         }
#         all_previews.append(preview)

#     # Retorna a lista completa de objetos
#     return jsonify(all_previews)