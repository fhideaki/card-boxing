from damage_calculator import *
from deck import *
from effects import *
from game_judge import *
from player import *
from robot import *
from static import *
from ui_manager import *
from turn import *

# Criando a UI
ui = UIManager()

# Criando um jogador
ferpas = Player('Ferna', 'Terminator', 'atk', ui)

# Equipando itens no robo
iron_head = parts_list[0]
blazing_arm = parts_list[1]
rubber_arm = parts_list[2]
iron_body = parts_list[3]
rubber_body = parts_list[4]
iron_leg = parts_list[5]
rubber_leg = parts_list[6]

ferpas.robot.setSlot('head', iron_head)
ferpas.robot.setSlot('right_arm', blazing_arm)
ferpas.robot.setSlot('body', iron_body)
ferpas.robot.setSlot('left_arm', rubber_arm)

paulo = Player('Colan', 'Mach35', 'bal', ui)
paulo.robot.setSlot('head', iron_head)
paulo.robot.setSlot('body', iron_body)
paulo.robot.setSlot('left_arm', rubber_arm)

# Robos equipados, criando o juiz e a calculadora
calculadora = DamageCalculator(ui)
juiz = GameJudge(ui, calculadora)

# Preparando os jogadores com as cartas especiais
ferpas.setDeck()
paulo.setDeck()

turno = Turn(ferpas, paulo, juiz, calculadora)

turno.game_start()

for i in range(3):
    turno.execute_first_phase()
    turno.execute_second_phase()
    turno.execute_third_phase()
    print(f'Cartas descartadas  P1 - {len(ferpas.graveyard)}')
    print(f'Cartas descartadas  P2 - {len(paulo.graveyard)}')

