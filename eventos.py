import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from bd import conectar_banco
from usuarios import listar_associados

def mostrar_eventos(conteudo, root):
    for widget in conteudo.winfo_children():
        widget.destroy()

    top = tk.Frame(conteudo)
    top.pack(fill="x")
    tk.Label(top, text="Eventos", font=("Arial", 16)).pack(side="left", padx=10, pady=10)
    btn_add = tk.Button(top, text="+ Novo Evento", command=lambda: abrir_formulario_evento(root, conteudo))
    btn_add.pack(side="right", padx=10, pady=10)

    colunas = ("Nome do evento", "Data", "Local")
    tree = ttk.Treeview(conteudo, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=200)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, data_hora, local FROM eventos")
    eventos = cursor.fetchall()
    conn.close()

    for evento in eventos:
        data_evento = evento[1]
        if data_evento is None:
            data_formatada = "Data não disponível"
        elif isinstance(data_evento, str):
            try:
                # Tenta converter string para datetime
                data_evento_dt = datetime.fromisoformat(data_evento)
                data_formatada = data_evento_dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                data_formatada = data_evento  # Deixa como está, pode ser um formato diferente
        else:
            data_formatada = data_evento.strftime("%Y-%m-%d %H:%M")

        tree.insert("", "end", values=(evento[0], data_formatada, evento[2]))


def abrir_formulario_evento(janela_pai, conteudo):
    def salvar_evento():
        nome = entry_nome.get()
        descricao = text_descricao.get("1.0", "end").strip()
        data_hora_str = entry_data_hora.get()
        local = entry_local.get()

        if not nome or not data_hora_str:
            messagebox.showwarning("Aviso", "Nome e Data/Hora são obrigatórios.")
            return

        try:
            # Espera data no formato 'YYYY-MM-DD HH:MM' ou 'YYYY-MM-DDTHH:MM'
            data_hora = datetime.fromisoformat(data_hora_str)
        except ValueError:
            messagebox.showerror("Erro", "Data/Hora inválida. Use o formato: YYYY-MM-DD HH:MM")
            return

        conn = conectar_banco()
        cursor = conn.cursor()
        # Salva como string no formato ISO para o banco
        cursor.execute("INSERT INTO eventos (nome, descricao, data_hora, local) VALUES (%s,%s,%s,%s)",
                       (nome, descricao, data_hora.isoformat(sep=' '), local))
        conn.commit()
        conn.close()

        mostrar_eventos(conteudo, janela_pai)
        form.destroy()

    form = tk.Toplevel(janela_pai)
    form.title("Novo Evento")

    tk.Label(form, text="Nome do evento:").grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(form, width=40)
    entry_nome.grid(row=0, column=1)

    tk.Label(form, text="Descrição:").grid(row=1, column=0, sticky="nw")
    text_descricao = tk.Text(form, width=30, height=4)
    text_descricao.grid(row=1, column=1)

    tk.Label(form, text="Data e hora:").grid(row=2, column=0, sticky="w")
    entry_data_hora = tk.Entry(form, width=25)
    entry_data_hora.grid(row=2, column=1)

    tk.Label(form, text="Local:").grid(row=3, column=0, sticky="w")
    entry_local = tk.Entry(form, width=30)
    entry_local.grid(row=3, column=1)

    tk.Button(form, text="Salvar", command=salvar_evento).grid(row=4, column=1, pady=10)
