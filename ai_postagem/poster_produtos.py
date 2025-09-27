# ai_postagem/poster_produtos.py
import sqlite3
from ml_client import ml_create_item

DB = "mercado.db"

def run():
    """
    Pega produtos não publicados e cria anúncios usando ml_create_item.
    Retorna a quantidade de anúncios criados.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    # Seleciona produtos ativos e não publicados
    cur.execute("SELECT id, title, price, thumbnail, ml_id FROM produtos WHERE status='active' AND publicado=0")
    rows = cur.fetchall()
    
    count = 0
    for row in rows:
        produto_id, title, price, thumbnail, ml_id = row
        
        try:
            # Chama a função que cria anúncio no Mercado Livre
            anuncio = ml_create_item(
                title=title,
                price=price,
                images=[thumbnail],
                category_id="ML_CATEGORY_ID",
                quantity=1
            )
            
            # Marca como publicado
            cur.execute("UPDATE produtos SET publicado=1, ml_item_id=? WHERE id=?", (anuncio["id"], produto_id))
            conn.commit()
            
            print(f"[poster_produtos] Anúncio criado: {title} | ID ML: {anuncio['id']}")
            count += 1
            
        except Exception as e:
            print(f"[poster_produtos] Erro ao criar anúncio {title}: {e}")
    
    conn.close()
    return count
