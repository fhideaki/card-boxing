# Aqui fica um arquivo responsável por gerenciar a exibição das tabelas de cartas, peças e mensagens para o usuário

# Imports
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout

class UIManager:
    def __init__(self):
        self.console = Console()
        
    # Método para printar mensagens
    def printMessage(self, message:str):
        self.console.print(Text(message))

    # Método para criar a estrutura da tabela de cards
    @staticmethod
    def createCardsTable(title):
        # Cria a tabela
        cards_table = Table(title=title)
        
        #Cria as colunas da tabela
        cards_table.add_column("ID")
        cards_table.add_column("Card Name")        
        cards_table.add_column("Class")  
        cards_table.add_column("Type")
        cards_table.add_column("Description")

        return cards_table
    
    # Método para formatar cada linha da tabela
    def addCardRow(self, cards_table, card):
        
        cards_table.add_row(
            str(card["id"]),
            card["name"],
            card["class"],
            card["type"],
            card["description"]
#             ", ".join(part["resistances"]) if part["resistances"] else "N/A",
#             ", ".join(part["weaknesses"]) if part["weaknesses"] else "N/A"
        )

        self.console.print(cards_table)

    # Método para criar a estrutura da tabela de status atuais
    @staticmethod
    def createCurrentStatsTable(title):
        # Cria a tabela
        current_stats_table = Table(title=title)
                
        #Cria as colunas da tabela
        current_stats_table.add_column("HP")
        current_stats_table.add_column("Con")        
        current_stats_table.add_column("Str")  
        current_stats_table.add_column("Agi")
        current_stats_table.add_column("Def")
        current_stats_table.add_column("Atk")
        current_stats_table.add_column("Cli")    
        current_stats_table.add_column("Resistances")        
        current_stats_table.add_column("Weaknesses")

        return current_stats_table
    
    # Método para formatar cada linha da tabela
    def addCurrentStatsRow(self, stats_table, stats_list):
        
        # Monta a tabela
        stats_table.add_row(*stats_list)

        # Printa a tabela
        self.console.print(stats_table)

    # Método para criar a estrutura da tabela de partes
    @staticmethod
    def createPartsTable(title):
        # Cria a tabela
        parts_table = Table(title=title)
        
        #Cria as colunas da tabela
        parts_table.add_column("ID")
        parts_table.add_column("Part Name")        
        parts_table.add_column("Slot")  
        parts_table.add_column("Type")
        parts_table.add_column("Description")
        parts_table.add_column("Con")        
        parts_table.add_column("Str")        
        parts_table.add_column("Agi")
        parts_table.add_column("HP")           
        parts_table.add_column("Resistances")        
        parts_table.add_column("Weaknesses")
        
        return parts_table

    # Método para formatar cada linha da tabela
    def addPartRow(self, parts_table, part):
        
        parts_table.add_row(
            str(part["id"]),
            part["part_name"],
            part["slot"],
            part["type"],
            part["description"],
            str(part["modifiers"]["constitution"]),
            str(part["modifiers"]["strength"]),
            str(part["modifiers"]["agility"]),
            str(part["modifiers"]["HP"]),
            ", ".join(part["resistances"]) if part["resistances"] else "N/A",
            ", ".join(part["weaknesses"]) if part["weaknesses"] else "N/A"
        )

    # Método para criar a estrutura da tabela de stats
    @staticmethod
    def createStatsTable(title):
        # Cria a tabela
        stats_table = Table(title=title)
                
        #Cria as colunas da tabela
        stats_table.add_column("HP")
        stats_table.add_column("Con")        
        stats_table.add_column("Str")  
        stats_table.add_column("Agi")
        stats_table.add_column("Def")
        stats_table.add_column("Atk")
        stats_table.add_column("Cli")    
        stats_table.add_column("Resistances")        
        stats_table.add_column("Weaknesses")

        return stats_table
    
    # Método para formatar cada linha da tabela
    def addStatsRow(self, stats_table, stats_list):
        
        # Monta a tabela
        stats_table.add_row(*stats_list)

        # Printa a tabela
        self.console.print(stats_table)
        
    @staticmethod
    def createSlotsTable(title):
        # Cria a tabela
        robot_slots = Table(title=title)

        # Cria a coluna da tabela
        robot_slots.add_column("Slot")
        robot_slots.add_column("Part ID")
        robot_slots.add_column("Part Name")
        robot_slots.add_column("Part Type")
        
        return robot_slots
    
    # Método para formatar cada linha da tabela
    def addSlotsRow(self, slots_table, slots_list):
        
        # Monta a tabela
        slots_table.add_row(*slots_list)