# ai_miners/miner_vendedores.py
import ml_client, time
import sqlite3

DB = "mercado.db"

def run():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    count = 0

    try:
        cur.execute("SELECT DISTINCT seller_id FROM produtos WHERE seller_id IS NOT NULL AND seller_id != ''")
        vendedores = cur.fetchall()

        for (seller_id,) in vendedores:
            try:
                vendedor = ml_client.ml_get_seller(seller_id)
                cur.execute("""INSERT OR REPLACE INTO vendedores (id, nome, reputacao) VALUES (?,?,?)""",
                            (seller_id, vendedor.get("nickname"), float(vendedor.get("reputation_level") or 0)))
                count += 1
                conn.commit()
                time.sleep(0.2)
            except Exception as e:
                print("[miner_vendedores] erro:", e)
    except Exception as e:
        print("[miner_vendedores] erro geral:", e)

    conn.close()
    return count
