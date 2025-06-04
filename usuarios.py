import tkinter as tk
from tkinter import ttk, messagebox
from bd import conectar_banco
from datetime import date

def listar_associados(tree):
    for row in tree.get_children():
        tree.delete(row)

    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf, status, data_cadastro FROM associados")
    associados = cursor.fetchall()
    conn.close()

    for associado in associados:
        tree.insert("", "end", values=associado)

def abrir_formulario_associado(janela_pai, tree, associado_id=None):
    def salvar():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        data_nasc = entry_data_nasc.get()
        endereco = text_endereco.get("1.0", "end").strip()
        email = entry_email.get()
        telefone = entry_telefone.get()
        status = var_status.get()
        data_cadastro = date.today().strftime("%Y-%m-%d")

        if not nome or not cpf or not status:
            messagebox.showwarning("Aviso", "Nome, CPF e Status são obrigatórios.")
            return

        conn = conectar_banco()
        cursor = conn.cursor()
        if associado_id:  # Editar
            cursor.execute("""
                UPDATE associados SET nome=%s, cpf=%s, data_nascimento=%s,
                endereco=%s, email=%s, telefone=%s, status=%s WHERE id=%s
            """, (nome, cpf, data_nasc, endereco, email, telefone, status, associado_id))
        else:  # Novo
            cursor.execute("""
                INSERT INTO associados (nome, cpf, data_nascimento, endereco, email, telefone, status, data_cadastro)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (nome, cpf, data_nasc, endereco, email, telefone, status, data_cadastro))
        conn.commit()
        conn.close()

        listar_associados(tree)
        form.destroy()

    form = tk.Toplevel(janela_pai)
    form.title("Associado")

    tk.Label(form, text="Nome completo:").grid(row=0, column=0, sticky="w")
    entry_nome = tk.Entry(form, width=40)
    entry_nome.grid(row=0, column=1)

    tk.Label(form, text="Documento (CPF/CNPJ):").grid(row=1, column=0, sticky="w")
    entry_cpf = tk.Entry(form, width=20)
    entry_cpf.grid(row=1, column=1)

    tk.Label(form, text="Data de nascimento :").grid(row=2, column=0, sticky="w")
    entry_data_nasc = tk.Entry(form, width=15)
    entry_data_nasc.grid(row=2, column=1)

    tk.Label(form, text="Endereço:").grid(row=3, column=0, sticky="nw")
    text_endereco = tk.Text(form, width=30, height=3)
    text_endereco.grid(row=3, column=1)

    tk.Label(form, text="E-mail:").grid(row=4, column=0, sticky="w")
    entry_email = tk.Entry(form, width=30)
    entry_email.grid(row=4, column=1)

    tk.Label(form, text="Telefone:").grid(row=5, column=0, sticky="w")
    entry_telefone = tk.Entry(form, width=20)
    entry_telefone.grid(row=5, column=1)

    tk.Label(form, text="Status:").grid(row=6, column=0, sticky="w")
    var_status = tk.StringVar(value="ativo")
    tk.Radiobutton(form, text="Ativo", variable=var_status, value="ativo").grid(row=6, column=1, sticky="w")
    tk.Radiobutton(form, text="Inativo", variable=var_status, value="inativo").grid(row=6, column=1, sticky="e")

    if associado_id:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, cpf, data_nascimento, endereco, email, telefone, status FROM associados WHERE id=%s", (associado_id,))
        associado = cursor.fetchone()
        conn.close()
        if associado:
            entry_nome.insert(0, associado[0])
            entry_cpf.insert(0, associado[1])
            entry_data_nasc.insert(0, associado[2])
            text_endereco.insert("1.0", associado[3])
            entry_email.insert(0, associado[4])
            entry_telefone.insert(0, associado[5])
            var_status.set(associado[6])

    tk.Button(form, text="Salvar", command=salvar).grid(row=7, column=1, pady=10)
