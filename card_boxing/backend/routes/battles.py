# Imports
from flask import Blueprint, request, jsonify
from database.operations import start_new_battle

# Construtor do flask/ Flask constructor
battle_bp = Blueprint('battle', __name__)
