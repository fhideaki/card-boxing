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
            VALUES (?, ?, (SELECT id FROM robot_archetypes WHERE key = ?))
    """, (robot_name, player_id, archetype_key))
        
        conn.commit()
        return True
    except Exception as e:
        # Em caso de qualquer erro de DB, falha o login por segurança
        print(f"Erro ao verificar senha: {str(e)}")
        return False
            
    finally:
        cursor.close()
        conn.close()