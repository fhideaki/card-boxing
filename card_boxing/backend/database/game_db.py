# Imports
import sqlite3

# Conectando ao DB
conn = sqlite3.connect('card_game.db')

# Criando um cursor
cursor = conn.cursor()
conn.execute("PRAGMA foreign_keys = ON;")

# Criando a tabela dos jogadores
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
)
""")

# Tabela dos arquétipos de robôs
cursor.execute("""
CREATE TABLE IF NOT EXISTS robot_archetypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    archetype_name TEXT NOT NULL UNIQUE,
    base_constitution INTEGER NOT NULL,
    base_strength INTEGER NOT NULL,
    base_agility INTEGER NOT NULL,
    base_hp INTEGER NOT NULL
)
""")

# Tabela dos slots
cursor.execute("""
CREATE TABLE IF NOT EXISTS robot_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot_name TEXT NOT NULL UNIQUE
)
""")

# Tabela de efeitos
cursor.execute("""
CREATE TABLE IF NOT EXISTS effects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    effect_name TEXT NOT NULL UNIQUE,
    description TEXT
)
""")

# Tabela de cartas
cursor.execute("""
CREATE TABLE IF NOT EXISTS special_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    class TEXT NOT NULL,  
    type INTEGER NOT NULL,
    description TEXT,
    effect_id INTEGER,

    FOREIGN KEY (type) REFERENCES element_types(id)
    FOREIGN KEY (effect_id) REFERENCES effects(id)
)
""")

# Tabela de tipos (materiais/ elementos)
cursor.execute("""
CREATE TABLE IF NOT EXISTS element_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL UNIQUE
)
""")

# Tabela de fraquezas dos tipos (materiais/ elementos)
cursor.execute("""
CREATE TABLE IF NOT EXISTS type_weaknesses (
    type_id INTEGER NOT NULL,
    weak_to_id INTEGER NOT NULL,

    FOREIGN KEY (type_id) REFERENCES element_types(id),
    FOREIGN KEY (weak_to_id) REFERENCES element_types(id),
    PRIMARY KEY (type_id, weak_to_id)
)
""")

# Tabela de resistências dos tipos (materiais/ elementos)
cursor.execute("""
CREATE TABLE IF NOT EXISTS type_resistances (
    type_id INTEGER NOT NULL,
    resists_id INTEGER NOT NULL,

    FOREIGN KEY (type_id) REFERENCES element_types(id),
    FOREIGN KEY (resists_id) REFERENCES element_types(id),
    PRIMARY KEY (type_id, resists_id)
)
""")

# Tabela de partes do robô
cursor.execute("""
CREATE TABLE IF NOT EXISTS robot_parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_name TEXT NOT NULL UNIQUE,
    description TEXT,
    slot_id INTEGER NOT NULL,
    type INTEGER NOT NULL,
    card_id INTEGER,
    stat_constitution_mod INTEGER DEFAULT 0,
    stat_strength_mod INTEGER DEFAULT 0,
    stat_agility_mod INTEGER DEFAULT 0,
    stat_hp_mod INTEGER DEFAULT 0,

    FOREIGN KEY (slot_id) REFERENCES robot_slots (id),
    FOREIGN KEY (type) REFERENCES element_types(id)
    FOREIGN KEY (card_id) REFERENCES special_cards (id)
)
""")

# Tabela dos robôs criados
cursor.execute("""
CREATE TABLE IF NOT EXISTS robots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    robot_name TEXT NOT NULL,
    player_id INTEGER NOT NULL,
    archetype_id INTEGER NOT NULL,
    
    FOREIGN KEY (player_id) REFERENCES players (id) ON DELETE CASCADE,
    FOREIGN KEY (archetype_id) REFERENCES robot_archetypes (id)
)
""")

# Tabela dos robôs com peças
cursor.execute("""
CREATE TABLE IF NOT EXISTS robot_equipped_parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    robot_id INTEGER NOT NULL,
    part_id INTEGER NOT NULL,
    slot_id INTEGER NOT NULL,

    FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE,
    FOREIGN KEY (part_id) REFERENCES robot_parts(id),
    FOREIGN KEY (slot_id) REFERENCES robot_slots(id),

    UNIQUE (robot_id, slot_id)
)
""")


conn.commit()
conn.close()