# ai_miners/miner_produtos.py
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
                cur.execute("""UPDATE produtos 
                               SET title=?, price=?, seller_id=?, thumbnail=?, link=?, last_updated=datetime('now')
                               WHERE ml_id=?""",
                            (detalhes.get("title"), float(detalhes.get("price") or 0),
                             str(detalhes.get("seller_id") or ""), detalhes.get("thumbnail") or "",
                             f"https://produto.mercadolivre.com.br/{ml_id}", ml_id))
                count += 1
                conn.commit()
                time.sleep(0.2)
            except Exception as e:
                print("[miner_produtos] erro:", e)
    except Exception as e:
        print("[miner_produtos] erro geral:", e)

    conn.close()
    return count
