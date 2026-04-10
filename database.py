import sqlite3

DB_NAME = "projeto.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_banco():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metricas (
        id INTEGER PRIMARY KEY,
        nome TEXT UNIQUE,
        valor INTEGER
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        usuario TEXT UNIQUE,
        senha TEXT
    )
    """)
    
    contadores = [('total_requests', 0), ('total_errors', 0), ('failed_logins', 0)]
    cursor.executemany("INSERT OR IGNORE INTO metricas (nome, valor) VALUES (?, ?)", contadores)
    
    cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, senha) VALUES (?, ?)", ('henrique', '123'))
    
    conn.commit()
    conn.close()

def verificar_login(user, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (user, password))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def incrementar_metrica(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE metricas SET valor = valor + 1 WHERE nome = ?", (nome,))
    conn.commit()
    conn.close()

def obter_metricas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, valor FROM metricas")
    dados = dict(cursor.fetchall())
    conn.close()
    return dados