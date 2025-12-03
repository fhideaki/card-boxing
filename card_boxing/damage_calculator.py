from ui_manager import UIManager
from static import *
# Classe que vai ser a "calculadora" do juiz. Ela vai calcular, aplicar e retornar os modificadores e o dano.
class DamageCalculator:
    def __init__(self, ui_manager: UIManager):
        self.ui = ui_manager
        self.ui.printMessage('Calculator created.')
    
    # Método para checar as fraquezas
    @staticmethod
    def check_weaknesses(card, defender):
        # Pega o tipo da carta atacante
        atk_type = card["type"]
        # Pega a lista de fraquezas do robô defensor
        def_weaknesses = defender.robot.weaknesses
        weaknesses_multiplier = 0
        for weakness in def_weaknesses:
            if weakness in weaknesses_matrix[atk_type]:
                weaknesses_multiplier += 0.5
        # Retorna o multiplicador de dano
        return weaknesses_multiplier
    
    # Método para checar as resistências
    @staticmethod
    def check_resistances(card, defender):
        # Pega o tipo da carta atacante
        atk_type = card["type"]
        # Pega a lista de resistências do robô defensor
        def_resistances = defender.robot.resistances
        resistances_multiplier = 0
        for resistance in def_resistances:
            if resistance in resistances_matrix[atk_type]:
                resistances_multiplier += 1
        # Retorna o multiplicador de dano
        return resistances_multiplier
    
    # O dano base é o dano a ser aplicado depois de considerar o ataque, fraquezas e resistências
    @staticmethod
    def get_base_damage(attacker, weaknesses_multiplier, resistances_multiplier):
        base_atk = attacker.initial_attack
        base_damage = base_atk * (1 + weaknesses_multiplier) * (0.5)**resistances_multiplier
        return base_damage

    # A defesa base leva em conta o atributo de defesa do robô. E quanto maior a defesa, menos eficientes os pontos de defesa adicionais se tornam.
    @staticmethod
    def get_base_defense(defender):
        base_def = defender.initial_defense
        base_defense = 100 / (100 + base_def)
        return base_defense

    # O dano final já leva em conta a defesa e retorna o número final que vai ser deduzido dos pontos de vida do defensor.
    @staticmethod
    def apply_mitigation(base_damage, base_defense):
        final_damage = base_damage * base_defense
        return final_damage