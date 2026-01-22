# Imports
from flask import request, jsonify, Blueprint, redirect, render_template, url_for, flash, send_file
from database import get_parts_from_db, get_details, get_type_names

# Construtor do flask/ Flask constructor
parts_bp = Blueprint('parts', __name__)

# Rota para receber todas as partes do banco de dados
@parts_bp.route('/parts', methods=['GET'])
def get_parts():
    # Criando uma lista vazia que vai armazenar as partes
    all_parts_list = []

    # Chamando a função que retorna um objeto com as entradas no banco de dados
    all_parts = get_parts_from_db()

    for part in all_parts:

        fraquezas = get_type_names('type_weaknesses', part['type'], 'type_id', 'weak_to_id')
        resistencias = get_type_names('type_resistances', part['type'], 'type_id', 'resists_id')

        part_dict = {
            'id': part["id"],
            'nome': part["part_name"],
            'descricao': part["description"],
            'slot_id': part['slot_id'],
            'slot': part['slot_name'],
            'tipo_id': part['type'],
            'tipo_nome': part['type_name'],
            'card_id': part['card_id'],
            'liberaCartas': [{"carta": part['card_name']}] if part['card_name'] else [],
            'fraquezas': fraquezas,
            'resistencias': resistencias,
            'conmod': part['stat_constitution_mod'],
            'strmod': part['stat_strength_mod'],
            'agimod': part['stat_agility_mod'],
            'hpmod': part['stat_hp_mod'],
            'imagem': part['image_url']
        }

        all_parts_list.append(part_dict)

    return jsonify(all_parts_list)
