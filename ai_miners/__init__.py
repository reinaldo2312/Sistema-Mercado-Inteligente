# ai_miners/__init__.py
from . import miner_novos, miner_produtos, miner_precos, miner_removidos, miner_vendedores

def run_all():
    results = {}
    for name, miner in {
        "novos": miner_novos,
        "produtos": miner_produtos,
        "precos": miner_precos,
        "removidos": miner_removidos,
        "vendedores": miner_vendedores,
    }.items():
        try:
            count = miner.run()
            results[name] = {"status": "ok", "count": count}
        except Exception as e:
            results[name] = {"status": "erro", "detalhe": str(e)}
    return results

