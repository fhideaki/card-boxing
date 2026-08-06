# UI "nula" usada pelo motor de batalha quando ele roda via API em vez de terminal.
# Captura as mensagens de log em uma lista ao invés de imprimir com rich/console,
# e vira no-op para os métodos de renderização de tabela (não fazem sentido numa resposta JSON).
class NullUIManager:
    def __init__(self):
        self.messages = []
        self.console = self

    def printMessage(self, message):
        self.messages.append(message)

    def print(self, *args, **kwargs):
        pass

    def createStatsTable(self, title):
        return None

    def addStatsRow(self, table, row):
        pass

    def createSlotsTable(self, title):
        return None

    def addSlotsRow(self, table, row):
        pass

    def createPartsTable(self, title):
        return None

    def addPartRow(self, table, part):
        pass

    def createCardsTable(self, title):
        return None

    def addCardRow(self, table, card):
        pass

    def createCurrentStatsTable(self, title):
        return None

    def addCurrentStatsRow(self, table, row):
        pass
