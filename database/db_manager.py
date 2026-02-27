import sqlite3
import os

DB_PATH = "nintendo_sniper.db"

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    # Isso permite acessar colunas pelo nome (ex: row['nome']) em vez de apenas índice
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db_connection() # Usando a função que acabamos de criar
    cursor = conn.cursor()
    
    # Tabela de Jogos
    cursor.execute('''CREATE TABLE IF NOT EXISTS jogos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL, 
                        url TEXT NOT NULL, 
                        alvo REAL NOT NULL)''')
    
    # Tabela de Histórico
    cursor.execute('''CREATE TABLE IF NOT EXISTS historico (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        jogo_id INTEGER, 
                        preco REAL, 
                        data_hora TEXT,
                        FOREIGN KEY(jogo_id) REFERENCES jogos(id))''')

    # Tabela de Recordes
    cursor.execute('''CREATE TABLE IF NOT EXISTS recordes (
                        jogo_id INTEGER PRIMARY KEY,
                        menor_preco REAL, 
                        data_registro TEXT,
                        FOREIGN KEY(jogo_id) REFERENCES jogos(id))''')

    # Tabela de Configurações
    cursor.execute('''CREATE TABLE IF NOT EXISTS configuracoes (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        token TEXT,
                        chat_id TEXT)''')
    conn.commit()
    conn.close()

def salvar_config(token, chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO configuracoes (id, token, chat_id) VALUES (1, ?, ?)", (token, chat_id))
    conn.commit()
    conn.close()

def carregar_config():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT token, chat_id FROM configuracoes WHERE id = 1")
    res = cursor.fetchone()
    conn.close()
    return (res['token'], res['chat_id']) if res else (None, None)