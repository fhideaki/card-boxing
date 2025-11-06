# Card Boxing Game

# Imports
# Imports rich são para melhorar a qualidade do display dos dados para o usuário
from rich.console import Console
from rich.table import Table
from static import parts_list
from ui_manager import UIManager

# Dois robôs boxeadores se enfrentam no ringue. Cada robô realiza uma ação que é declarada por meio de cartas.
# O jogo dura 3 rounds.
# Cada round acontece em 3 turnos.
# Cada turno é composto por uma ação de cada jogador e por suas consequências.

# Criando primeiro a classe robô.
class Robot:
    # Aqui o jogador define se ele quer um arquétipo de robô focado em ataque, defesa ou balanceado. Isso define os atributos base do robô.
    def __init__(self, archetype, ui_manager, robot_name=None):
        
        self.archetype = archetype
        
        if archetype == "atk":
            self.constitution = 6
            self.strength = 10
            self.agility = 8
            self.HP = 6
            
        elif archetype == "def":
            self.constitution = 10
            self.strength = 6
            self.agility = 6
            self.HP = 8
            
        elif archetype == "bal":
            self.constitution = 7
            self.strength = 7
            self.agility = 7
            self.HP = 7
            
        self.robot_name = robot_name
            
        self.defense = self.constitution + (0.6 * self.strength)
        self.attack = self.strength + (0.6 * self.agility)
        self.clinch = self.agility + (0.6 * self.strength)

        self.resistances = []
        self.weaknesses = []
        
        # Dicionário com os slots do robô e suas partes
        self.slots = {
            "head": None,
            "body": None,
            "right_arm": None,
            "left_arm": None,
            "right_leg": None,
            "left_leg": None
        }

        self.ui = ui_manager
        
    # Método para mostrar os atributos e status do robô.
    def showStats(self):
        stats_table = self.ui.createStatsTable(f"Robot {self.robot_name}'s Stats")
        
        # Escrevendo a tabela
        stats_list = [
            str(self.constitution),
            str(self.strength),
            str(self.agility),
            str(self.HP),
            str(self.defense),
            str(self.attack),
            str(self.clinch),
            ", ".join(self.resistances) if self.resistances else "N/A",
            ", ".join(self.weaknesses) if self.weaknesses else "N/A"
            ]
        
        self.ui.addStatsRow(stats_table, stats_list)

    # Método para receber a peça de um slot.
    def getPartFromSlot(self, slot):
        return self.slots.get(slot, None)
        
    # Método para checar se o slot está vago.
    def checkSlotIfEmpty(self, slot):
        
        found_part = self.slots.get(slot)

        # Se não encontrar uma parte, retorna False
        if found_part is None:
            self.ui.printMessage(f"Slot '{slot}' is Empty.")
            return False
        # Se encontrar uma parte, retorna a parte.
        else:
            self.showParts(found_part["id"])
            return found_part
        
    # Método para exibir os slots e retornar a peça 
    def showSlots(self):
        
        robot_slots = self.ui.createSlotsTable(title=f"Robot {self.robot_name} Slots")
        
        # Iterando sobre as partes (head, body, etc)
        for slot_name in self.slots:
            # Retornando o dicionário da peça procurada, ou None caso não tenha peça
            part_data = self.getPartFromSlot(slot_name)
            
            if part_data:
                part_id = str(part_data["id"])
                part_name = part_data["part_name"]
                part_type = part_data["type"]
            
            else:
                part_id = "N/A"
                part_name = "N/A"
                part_type = "N/A"
                
            # Cria a lista com as informações
            robot_slots_list = [
                slot_name,
                part_id,
                part_name,
                part_type
            ]
            # Adiciona a lista na tabela
            self.ui.addSlotsRow(robot_slots, robot_slots_list)
        
        # Printa a tabela
        self.ui.console.print(robot_slots)
    
    # Colocando uma peça em um slot.
    def setSlot(self, slot, part):
        # A parte é referente ao slot correto?
        if part["slot"] == slot:
            # Checando se o slot está vazio
            if self.checkSlotIfEmpty(slot) is False:
                
                self.ui.printMessage(f"Slot {slot} empty and available. Printing current robot stats.")
                
                self.showStats()
                
                # Adicionando os modificadores nos atributos base do robô
                self.slots[part["slot"]] = part
                self.constitution += part["modifiers"]["constitution"]
                self.strength += part["modifiers"]["strength"]
                self.agility += part["modifiers"]["agility"]
                self.HP += part["modifiers"]["HP"]

                for i in part["resistances"]:
                    self.resistances.append(i)
                for i in part["weaknesses"]:
                    self.weaknesses.append(i)
                
                self.ui.printMessage(f"Part {part['part_name']} equipped in slot {slot}")
                self.ui.printMessage(f"New stats after part was equipped:")
                self.showStats()
                
                return self.showSlots()
            
            # Se o slot estiver ocupado
            else:
                # Removendo os modificadores antigos
                self.ui.printMessage(f"Slot {slot} already equipped with {self.slots[slot]['part_name']} part. Showing current stats.")
                self.showStats()
                
                self.ui.printMessage("Removing currently equipped part.")
                
                old_part = self.slots[slot]
                self.constitution -= old_part["modifiers"]["constitution"]
                self.strength -= old_part["modifiers"]["strength"]
                self.agility -= old_part["modifiers"]["agility"]
                self.HP -= old_part["modifiers"]["HP"]
                
                # Removendo as resistências e fraquezas da parte antiga.
                for i in old_part["resistances"]:
                    self.resistances.remove(i)
                for i in old_part["weaknesses"]:
                    self.weaknesses.remove(i)
                
                self.ui.printMessage(f"Part {old_part['part_name']} removed.")
                
                # Adicionando os modificadores nos atributos base do robô
                self.slots[part["slot"]] = part
                self.constitution += part["modifiers"]["constitution"]
                self.strength += part["modifiers"]["strength"]
                self.agility += part["modifiers"]["agility"]
                self.HP += part["modifiers"]["HP"]

                for i in part["resistances"]:
                    self.resistances.append(i)
                for i in part["weaknesses"]:
                    self.weaknesses.append(i)
                
                self.ui.printMessage(f"Part {part['part_name']} equipped in slot {slot}")
                self.ui.printMessage(f"New stats after part was equipped:")
                self.showStats()
                
                return self.showSlots()
       
        else:
            self.ui.printMessage(f"The part {part['part_name']} is meant to be equipped in the {part['slot']} slot. Not in the {slot} slot.")
    
    # Removendo uma peça de um slot.
    def cleanSlot(self, slot):
        
        # Checando se o slot está vazio
        if self.checkSlotIfEmpty(slot) is False:

            print(f"Slot {slot} already empty and available. Printing current robot stats.")

            self.showStats()

            return self.showSlots()

        # Se o slot estiver ocupado
        else:
            # Removendo os modificadores antigos
            print(f"Slot {slot} equipped with {self.slots[slot]['part_name']} part. Showing current stats.")
            self.showStats()

            print("Removing currently equipped part.")

            old_part = self.slots[slot]
            self.constitution -= old_part["modifiers"]["constitution"]
            self.strength -= old_part["modifiers"]["strength"]
            self.agility -= old_part["modifiers"]["agility"]
            self.HP -= old_part["modifiers"]["HP"]

            # Removendo as resistências e fraquezas da parte antiga.
            for i in old_part["resistances"]:
                self.resistances.remove(i)
            for i in old_part["weaknesses"]:
                self.weaknesses.remove(i)
                
            self.slots[slot] = None

            print(f"Part {old_part['part_name']} removed.")

            print(f"Updated stats after part was removed:")
            self.showStats()

            return self.showSlots()

    # Mostrar partes disponíveis
    def showParts(self, id_filter=None, slot_filter=None):
        
        # Primeiro, definindo o título
        if  id_filter is not None:
            title = f"Part Details (ID: {id_filter})"
        elif slot_filter is not None:
            title = f"Parts for Slot: {slot_filter}"
        else:
            title = f"All Parts"
        
        # Criando a tabela
        parts_table = self.ui.createPartsTable(title)    

        # Filtragem das partes
        found_parts = False
        
        for part in parts_list:
            
            # Manda continuar apenas se o id fornecido for diferente do id da parte iterada.
            if id_filter is not None and part["id"] != id_filter:
                continue
            
            # Mesma dinâmica, porém para as peças com slot diferente do procurado
            if slot_filter is not None and part["slot"] != slot_filter:
                continue
                
            # Caso isso tenha sido passado por ambos os filtros. Criamos a variável
            found_parts = True

            self.ui.addPartRow(parts_table, part)
            
            # Caso seja uma busca por ID único, a iteraçao acaba assim que encontra o ID
            if id_filter is not None:
                break
        
        # Valores de saída
        if found_parts:
            self.ui.console.print(parts_table)
        else:
            self.ui.printMessage("No pieces found.")
