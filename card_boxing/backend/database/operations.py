import sqlite3
import bcrypt

DB_NAME = 'card_game.db'

def create_user(username, password):

    password_bytes = password.encode('utf-8')

    hashed_password_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))

    hashed_password_string = hashed_password_bytes.decode('utf-8')

    conn = sqlite3.connect('card_game.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO players (username, password_hash)
            VALUES (?, ?)
        """, (username, hashed_password_string))

        conn.commit()
        return True, f"Usuário '{username}' criado com sucesso."
    
    except sqlite3.IntegrityError:
        return False, f"Erro: o nome de usuário '{username}' já existe."
    
    except Exception as e:
        # Retorno para o Flask em caso de OUTRO ERRO de DB
        return False, f"Erro interno ao registrar: {str(e)}"
    
    finally:
            cursor.close()
            conn.close()

def check_password(username, password_attempt):

    conn = sqlite3.connect('card_game.db')
    cursor = conn.cursor()

    try: 

        cursor.execute("""
            SELECT password_hash FROM players WHERE username = ?
    """, (username, ))
        
        result = cursor.fetchone()

        if result is None:
            print(f"Login falhou: Usuário '{username}' não encontrado.")
            return False
        
        hashed_password_from_db_string = result[0]

        password_attempt_bytes = password_attempt.encode('utf-8')
        hashed_password_from_db_byte = hashed_password_from_db_string.encode('utf-8')

        return bcrypt.checkpw(password_attempt_bytes, hashed_password_from_db_byte)
    except Exception as e:
        # Em caso de qualquer erro de DB, falha o login por segurança
        print(f"Erro ao verificar senha: {str(e)}")
        return False
            
    finally:
        cursor.close()
        conn.close()

# Retorna todas as peças no banco de dados
def get_parts_from_db():
    
    conn = sqlite3.connect('card_game.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT
        p.*,
        s.slot_name AS slot_name,
        t.type_name AS type_name,
        c.name AS card_name
    FROM robot_parts as p
    JOIN robot_slots s ON p.slot_id = s.id
    JOIN element_types t ON p.type = t.id
    LEFT JOIN cards c ON p.card_id = c.id
    """

    cursor.execute(query)

    all_parts = cursor.fetchall()

    return all_parts

# Função auxiliar para buscar IDs das fraquezas ou das resistências do tipo
def get_details(table_name, type_id, col_name):

    conn = sqlite3.connect('card_game.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT {col_name} FROM {table_name} WHERE type_id = ?", (type_id, ))
    return [row[0] for row in cursor.fetchall()]

# Função auxiliar para pegar os nomes dos tipos com base no ID
def get_type_names(table_name, type_id, col_to_return, col_to_filter):

    conn = sqlite3.connect('card_game.db')
    cursor = conn.cursor()

    query = f"""
        SELECT et.type_name
        FROM {table_name} t
        JOIN element_types et ON t.{col_to_return} = et.id
        WHERE t.{col_to_filter} = ?
    """

    cursor.execute(query, (type_id,))
    return [row[0] for row in cursor.fetchall()]

# Retorna todas as cartas no banco de dados
def get_cards_from_db():
    
    conn = sqlite3.connect('card_game.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT
        c.*,
        t.type_name AS type_name,
        e.effect_name AS effect_name,
        GROUP_CONCAT(p.part_name, ', ') AS requisitos_pecas
    FROM cards c
    JOIN element_types t ON c.type = t.id
    LEFT JOIN effects e ON c.effect_id = e.id
    LEFT JOIN robot_parts p ON c.id = p.card_id
    GROUP BY c.id
    """

    cursor.execute(query)

    all_parts = cursor.fetchall()

    return all_parts

# Retorna o robô e também todos os seus dados
def get_robot_with_stats(player_id):
    
    conn = sqlite3.connect('card_game.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT
        r.id,
        r.robot_name,
        ra.archetype_name,
        (ra.base_constitution + SUM(COALESCE(p.stat_constitution_mod, 0))) AS total_con,
        (ra.base_strength + SUM(COALESCE(p.stat_strength_mod, 0))) AS total_str,
        (ra.base_agility + SUM(COALESCE(p.stat_agility_mod, 0))) AS total_agi,
        (ra.base_hp + SUM(COALESCE(p.stat_hp_mod, 0))) AS total_hp
    FROM robots r
    JOIN robot_archetypes ra ON r.archetype_id = ra.id
    LEFT JOIN robot_equipped_parts rep ON r.id = rep.robot_id
    LEFT JOIN robot_parts p ON rep.part_id = p.id
    WHERE r.player_id = ?
    GROUP BY r.id
    """

    cursor.execute(query, (player_id,))
    return cursor.fetchall()

# Método para criar um robô no banco de dados
def create_robot_in_db(robot_name, archetype_id, player_id):
    
    conn = sqlite3.connect('card_game.db')
    cursor = conn.cursor()    
    
    try:
        query = """
        INSERT INTO robots (robot_name, player_id, archetype_id)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (robot_name, player_id, archetype_id))

        novo_id = cursor.lastrowid   

        conn.commit()
        return novo_id
        # Retornando o ID do robô criado
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")
        raise e
    finally:
        conn.close()

# Método para pegar os arquétipos do banco de dados
def get_archetypes_from_db():

    conn = sqlite3.connect('card_game.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT id, archetype_name FROM robot_archetypes
    """

    cursor.execute(query)
    archetypes = cursor.fetchall()

    conn.close()

    return archetypes

# Método para pegar os slots do banco de dados
def get_slots_from_db():

    conn = sqlite3.connect('card_game.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT * FROM robot_slots
    """

    cursor.execute(query)
    slots = cursor.fetchall()

    conn.close()

    return slots

# Pegar os detalhes de um robô pelo id
def get_equipped_parts_detailed(robot_id):
    conn = sqlite3.connect('card_game.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query para buscar os detalhes das partes equipadas ao robô em questão
    query = """
    SELECT 
        p.*, 
        s.slot_name AS slot_name, 
        t.type_name AS type_name,
        c.name AS card_name
    FROM robot_parts p
    JOIN robot_equipped_parts rep ON p.id = rep.part_id
    JOIN robot_slots s ON p.slot_id = s.id
    JOIN element_types t ON p.type = t.id
    LEFT JOIN cards c ON p.card_id = c.id
    WHERE rep.robot_id = ?
    """

    cursor.execute(query, (robot_id,))
    return cursor.fetchall()

# Pega todos os robôs do usuário
def get_full_robots_data(player_id):
    # Busca os robôs e stats
    rows = get_robot_with_stats(player_id)

    full_robots = []

    for robot in rows:
        # Busca as peças detalhadas deste robô em específico
        equipped_parts = get_equipped_parts_detailed(robot['id'])

        total_weaknesses = []
        total_resistances = []
        parts_list = []

        for part in equipped_parts:
            fw = get_type_names('type_weaknesses', part['type'], 'weak_to_id', 'type_id')
            tr = get_type_names('type_resistances', part['type'], 'resists_id', 'type_id')

            total_weaknesses.extend(fw)
            total_resistances.extend(tr)

            parts_list.append({
                'id': part['id'],
                'nome': part['part_name'],
                'slot': part['slot_name']
            })

        # Montando o dicionário para o font
        full_robots.append({
            'id': robot['id'],
            'name': robot['robot_name'],
            'archetype': robot['archetype_name'],
            'stats': {
                'constitution': robot['total_con'],
                'strength': robot['total_str'],
                'agility': robot['total_agi'],
                'hp': robot['total_hp']
            },
            'fraquezas': total_weaknesses,
            'resistencias': total_resistances,
            'parts': parts_list
        })
    
    return full_robots

# Método para renomear o robô
def rename_robot_on_db(new_name, robot_id):
    try:
        conn = sqlite3.connect('card_game.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE robots SET robot_name = ? WHERE id = ?", (new_name, robot_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao renomear no banco: {e}")
        return False
    
# Método para atualizar as peças do robô
def update_robot_parts_on_db(robot_id, parts_data):
    try:
        conn = sqlite3.connect('card_game.db')
        cursor = conn.cursor()

        # Removendo as peças do robô para evitar duplicatas
        cursor.execute("DELETE FROM robot_equipped_parts WHERE robot_id = ?", (robot_id,))

        # Inserindo as novas peças
        for item in parts_data:
            if item['part_id']:
                cursor.execute("""
                    INSERT INTO robot_equipped_parts (robot_id, slot_id, part_id)
                    VALUES (?, ?, ?)
            """, (robot_id, item['slot_id'], item['part_id']))
                
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Erro ao equipar peças no banco: {e}")
        return False