import sqlite3
import datetime

DB = "mercado.db"

def run():
    """
    Cria anúncios automáticos para produtos não publicados.
    Retorna a quantidade de anúncios criados.
    """
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("SELECT id, nome, price, estoque FROM produtos WHERE publicado=0")
    produtos = cur.fetchall()
    total_criados = 0

    for p in produtos:
        produto_id, nome, price, estoque = p

        # Marca como publicado
        cur.execute("UPDATE produtos SET publicado=1, last_updated=? WHERE id=?",
                    (datetime.datetime.now().isoformat(), produto_id))
        total_criados += 1

    con.commit()
    con.close()
    return total_criados
