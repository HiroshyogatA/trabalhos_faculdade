import tkinter as tk
from tkinter import ttk
from usuarios import listar_associados, abrir_formulario_associado
from eventos import mostrar_eventos
from pagamentos import mostrar_pagamentos
from relatorios import mostrar_relatorios

def iniciar_main():
    root = tk.Tk()
    root.title("Sistema de Gerenciamento de Eventos")
    root.geometry("1000x600")

    sidebar = tk.Frame(root, bg="#f0f0f0", width=200)
    sidebar.pack(side="left", fill="y")

    conteudo = tk.Frame(root)
    conteudo.pack(side="right", expand=True, fill="both")

    def mostrar_associados():
        for widget in conteudo.winfo_children():
            widget.destroy()

        top = tk.Frame(conteudo)
        top.pack(fill="x")
        tk.Label(top, text="Associados", font=("Arial", 16)).pack(side="left", padx=10, pady=10)
        btn_add = tk.Button(top, text="+ Novo Associado", command=lambda: abrir_formulario_associado(root, tree))
        btn_add.pack(side="right", padx=10, pady=10)

        colunas = ("Nome", "CPF", "Status", "Data de Cadastro")
        tree = ttk.Treeview(conteudo, columns=colunas, show="headings")
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        listar_associados(tree)

    def selecionar_menu(opcao):
        if opcao == "🧍 Associados":
            mostrar_associados()
        elif opcao == "📅 Eventos":
            mostrar_eventos(conteudo, root)
        elif opcao == "💰 Pagamentos":
            mostrar_pagamentos(conteudo, root)
        elif opcao == "📊 Relatórios":
            mostrar_relatorios(conteudo)
        else:
            for widget in conteudo.winfo_children():
                widget.destroy()
            tk.Label(conteudo, text="Tela em construção", font=("Arial", 16)).pack(pady=20)

    for item in ["🧍 Associados", "📅 Eventos", "💰 Pagamentos", "📊 Relatórios", "⚙️ Configurações"]:
        tk.Button(sidebar, text=item, anchor="w", command=lambda t=item: selecionar_menu(t)).pack(fill="x")

    mostrar_associados()
    root.mainloop()
