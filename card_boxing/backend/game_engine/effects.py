# Esta vai ser a classe-mãe das outras classes de efeito
class Effect:
    def __init__(self, param):
        self.param = param

    # Método para ser aplicado antes da defesa ser contada em cálculo. Ele modifica o dano base com multiplicadores (*2, *3, etc)
    def apply_pre_damage_modifier(self, base_damage):
        return base_damage

    # Método para gerenciar os efeitos posteriores ao dano. Descartar cartas, perder slots, novos efeitos em geral.
    def apply_post_damage_effect(self, final_damage, attacker, target, judge, calculator):
        pass

    # Método para debug
    def __repr__(self):
        return f"{self.__class__.__name__}({self.param})"
        
class DoubleDamageEffect(Effect):
    def __init__(self):
        self.multiplier = 2

    # Dobra o dano base
    def apply_pre_damage_modifier(self, base_damage, attacker, target, judge):
        # Checando se uma carta do tipo clinch foi utilizada
        if judge.has_used_clinch(target):
            doubled_damage = base_damage * self.multiplier
            judge.log_message(f"{attacker.name} attack caused Double Damage on {target.name} 'clinch'. {base_damage} double to {doubled_damage}")
            return doubled_damage
        else:
            judge.log_message(f"Double Damage condition failed. Target {target.name} did not use clinch.")
            return base_damage
        
class ClinchEffect(Effect):

    def apply_post_damage_effect(self, final_damage, attacker, target, judge, calculator):
        judge.log_message(f"{attacker.name} clinched {target.name}! Draw block for next turn activated.")

        # Juiz bloqueia a compra
        judge.set_draw_lock(target, self.param)

class InvincibleEffect(Effect):

    def apply_post_damage_effect(self, final_damage, attacker, target, judge, calculator):
        judge.log_message(f"{attacker.name} cannot be damaged or clinched.")

        judge.set_invulnerability(attacker)

class StopHittingYourselfEffect(Effect):
    def __init__(self):
        self.returned_damage = 0.20

    def apply_post_damage_effect(self, final_damage, attacker, target, judge, calculator):
        attacker_card = judge.current_turn_actions.get(attacker)
        is_attacker_attack = attacker_card and attacker_card.get("class") == "attack"

        if judge.check_card_class(target, "guard") and final_damage > 0 and is_attacker_attack:

            damage_reflected = int(final_damage * self.param)
            judge.log_message(f"{target.name} successfully defended and reflected {self.returned_damage*100}% damage!")
            judge.apply_damage(attacker, damage_reflected)

        elif not is_attacker_attack:
            judge.log_message(f"Effect failed. {attacker.name} card was not in the 'attack' class.")

class WhiteHotFirePunchEffect(Effect):
    def __init__(self):
        self.lost_slots = 1

    def apply_post_damage_effect(self, final_damage, attacker, target, judge, calculator):
        judge.log_message(f"{attacker.name}'s attack burned {target.name}'s hand and now it lost {self.lost_slots} slot.")

        judge.drop_hand_slot(target, self.lost_slots)

class OmniclinchEffect(Effect):
    def __init__(self):
        self.draw_lock = 1

    def apply_post_damage_effect(self, final_damage, attacker, target, judge, calculator):
        if target.is_invincible:
            judge.log_message(f"{target.name} in Invincible state, clinch blocked!")
            return

        judge.log_message(f"{attacker.name} activated Omniclinch. Draw block activated.")
        judge.set_draw_lock(target, self.draw_lock)