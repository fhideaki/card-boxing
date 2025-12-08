# Imports
import sqlite3

# Conectando ao DB
conn = sqlite3.connect('card_game.db')

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

conn.commit()
conn.close()