# ai_orquestradora.py

import datetime

class Orquestradora:
    def __init__(self, clientes=None, produtos=None, vendedores=None, interval_seconds=60):
        self.clientes = clientes or []
        self.produtos = produtos or []
        self.vendedores = vendedores or []
        self.interval_seconds = interval_seconds

    def processar_evento(self, evento):
        """
        Recebe evento (dict) e simula criação de pedido.
        Retorna pedido simulado ou None se inválido.
        """
        if not evento or "produto_id" not in evento or "cliente_id" not in evento:
            return None

        pedido = {
            "id": int(datetime.datetime.now().timestamp()),
            "cliente_id": evento["cliente_id"],
            "produto_id": evento["produto_id"],
            "preco": evento.get("preco", 100),
            "criado_em": datetime.datetime.now().isoformat()
        }
        return pedido

    def executar_fluxo(self, pedido):
        """
        Simula execução de fluxo de orquestração para pedido
        """
        pedido["status"] = "processado"
        pedido["processado_em"] = datetime.datetime.now().isoformat()
        return pedido

    def start_background(self):
        """
        Simula loop em background (não obrigatório)
        """
        import threading, time
        def worker():
            while True:
                # Aqui você poderia varrer produtos e criar ofertas automáticas
                time.sleep(self.interval_seconds)
        t = threading.Thread(target=worker, daemon=True)
        t.start()
