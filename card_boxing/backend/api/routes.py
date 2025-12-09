# Imports
from flask import request, jsonify, Blueprint, redirect, render_template, url_for, flash, send_file
from database.operations import *

# Construtor do flask/ Flask constructor
api = Blueprint('api', __name__)

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

# # Registro de Jogador
# @api.route('/', methods=['POST'])
# def register(username, password):
#     create_user(username, password)

# # Login
# @api.route('/', methods=['POST'])
# def login(username, password):
#     check_password(username, password)