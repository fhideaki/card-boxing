# Imports
from flask import request, jsonify, Blueprint, redirect, render_template, url_for, flash, send_file
from database import get_cards_from_db, get_details, get_type_names

# Construtor do flask/ Flask constructor
cards_bp = Blueprint('cards', __name__)

# Rota para receber todas as partes do banco de dados
@cards_bp.route('/cards', methods=['GET'])
def get_cards():
    # Criando uma lista vazia que vai armazenar as partes
    all_cards_list = []

    # Chamando a função que retorna um objeto com as entradas no banco de dados
    all_cards = get_cards_from_db()

    for card in all_cards:

        muito_efetiva = get_type_names('type_weaknesses', card['type'], 'type_id', 'weak_to_id')
        pouco_efetiva = get_type_names('type_resistances', card['type'], 'type_id', 'resists_id')

        pecas_str = card['requisitos_pecas'] if card['requisitos_pecas'] else ""

        card_dict = {
            'id': card["id"],
            'nome': card["name"],
            'class': card["class"],
            'tipo_id': card["type"],
            'tipo_nome': card["type_name"],
            'descricao': card["description"],
            'efeito_id': card["effect_id"],
            'efeito_nome': card["effect_name"],
            'requisitos_pecas': pecas_str.split(", ") if pecas_str else [],
            'muito_efetiva_contra': muito_efetiva,
            'pouco_efetiva_contra': pouco_efetiva
        }

        all_cards_list.append(card_dict)

    return jsonify(all_cards_list)
