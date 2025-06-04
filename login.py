import tkinter as tk
from tkinter import messagebox
from bd import conectar_banco
import main

def iniciar_login():
    def autenticar():
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            login_window.destroy()
            main.iniciar_main()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Usuário").pack(pady=5)
    entry_usuario = tk.Entry(login_window)
    entry_usuario.pack(pady=5)

    tk.Label(login_window, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(login_window, show="*")
    entry_senha.pack(pady=5)

    tk.Button(login_window, text="Entrar", command=autenticar).pack(pady=20)

    login_window.mainloop()
