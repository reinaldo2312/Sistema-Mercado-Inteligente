# ai_miners/miner_novos.py
import ml_client, time
import sqlite3

DB = "mercado.db"

def run():
    termos = ["tenis", "camiseta", "fone de ouvido", "smartphone", "notebook"]
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    count = 0

    for termo in termos:
        try:
            itens = ml_client.ml_search_items(termo, limit=12)
            for it in itens:
                exists = cur.execute("SELECT 1 FROM produtos WHERE ml_id=?", (it['id'],)).fetchone()
                if not exists:
                    cur.execute("""INSERT INTO produtos 
                                   (ml_id, title, price, seller_id, thumbnail, link, status, last_updated)
                                   VALUES (?,?,?,?,?,?,?,datetime('now'))""",
                                (it['id'], it.get('title'), float(it.get('price') or 0),
                                 str(it.get('seller_id') or ""), it.get('thumbnail') or "",
                                 f"https://produto.mercadolivre.com.br/{it['id']}", "active"))
                    count += 1
            conn.commit()
            time.sleep(0.3)
        except Exception as e:
            print("[miner_novos] erro:", e)

    conn.close()
    return count

