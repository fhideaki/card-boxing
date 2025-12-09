from damage_calculator import *
from deck import *
from effects import *
from game_judge import *
from player import *
from robot import *
from static import *
from ui_manager import *
from turn import *

# # Criando a UI
# ui = UIManager()

# # Criando um jogador
# ferpas = Player('Ferna', 'Terminator', 'atk', ui)

# # Equipando itens no robo
# iron_head = parts_list[0]
# blazing_arm = parts_list[1]
# rubber_arm = parts_list[2]
# iron_body = parts_list[3]
# rubber_body = parts_list[4]
# iron_leg = parts_list[5]
# rubber_leg = parts_list[6]

# ferpas.robot.setSlot('head', iron_head)
# ferpas.robot.setSlot('right_arm', blazing_arm)
# ferpas.robot.setSlot('body', iron_body)
# ferpas.robot.setSlot('left_arm', rubber_arm)

# paulo = Player('Colan', 'Mach35', 'bal', ui)
# paulo.robot.setSlot('head', iron_head)
# paulo.robot.setSlot('body', iron_body)
# paulo.robot.setSlot('left_arm', rubber_arm)

# # Robos equipados, criando o juiz e a calculadora
# calculadora = DamageCalculator(ui)
# juiz = GameJudge(ui, calculadora)

# # Preparando os jogadores com as cartas especiais
# ferpas.setDeck()
# paulo.setDeck()

# turno = Turn(ferpas, paulo, juiz, calculadora)

# turno.game_start()

# for i in range(3):
#     turno.execute_first_phase()
#     turno.execute_second_phase()
#     turno.execute_third_phase()
#     print(f'Cartas descartadas  P1 - {len(ferpas.graveyard)}')
#     print(f'Cartas descartadas  P2 - {len(paulo.graveyard)}')

import sqlite3
from pathlib import Path

DB_PATH = Path("game.db")

def create_tables(conn):
    cur = conn.cursor()

    # ---- TABLE: effects ----
    cur.execute("""
        CREATE TABLE IF NOT EXISTS effects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            payload_schema TEXT  -- JSON descrevendo que parâmetros esse efeito usa
        );
    """)

    # ---- TABLE: cards ----
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            class TEXT NOT NULL,
            speed INTEGER NOT NULL,
            base_damage INTEGER NOT NULL
        );
    """)

    # ---- TABLE: conflicts ----
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conflicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_p1 TEXT NOT NULL,
            class_p2 TEXT NOT NULL,
            winner TEXT NOT NULL,  -- 'p1', 'p2' ou 'tie'
            winning_class TEXT NOT NULL
        );
    """)

    # ---- TABLE: card_effects ----
    cur.execute("""
        CREATE TABLE IF NOT EXISTS card_effects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER NOT NULL,
            effect_id INTEGER NOT NULL,
            effect_payload TEXT,  -- parâmetros específicos em JSON
            FOREIGN KEY(card_id) REFERENCES cards(id),
            FOREIGN KEY(effect_id) REFERENCES effects(id)
        );
    """)

    conn.commit()


def seed_data(conn):
    cur = conn.cursor()

    # Insert sample effects
    cur.execute("INSERT OR IGNORE INTO effects (name, description, payload_schema) VALUES (?, ?, ?)",
                ("damage_boost", "Aumenta o dano aplicado", '{"amount": "int"}'))

    cur.execute("INSERT OR IGNORE INTO effects (name, description, payload_schema) VALUES (?, ?, ?)",
                ("clinch", "Impede o inimigo de comprar carta no próximo turno", '{}'))

    # Insert sample cards
    cur.execute("INSERT OR IGNORE INTO cards (name, class, speed, base_damage) VALUES (?, ?, ?, ?)",
                ("Punch", "attack", 5, 10))

    cur.execute("INSERT OR IGNORE INTO cards (name, class, speed, base_damage) VALUES (?, ?, ?, ?)",
                ("Shield", "defense", 2, 0))

    # Insert sample conflict rule
    cur.execute("INSERT OR IGNORE INTO conflicts (class_p1, class_p2, winner, winning_class) VALUES (?, ?, ?, ?)",
                ("attack", "defense", "p2", "defense"))

    # Insert effect assigned to a card
    cur.execute("""
        INSERT OR IGNORE INTO card_effects (card_id, effect_id, effect_payload)
        VALUES (
            (SELECT id FROM cards WHERE name='Punch'),
            (SELECT id FROM effects WHERE name='damage_boost'),
            '{"amount": 5}'
        );
    """)

    conn.commit()


def show_data(conn):
    cur = conn.cursor()

    print("\n--- EFFECTS ---")
    for row in cur.execute("SELECT * FROM effects"):
        print(row)

    print("\n--- CARDS ---")
    for row in cur.execute("SELECT * FROM cards"):
        print(row)

    print("\n--- CONFLICTS ---")
    for row in cur.execute("SELECT * FROM conflicts"):
        print(row)

    print("\n--- CARD_EFFECTS ---")
    for row in cur.execute("SELECT * FROM card_effects"):
        print(row)


if __name__ == "__main__":
    print(">> Criando/abrindo game.db...")

    conn = sqlite3.connect(DB_PATH)

    print(">> Criando tabelas...")
    create_tables(conn)

    print(">> Inserindo dados exemplo...")
    seed_data(conn)

    print(">> Lendo dados do banco...")
    show_data(conn)

    conn.close()
    print("\n>> Teste concluído!")
