# atualiza_e_testa_poster.py
import sqlite3
from ai_postagem import poster_produtos

DB = "mercado.db"

# --- Atualiza banco ---
conn = sqlite3.connect(DB)
cur = conn.cursor()

try: cur.execute("ALTER TABLE produtos ADD COLUMN ml_id TEXT;")
except: pass
try: cur.execute("ALTER TABLE produtos ADD COLUMN title TEXT;")
except: pass
try: cur.execute("ALTER TABLE produtos ADD COLUMN price REAL;")
except: pass
try: cur.execute("ALTER TABLE produtos ADD COLUMN seller_id TEXT;")
except: pass
try: cur.execute("ALTER TABLE produtos ADD COLUMN thumbnail TEXT;")
except: pass
try: cur.execute("ALTER TABLE produtos ADD COLUMN link TEXT;")
except: pass
try: cur.execute("ALTER TABLE produtos ADD COLUMN status TEXT DEFAULT 'active';")
except: pass
try: cur.execute("ALTER TABLE produtos ADD COLUMN publicado INTEGER DEFAULT 0;")
except: pass
try: cur.execute("ALTER TABLE produtos ADD COLUMN ml_item_id TEXT;")
except: pass

conn.commit()

# --- Adiciona alguns produtos de teste ---
produtos_teste = [
    ("Tênis Azul", 150.0, "https://via.placeholder.com/150", "IMG1"),
    ("Camiseta Preta", 50.0, "https://via.placeholder.com/150", "IMG2"),
    ("Fone de Ouvido", 120.0, "https://via.placeholder.com/150", "IMG3")
]

for nome, preco, thumbnail, ml_id in produtos_teste:
    try:
        cur.execute("""
            INSERT INTO produtos (nome, title, price, thumbnail, ml_id, status, publicado)
            VALUES (?,?,?,?,?, 'active', 0)
        """, (nome, nome, preco, thumbnail, ml_id))
    except:
        pass

conn.commit()
conn.close()

print("Banco atualizado e produtos de teste adicionados!")

# --- Executa poster_produtos ---
qtd = poster_produtos.run()
print(f"Anúncios criados: {qtd}")
