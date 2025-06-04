import tkinter as tk
from bd import conectar_banco

def mostrar_relatorios(conteudo):
    for widget in conteudo.winfo_children():
        widget.destroy()

    tk.Label(conteudo, text="Relatórios (básico)", font=("Arial", 16)).pack(pady=20)

    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM associados WHERE status='ativo'")
    ativos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM associados WHERE status='inativo'")
    inativos = cursor.fetchone()[0]

    tk.Label(conteudo, text=f"Associados Ativos: {ativos}").pack()
    tk.Label(conteudo, text=f"Associados Inativos: {inativos}").pack()

    cursor.execute("SELECT COUNT(*) FROM eventos")
    eventos = cursor.fetchone()[0]
    tk.Label(conteudo, text=f"Total de Eventos: {eventos}").pack()

    cursor.execute("SELECT COUNT(*) FROM pagamentos WHERE situacao='Pendente'")
    pendentes = cursor.fetchone()[0]
    tk.Label(conteudo, text=f"Pagamentos Pendentes: {pendentes}").pack()

    conn.close()
