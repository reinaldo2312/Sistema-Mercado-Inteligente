# ml_client.py
import time

# Função simulada para criar anúncio no Mercado Livre
def ml_create_item(title, price, images, category_id, quantity):
    """
    Simula a criação de um anúncio no Mercado Livre.
    Retorna um dict com o id do anúncio e informações.
    """
    # Simula um tempo de resposta da API
    time.sleep(0.2)
    
    # Cria um id fictício baseado no tempo ou preço
    anuncio_id = f"ML{int(time.time())}"
    
    print(f"[ml_client] Anúncio criado: {title} | ID: {anuncio_id} | Preço: {price}")
    
    return {
        "id": anuncio_id,
        "title": title,
        "price": price,
        "images": images,
        "category_id": category_id,
        "quantity": quantity
    }

# Função já existente, apenas exemplo
def ml_get_item(ml_id):
    """
    Simula a busca de um item pelo ID no Mercado Livre
    """
    # Aqui você poderia consultar a API real do ML
    return {
        "id": ml_id,
        "title": f"Produto {ml_id}",
        "price": 100.0,
        "images": [],
        "category_id": "ML_CATEGORY_ID",
        "quantity": 1
    }
