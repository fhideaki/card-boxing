# Imports
import sqlite3

def init_db():

    # Conectando ao DB
    conn = sqlite3.connect('card_game.db')
    conn.execute("PRAGMA foreign_keys = ON;")

    # Criando um cursor
    cursor = conn.cursor()

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

    # Tabela de tipos (materiais/ elementos)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS element_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name TEXT NOT NULL UNIQUE
    )
    """)

    # Tabela de cartas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        class TEXT NOT NULL,  
        type INTEGER NOT NULL,
        description TEXT,
        effect_id INTEGER,

        FOREIGN KEY (type) REFERENCES element_types(id),
        FOREIGN KEY (effect_id) REFERENCES effects(id)
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
        image_url TEXT NOT NULL DEFAULT 'parts/default.png',

        FOREIGN KEY (slot_id) REFERENCES robot_slots (id),
        FOREIGN KEY (type) REFERENCES element_types(id)
        FOREIGN KEY (card_id) REFERENCES cards (id)
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

    # Tabela de cartas possíveis para cada robô
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS robot_available_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        robot_id INTEGER NOT NULL,
        card_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        source TEXT,

        FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE,
        FOREIGN KEY (card_id) REFERENCES cards(id),

        UNIQUE (robot_id, card_id)  
    )
    """)


    # Tabela do deck ativo do robô
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS robot_decks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        robot_id INTEGER NOT NULL,
        card_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,

        FOREIGN KEY (robot_id) REFERENCES robots(id) ON DELETE CASCADE,
        FOREIGN KEY (card_id) REFERENCES cards(id)
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

    # Tabela de cartas base para cada arquétipo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS archetype_starting_cards (
        archetype_id INTEGER NOT NULL,
        card_id INTEGER NOT NULL,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (archetype_id) REFERENCES robot_archetypes (id),
        FOREIGN KEY (card_id) REFERENCES cards (id),
        PRIMARY KEY (archetype_id, card_id)
    )
    """)

    archetypes = [
        ('atk', 6, 10, 8, 6),
        ('def', 10, 6, 6, 8),
        ('bal', 7, 7, 7, 7),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO robot_archetypes
            (archetype_name, base_constitution, base_strength, base_agility, base_hp)
            VALUES (?, ?, ?, ?, ?)
        """, archetypes)

    slots = [
        ('head',),
        ('body',),
        ('right_arm',),
        ('left_arm',),
        ('right_leg',),
        ('left_leg',)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO robot_slots
            (slot_name)
            VALUES (?)
        """, slots)
    
    effects = [
        ('Clinch', 'Clinch, holds the opponent fighter. Vulnerable to opponents attacks. Effective against opponents guards.'),
        ('Double Damage', 'Strong Attack. If the opponent clinches, it does double damage.'),
        ('Invincible', 'Special Guard. Makes the user invulnerable to everything.'),
        ('Stop Hitting Yourself', 'It returns some damage to the oponent if they choose to attack.'),
        ('White Hot Fire Punch', 'Attack that leaves the opponent with a burn. If it lands, the opponent loses one slot of his hand until the end of the round.'),
        ('Omniclinch', 'Automatically clinches if it lands. It works even against attacks but does not protect against damage.')
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO effects
        (effect_name, description)
        VALUES (?, ?)
    """, effects)
 
    types = [
        ('Neutral',),
        ('Fire',),
        ('Water',),
        ('Iron',),
        ('Rubber',),
        ('Sand',)
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO element_types
        (type_name)
        VALUES (?)
    """, types)

    cards = [
        ('Simple Guard', 'guard', 'Neutral', 'Simple Guard. Protects against Attack from opponent.It still can be Clinched', None),
        ('Simple Attack', 'attack', 'Neutral', 'Simple Attack. Does damage even if the opponent Attacks or Clinches. It can be blocked by Simple Guard.', None),
        ('Clinch', 'clinch', 'Neutral', 'Clinch, holds the opponent fighter. Vulnerable to opponents attacks. Strong against opponents guards.', 'Clinch'),
        ('Strong Attack', 'attack', 'Neutral', 'Strong Attack. If the opponent clinches, it does double damage. Does regular damage against Simple Guard.', 'Double Damage'),
        ('Special Guard', 'guard', 'Neutral', 'Special Guard. Makes the user invulnerable to everything.', 'Invincible'),
        ('Iron Guard', 'guard', 'Iron', 'The Iron Guard is so strong that it returns some damage to the oponent if they choose to attack.', 'Stop Hitting Yourself'),
        ('Fiery Punch', 'attack', 'Fire', 'Attack that leaves the opponent with a burn. If it lands, the opponent loses one slot of his hand for the end of the round.', 'White Hot Fire Punch'),
        ('Rubber Attack', 'attack', 'Rubber', 'Hits weakly and automatically clinches if it lands.', 'Omniclinch')
    ]
    
    cursor.executemany("""
        INSERT OR IGNORE INTO cards (
            name, 
            class,
            type,
            description,
            effect_id
        ) VALUES (
            ?,
            ?,
            (SELECT id FROM element_types WHERE type_name = ?),
            ?,
            (SELECT id FROM effects WHERE effect_name = ?)
        )
    """, cards)
     
    parts = [
        ('Iron Head', 'A solid Iron head made from pieces found in the scrapyard. If the fighter gets a full set of iron parts, it gets an extra bonus.', 'head', 'Iron', 'Iron Guard', 2, 0, -2, 2),
        ('Blazing Arm', 'A regular fighter arm bathed in a flammable substance and lit on fire. It increases the damage output but the fire also harms the user.', 'right_arm', 'Fire', 'Fiery Punch', -2, 2, 2, -2),
        ('Rubber Arm', 'A rubber arm that is very flexible and helps holding the opponent. But it is not that powerful.', 'left_arm', 'Rubber', 'Rubber Attack', 1, -1, 3, 0),
        ('Iron Body', 'A body part made of iron. Very heavy and durable. If the fighter gets a full set of iron parts, it gets an extra bonus.', 'body', 'Iron', None, 6, 0, -6, 4),
        ('Rubber Body', 'A body made of very flexible rubber. It is very effective withstanding attacks without losing agility. If the fighter gets a full set of rubber parts, it unlocks a new special card.', 'body', 'Rubber', None, 2, -1, 2, 0),
        ('Iron Leg', 'Looks like a very thick nail, but who can tell? If the fighter gets a full set of iron parts, it gets an extra bonus.', 'right_leg', 'Iron', None, 3, 0, -2, 2),
        ('Rubber Leg', 'A leg made of very flexible rubber. It increases agility but sacrifices power. If the fighter gets a full set of rubber parts, it unlocks a new special card.', 'left_leg', 'Rubber', None, 1, -2, 3, 0)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO robot_parts (
            part_name, 
            description,
            slot_id, 
            type,
            card_id,
            stat_constitution_mod,
            stat_strength_mod,
            stat_agility_mod,
            stat_hp_mod
        ) VALUES (
            ?,
            ?,
            (SELECT id FROM robot_slots WHERE slot_name = ?),
            (SELECT id FROM element_types WHERE type_name = ?),
            (SELECT id FROM cards WHERE name = ?),
            ?,
            ?,
            ?,
            ?
        )
    """, parts)

    weaknesses = [
            ('Neutral', 'Iron'),
            ('Fire', 'Water'),
            ('Fire', 'Sand'),
            # Water não tem fraquezas
            ('Iron', 'Fire'),
            ('Rubber', 'Fire'),
            ('Sand', 'Iron'),
            ('Sand', 'Water')
        ]

    cursor.executemany("""
        INSERT OR IGNORE INTO type_weaknesses (
            type_id,
            weak_to_id
        ) VALUES (
            (SELECT id FROM element_types WHERE type_name = ?),
            (SELECT id FROM element_types WHERE type_name = ?)           
        )
    """, weaknesses)

    resistances = [
        ('Neutral', 'Rubber'),
        ('Fire', 'Rubber'),
        ('Water', 'Fire'),
        ('Water', 'Iron'),
        ('Iron', 'Rubber'),
        ('Iron', 'Neutral'),
        ('Iron', 'Sand'),
        ('Rubber', 'Neutral'),
        ('Sand', 'Fire')
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO type_resistances (
            type_id,
            resists_id
        ) VALUES (
            (SELECT id FROM element_types WHERE type_name = ?),
            (SELECT id FROM element_types WHERE type_name = ?)           
        )
    """, resistances)

    archetype_cards_data = [
        # Arquétipo ATK (Ataque)
        ('atk', 1, 3), # Simple Guard
        ('atk', 2, 3), # Simple Attack
        ('atk', 3, 3), # Clinch
        ('atk', 4, 2), # Strong Attack

        # Arquétipo DEF (Defesa)
        ('def', 1, 3),
        ('def', 2, 3),
        ('def', 3, 3),
        ('def', 5, 2), # Special Guard

        # Arquétipo BAL (Balanceado)
        ('bal', 1, 3),
        ('bal.id', 2, 3),
        ('bal', 3, 3),
        ('bal', 4, 1), # Strong Attack
        ('bal', 5, 1)  # Special Guard
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO archetype_starting_cards (
            archetype_id,
            card_id,
            quantity
        ) VALUES (
            (SELECT id FROM robot_archetypes WHERE archetype_name = ?),
            ?,
            ?
        )
    """, archetype_cards_data)

    conn.commit()
    conn.close()