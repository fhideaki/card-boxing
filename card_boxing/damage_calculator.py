from ui_manager import UIManager
from static import *
# Classe que vai ser a "calculadora" do juiz. Ela vai calcular, aplicar e retornar os modificadores e o dano.
class DamageCalculator:
    def __init__(self, ui_manager: UIManager):
        self.ui = ui_manager
    
    @staticmethod
    def check_weaknesses(card, defender_robot):
        # Pega o tipo da carta atacante
        atk_type = card["type"]
        # Pega a lista de fraquezas do robô defensor
        def_weaknesses = defender_robot.weaknesses
        weaknesses_multiplier = 0
        for weakness in def_weaknesses:
            if weakness in weaknesses_matrix[atk_type]:
                weaknesses_multiplier += 0.5
        # Retorna o multiplicador de dano
        return weaknesses_multiplier
    
    @staticmethod
    def check_resistances(card, defender_robot):
        # Pega o tipo da carta atacante
        atk_type = card["type"]
        # Pega a lista de fraquezas do robô defensor
        def_resistances = defender_robot.resistances
        resistances_multiplier = 0
        for resistance in def_resistances:
            if resistance in resistances_matrix[atk_type]:
                resistances_multiplier += 0.5
        # Retorna o multiplicador de dano
        return resistances_multiplier
    
    @staticmethod
    def get_base_damage(attacker_robot, weaknesses_multiplier, resistances_multiplier):
        base_atk = attacker_robot.attack
        base_damage = base_atk * (weaknesses_multiplier - resistances_multiplier)
        return base_damage

    @staticmethod
    def get_base_defense(defender_robot):
        base_def = defender_robot.defense
        base_defense = 100 / (100 + base_def)
        return base_defense

    @staticmethod
    def apply_mitigation(base_damage, base_defense):
        final_damage = base_damage * base_defense
        return final_damage