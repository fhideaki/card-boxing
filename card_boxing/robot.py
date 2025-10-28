# Card Boxing Game

# Dois robôs boxeadores se enfrentam no ringue. Cada robô realiza uma ação que é declarada por meio de cartas.
# O jogo dura 3 rounds.
# Cada round acontece em 3 turnos.
# Cada turno é composto por uma ação de cada jogador e por suas consequências.

# Criando primeiro a classe robô.
class Robot:
    # Aqui o jogador define se ele quer um arquétipo de robô focado em ataque, defesa ou balanceado. Isso define os atributos base do jogador.
    def __init__(self, archetype):
        if archetype == "ATK":
            self.constitution = 6
            self.strength = 10
            self.agility = 8
            self.HP = 6
        elif archetype == "DEF":
            self.constitution = 10
            self.strength = 6
            self.agility = 6
            self.HP = 8
        elif archetype == "BAL":
            self.constitution = 7
            self.strength = 7
            self.agility = 7
            self.HP = 7
        self.defense = self.constitution + (0.6 * self.strength)
        self.attack = self.strength + (0.6 * self.agility)
        self.clinch = self.agility + (0.6 * self.strength)

        self.part_list = []

        self.resistances = []
        self.weaknesses = []
    
    # Daqui pra baixo o jogador define as peças do robô que ele quer jogar, quando ele define a peça, o método atualiza os atributos.
    def setHead(self, head_part):

        if head_part["slot"] == "HEAD":

            self.constitution += head_part["modifiers"]["constitution"]
            self.strength += head_part["modifiers"]["strength"]
            self.agility += head_part["modifiers"]["agility"]
            self.HP += head_part["modifiers"]["HP"]
            self.part_list.append(head_part)

            for i in head_part["resistances"]:
                self.resistances.append(i)
            for i in head_part["weaknesses"]:
                self.weaknesses.append(i)

    def setBody(self, body_part):

        if body_part["slot"] == "BODY":

            self.constitution += body_part["modifiers"]["constitution"]
            self.strength += body_part["modifiers"]["strength"]
            self.agility += body_part["modifiers"]["agility"]
            self.HP += body_part["modifiers"]["HP"]
            self.part_list.append(body_part)

            for i in body_part["resistances"]:
                self.resistances.append(i)
            for i in body_part["weaknesses"]:
                self.weaknesses.append(i)

    def setLArm(self, larm_part):

        if larm_part["slot"] == "ARM":

            self.constitution += larm_part["modifiers"]["constitution"]
            self.strength += larm_part["modifiers"]["strength"]
            self.agility += larm_part["modifiers"]["agility"]
            self.HP += larm_part["modifiers"]["HP"]
            self.part_list.append(larm_part)

            for i in larm_part["resistances"]:
                self.resistances.append(i)
            for i in larm_part["weaknesses"]:
                self.weaknesses.append(i)

    def setRArm(self, rarm_part):

        if rarm_part["slot"] == "ARM":

            self.constitution += rarm_part["modifiers"]["constitution"]
            self.strength += rarm_part["modifiers"]["strength"]
            self.agility += rarm_part["modifiers"]["agility"]
            self.HP += rarm_part["modifiers"]["HP"]
            self.part_list.append(rarm_part)

            for i in rarm_part["resistances"]:
                self.resistances.append(i)
            for i in rarm_part["weaknesses"]:
                self.weaknesses.append(i)

    def setLLeg(self, lleg_part):

        if lleg_part["slot"] == "LEG":

            self.constitution += lleg_part["modifiers"]["constitution"]
            self.strength += lleg_part["modifiers"]["strength"]
            self.agility += lleg_part["modifiers"]["agility"]
            self.HP += lleg_part["modifiers"]["HP"]
            self.part_list.append(lleg_part)

            for i in lleg_part["resistances"]:
                self.resistances.append(i)
            for i in lleg_part["weaknesses"]:
                self.weaknesses.append(i)

    def letRLeg(self, rleg_part):

        if rleg_part["slot"] == "LEG":

            self.constitution += rleg_part["modifiers"]["constitution"]
            self.strength += rleg_part["modifiers"]["strength"]
            self.agility += rleg_part["modifiers"]["agility"]
            self.HP += rleg_part["modifiers"]["HP"]
            self.part_list.append(rleg_part)

            for i in rleg_part["resistances"]:
                self.resistances.append(i)
            for i in rleg_part["weaknesses"]:
                self.weaknesses.append(i)