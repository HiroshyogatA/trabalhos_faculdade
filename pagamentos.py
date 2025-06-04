import tkinter as tk
from tkinter import ttk, messagebox
from bd import conectar_banco

def mostrar_pagamentos(conteudo, root):
    for widget in conteudo.winfo_children():
        widget.destroy()

    top = tk.Frame(conteudo)
    top.pack(fill="x")
    tk.Label(top, text="Pagamentos", font=("Arial", 16)).pack(side="left", padx=10, pady=10)
    btn_add = tk.Button(top, text="+ Novo Lançamento", command=lambda: abrir_formulario_pagamento(root, conteudo))
    btn_add.pack(side="right", padx=10, pady=10)

    colunas = ("Associado", "Tipo de taxa", "Valor", "Vencimento", "Situação")
    tree = ttk.Treeview(conteudo, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.nome, p.tipo_taxa, p.valor, p.vencimento, p.situacao
        FROM pagamentos p
        JOIN associados a ON p.associado_id = a.id
    """)
    pagamentos = cursor.fetchall()
    conn.close()

    for pag in pagamentos:
        tree.insert("", "end", values=pag)

def abrir_formulario_pagamento(janela_pai, conteudo):
    def salvar_pagamento():
        associado = cb_associado.get()
        tipo_taxa = entry_tipo_taxa.get()
        valor = entry_valor.get()
        vencimento = entry_vencimento.get()
        forma_pag = cb_forma_pag.get()
        situacao = cb_situacao.get()

        if not associado or not tipo_taxa or not valor or not vencimento or not forma_pag or not situacao:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        # Buscar id do associado
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM associados WHERE nome=%s", (associado,))
        res = cursor.fetchone()
        if not res:
            messagebox.showerror("Erro", "Associado não encontrado.")
            conn.close()
            return
        associado_id = res[0]

        cursor.execute("""
            INSERT INTO pagamentos (associado_id, tipo_taxa, valor, vencimento, forma_pagamento, situacao)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (associado_id, tipo_taxa, valor, vencimento, forma_pag, situacao))
        conn.commit()
        conn.close()

        mostrar_pagamentos(conteudo, janela_pai)
        form.destroy()

    form = tk.Toplevel(janela_pai)
    form.title("Novo Pagamento")

    tk.Label(form, text="Associado:").grid(row=0, column=0, sticky="w")
    cb_associado = ttk.Combobox(form, width=30)
    cb_associado.grid(row=0, column=1)

    tk.Label(form, text="Tipo de taxa:").grid(row=1, column=0, sticky="w")
    entry_tipo_taxa = tk.Entry(form, width=30)
    entry_tipo_taxa.grid(row=1, column=1)

    tk.Label(form, text="Valor:").grid(row=2, column=0, sticky="w")
    entry_valor = tk.Entry(form, width=15)
    entry_valor.grid(row=2, column=1)

    tk.Label(form, text="Vencimento:").grid(row=3, column=0, sticky="w")
    entry_vencimento = tk.Entry(form, width=15)
    entry_vencimento.grid(row=3, column=1)

    tk.Label(form, text="Forma de pagamento:").grid(row=4, column=0, sticky="w")
    cb_forma_pag = ttk.Combobox(form, values=["boleto", "PIX", "cartão"], width=15)
    cb_forma_pag.grid(row=4, column=1)

    tk.Label(form, text="Situação:").grid(row=5, column=0, sticky="w")
    cb_situacao = ttk.Combobox(form, values=["Pago", "Pendente"], width=15)
    cb_situacao.grid(row=5, column=1)

    # Preencher lista de associados
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM associados")
    associados = [a[0] for a in cursor.fetchall()]
    conn.close()
    cb_associado['values'] = associados

    tk.Button(form, text="Salvar", command=salvar_pagamento).grid(row=6, column=1, pady=10)
