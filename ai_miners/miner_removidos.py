# ai_miners/miner_removidos.py
import ml_client, time
import sqlite3

DB = "mercado.db"

def run():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    count = 0

    try:
        cur.execute("SELECT ml_id FROM produtos WHERE status='active'")
        produtos = cur.fetchall()

        for (ml_id,) in produtos:
            try:
                detalhes = ml_client.ml_get_item(ml_id)
                if detalhes.get("status") != "active":
                    cur.execute("UPDATE produtos SET status=?, last_updated=datetime('now') WHERE ml_id=?",
                                (detalhes.get("status"), ml_id))
                    count += 1
                conn.commit()
                time.sleep(0.2)
            except Exception as e:
                print("[miner_removidos] erro:", e)
    except Exception as e:
        print("[miner_removidos] erro geral:", e)

    conn.close()
    return count

