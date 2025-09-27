# ai_helper.py
def analisar_pedido(pedido):
    # Exemplo simples de análise
    return {
        "status": "ok",
        "produto_original": pedido.get("produto", "desconhecido"),
        "sugestao": f"Produto alternativo mais barato para {pedido.get('produto', 'desconhecido')}",
        "lucro_estimado": round(pedido.get("preco", 0) * 0.15, 2)  # simulação de 15% de lucro
    }