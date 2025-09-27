# ai_miners/miner_precos.py
import ml_client, time
import sqlite3

DB = "mercado.db"

def run():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    count = 0

    try:
        cur.execute("SELECT ml_id FROM produtos")
        produtos = cur.fetchall()

        for (ml_id,) in produtos:
            try:
                detalhes = ml_client.ml_get_item(ml_id)
                cur.execute("UPDATE produtos SET price=?, last_updated=datetime('now') WHERE ml_id=?",
                            (float(detalhes.get("price") or 0), ml_id))
                count += 1
                conn.commit()
                time.sleep(0.2)
            except Exception as e:
                print("[miner_precos] erro:", e)
    except Exception as e:
        print("[miner_precos] erro geral:", e)

    conn.close()
    return count

