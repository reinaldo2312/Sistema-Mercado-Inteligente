from flask import Flask, request, jsonify
import sqlite3, json, datetime, os
from ai_orquestradora import Orquestradora
import ai_miners
from ai_postagem import poster_produtos

DB = "mercado.db"
app = Flask(__name__)

# ---------- Funções auxiliares ----------
def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # tabela produtos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        ml_id TEXT,
        title TEXT,
        price REAL,
        seller_id TEXT,
        thumbnail TEXT,
        link TEXT,
        status TEXT,
        estoque INTEGER,
        last_updated TEXT,
        publicado INTEGER DEFAULT 0,
        ml_item_id TEXT
    )
    """)

    # tabela vendedores
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendedores(
        id TEXT PRIMARY KEY,
        nome TEXT,
        reputacao REAL
    )
    """)

    # tabela pedidos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pedidos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        itens TEXT,
        total REAL,
        status TEXT
    )
    """)

    # tabela eventos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS eventos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        detalhes TEXT,
        criado_em TEXT
    )
    """)

    con.commit()
    con.close()

def log_event(tipo, detalhes):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO eventos (tipo, detalhes, criado_em) VALUES (?,?,?)",
                (tipo, json.dumps(detalhes), datetime.datetime.now().isoformat()))
    con.commit()
    con.close()

def fetch_all(query):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
    return rows

# ---------- Dados simulados e Orquestradora ----------
clientes = [{"id": 1, "nome": "João"}, {"id": 2, "nome": "Maria"}]
produtos = [{"id": 1, "nome": "Tênis", "preco_vendedor": 100}]
vendedores = [
    {"produto_id": 1, "preco": 95},
    {"produto_id": 1, "preco": 90},
]

orq = Orquestradora(clientes, produtos, vendedores)

# ---------- Rotas ----------
@app.route("/")
def home():
    return """
    Mercado Inteligente - Dashboard<br>
    /produtos<br>
    /vendedores<br>
    /ofertas<br>
    /pedidos<br>
    /events<br>
    /ia/status<br>
    /orquestra<br>
    /miner/status<br>
    /poster/run (GET ou POST)<br>
    Use API (POST/GET) para interagir.
    """

# --- produtos ---
@app.route("/produtos", methods=["GET","POST"])
def produtos_route():
    if request.method == "POST":
        d = request.get_json()
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("INSERT INTO produtos (nome, price, estoque) VALUES (?,?,?)",
                    (d["nome"], d["preco"], d["estoque"]))
        con.commit()
        con.close()
        log_event("produto_adicionado", d)
        return jsonify({"status":"ok"}), 201
    else:
        return jsonify(fetch_all("SELECT * FROM produtos"))

# --- vendedores ---
@app.route("/vendedores", methods=["GET","POST"])
def vendedores_route():
    if request.method == "POST":
        d = request.get_json()
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("INSERT INTO vendedores (id, nome, reputacao) VALUES (?,?,?)",
                    (d.get("id"), d["nome"], d["reputacao"]))
        con.commit()
        con.close()
        log_event("vendedor_adicionado", d)
        return jsonify({"status":"ok"}), 201
    else:
        return jsonify(fetch_all("SELECT * FROM vendedores"))

# --- ofertas ---
@app.route("/ofertas", methods=["GET"])
def ofertas_route():
    return jsonify({"melhor_oferta":"produtoX a R$ 50"})

# --- pedidos ---
@app.route("/pedidos", methods=["GET","POST"])
def pedidos_route():
    if request.method == "POST":
        d = request.get_json()
        con = sqlite3.connect(DB)
        cur = con.cursor()
        cur.execute("INSERT INTO pedidos (cliente, itens, total, status) VALUES (?,?,?,?)",
                    (d["cliente"], json.dumps(d["itens"]), d["total"], "pendente"))
        con.commit()
        con.close()
        log_event("pedido_criado", d)
        return jsonify({"status":"pedido recebido"}), 201
    else:
        return jsonify(fetch_all("SELECT * FROM pedidos"))

# --- eventos usando Orquestradora ---
@app.route("/events", methods=["POST"])
def events_post():
    d = request.get_json()
    if not d:
        return jsonify({"erro":"JSON inválido"}), 400

    # processa com Orquestradora
    pedido = orq.processar_evento(d)
    if pedido:
        return jsonify({"ok": True, "pedido": pedido}), 201
    else:
        return jsonify({"erro": "Evento inválido"}), 400

@app.route("/events", methods=["GET"])
def events_get():
    return jsonify(fetch_all("SELECT * FROM eventos ORDER BY criado_em DESC LIMIT 200"))

# --- status IA ---
@app.route("/ia/status")
def ia_status():
    return jsonify({"status":"IA ativa e monitorando"})

# --- orquestra pedidos com AI ---
@app.route("/orquestra", methods=["POST"])
def orquestra():
    data = request.get_json()
    if not data or "pedido" not in data:
        return jsonify({"erro": "Envie um JSON com a chave 'pedido'"}), 400
    
    resultado = orq.executar_fluxo(data["pedido"])
    return jsonify(resultado), 200

# --- miner status ---
@app.route("/miner/status")
def miner_status():
    try:
        resultados = ai_miners.run_all()
        return jsonify(resultados)
    except Exception as e:
        return jsonify({"status": "erro", "message": str(e)}), 500

# --- rodar poster de anúncios ---
@app.route("/poster/run", methods=["GET","POST"])
def poster_run_endpoint():
    try:
        qtd = poster_produtos.run()
        return {"message": "Anúncios criados pela AI", "total": qtd}, 200
    except Exception as e:
        return {"status": "erro", "message": str(e)}, 500

# ---------- Main ----------
if __name__ == "__main__":
    init_db()
    
    # Porta do Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
