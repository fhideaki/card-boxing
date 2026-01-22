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

def insert_robot_in_db(robot_name, player_id, archetype_key):

    conn = sqlite3.connect('card_game.db')
    cursor = conn.cursor()

    try: 
        cursor.execute("""
            INSERT INTO robots (robot_name, player_id, archetype_id)
            VALUES (?, ?, (SELECT id FROM robot_archetypes WHERE archetype_name = ?))
    """, (robot_name, player_id, archetype_key))
        
        robot_id = cursor.lastrowid
        conn.commit()
        return robot_id
    
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