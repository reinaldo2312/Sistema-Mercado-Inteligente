import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time
import random

# ==========================
# Dados simulados / placeholders
# ==========================
clientes = [
    {"id": 0, "nome": "João", "carrinho": []},
    {"id": 1, "nome": "Maria", "carrinho": []}
]

produtos = [
    {"id": 0, "nome": "Tênis", "preco_vendedor": 100.0},
    {"id": 1, "nome": "Camiseta", "preco_vendedor": 50.0},
    {"id": 2, "nome": "Boné", "preco_vendedor": 30.0}
]

# ==========================
# Funções simuladas das AIs
# ==========================
def ai_menor_preco(produto):
    time.sleep(0.05)
    return produto["preco_vendedor"]  # placeholder

def ai_desconto(preco_cliente, preco_real):
    desconto = (preco_cliente - preco_real) * 0.05
    return round(preco_cliente - desconto, 2)

def ai_substituicao(produto):
    time.sleep(0.02)
    return produto  # placeholder

def ai_calculo_financeiro(preco_cliente, preco_vendedor):
    return round(preco_cliente - preco_vendedor, 2)

def ai_preparar_pedido(cliente, produtos_carrinho):
    pedido_final = {
        "cliente": cliente["nome"],
        "itens": [],
        "total_cliente": 0,
        "total_vendedor": 0,
        "lucro_total": 0
    }
    for produto in produtos_carrinho:
        preco_real = ai_menor_preco(produto)
        preco_cliente = ai_desconto(preco_real * 1.9, preco_real)  # simula markup
        lucro = ai_calculo_financeiro(preco_cliente, preco_real)
        pedido_final["itens"].append({
            "produto": produto["nome"],
            "preco_cliente": preco_cliente,
            "preco_vendedor": preco_real,
            "lucro": lucro
        })
        pedido_final["total_cliente"] += preco_cliente
        pedido_final["total_vendedor"] += preco_real
        pedido_final["lucro_total"] += lucro
    return pedido_final

# ==========================
# Orquestradora e AI reserva
# ==========================
def ai_orquestradora(cliente):
    try:
        carrinho = cliente["carrinho"]
        if not carrinho:
            return None
        pedido = ai_preparar_pedido(cliente, carrinho)
        return pedido
    except Exception as e:
        log_message(f"[ERRO] Orquestradora falhou: {e}. AI reserva assumindo.")
        pedido = ai_preparar_pedido(cliente, carrinho)
        return pedido

# ==========================
# Interface Tkinter
# ==========================
def log_message(msg):
    txt_log.configure(state='normal')
    txt_log.insert(tk.END, msg + "\n")
    txt_log.configure(state='disabled')
    txt_log.yview(tk.END)

def adicionar_produto():
    try:
        cid = int(entry_cliente.get())
        pid = int(entry_produto.get())
        cliente = next((c for c in clientes if c["id"] == cid), None)
        produto = next((p for p in produtos if p["id"] == pid), None)
        if cliente and produto:
            cliente["carrinho"].append(produto)
            log_message(f"[LOG] Produto '{produto['nome']}' adicionado ao carrinho de {cliente['nome']}")
        else:
            messagebox.showerror("Erro", "Cliente ou produto inválido")
    except:
        messagebox.showerror("Erro", "Informe IDs válidos")

def gerar_pedido():
    try:
        cid = int(entry_cliente.get())
        cliente = next((c for c in clientes if c["id"] == cid), None)
        if not cliente:
            messagebox.showerror("Erro", "Cliente inválido")
            return
        if not cliente["carrinho"]:
            messagebox.showinfo("Info", "Carrinho vazio")
            return

        def thread_exec():
            log_message(f"[LOG] Orquestradora iniciando para {cliente['nome']}")
            pedido = ai_orquestradora(cliente)
            if pedido:
                log_message(f"[LOG] Pedido final para {cliente['nome']}:")
                for item in pedido["itens"]:
                    log_message(f"  Produto: {item['produto']}, Preço Cliente: {item['preco_cliente']}, Preço Vendedor: {item['preco_vendedor']}, Lucro: {item['lucro']}")
                log_message(f"  Total Cliente: {round(pedido['total_cliente'],2)}, Total Vendedor: {round(pedido['total_vendedor'],2)}, Lucro Total: {round(pedido['lucro_total'],2)}")
                cliente["carrinho"].clear()

        threading.Thread(target=thread_exec).start()
    except Exception as e:
        log_message(f"[ERRO] Falha ao gerar pedido: {e}")

# ==========================
# Janela principal
# ==========================
janela = tk.Tk()
janela.title("Sistema Inteligente de Pedidos - Preparado para Mercado Livre")
janela.geometry("750x500")

tk.Label(janela, text="ID Cliente:").pack()
entry_cliente = tk.Entry(janela)
entry_cliente.pack()

tk.Label(janela, text="ID Produto:").pack()
entry_produto = tk.Entry(janela)
entry_produto.pack()

btn_add = tk.Button(janela, text="Adicionar Produto ao Carrinho", command=adicionar_produto, bg="#4CAF50", fg="white", height=2)
btn_add.pack(pady=5)

btn_gerar = tk.Button(janela, text="Consolidar Pedido / Gerar", command=gerar_pedido, bg="#2196F3", fg="white", height=2)
btn_gerar.pack(pady=5)

txt_log = scrolledtext.ScrolledText(janela, state='disabled', width=95, height=20)
txt_log.pack(pady=10)

janela.mainloop()






