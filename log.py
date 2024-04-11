import tkinter as tk
from tkinter import ttk


# Quando realizar uma operação, atualize o dicionário
def adicionar_log(operacoes_logs, nome_paciente, operacao):
    if nome_paciente not in operacoes_logs:
        operacoes_logs[nome_paciente] = {"Nome": nome_paciente, "Cadastro": "", "Leito": "", "Solicitado": ""}
    operacoes_logs[nome_paciente][operacao] = "Sucesso"

def exibir_logs(operacoes_logs):
    log_window = tk.Tk()
    log_window.title("Logs de Operações")
    log_window.geometry("600x400")

    # Define as colunas
    colunas = ("Nome", "Cadastro", "Leito", "Solicitado")

    # Configurando o estilo
    style = ttk.Style(log_window)
    style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'), foreground="blue")
    style.configure("Treeview", font=('Calibri', 10), rowheight=25)
    # Centraliza o texto nas colunas e adiciona borda
    style.layout("Treeview.Item", [('Treeview.row', {'sticky': 'nswe'})])  # Permite a borda cobrir toda a linha
    style.configure("Treeview", highlightthickness=1, bd=2, font=('Calibri', 10))  # Ajuste conforme necessário
    style.configure("Treeview.Heading", anchor=tk.CENTER)
    style.map("Treeview", background=[('selected', 'gray')])  # Cor quando selecionado
    style.map("Treeview.Heading", background=[('active', 'lightblue')])  # Cor do cabeçalho ao passar o mouse

    tree = ttk.Treeview(log_window, columns=colunas, show="headings", style="Treeview")
    tree.heading("Nome", text="Nome", anchor=tk.CENTER)
    tree.heading("Cadastro", text="Cadastro", anchor=tk.CENTER)
    tree.heading("Leito", text="Leito", anchor=tk.CENTER)
    tree.heading("Solicitado", text="Solicitado", anchor=tk.CENTER)

    # Ajusta a largura das colunas
    tree.column("Nome", anchor=tk.CENTER, width=150)
    tree.column("Cadastro", anchor=tk.CENTER, width=100)
    tree.column("Leito", anchor=tk.CENTER, width=100)
    tree.column("Solicitado", anchor=tk.CENTER, width=100)

    # Adiciona os dados ao Treeview
    for nome_paciente, operacoes in operacoes_logs.items():
        tree.insert("", tk.END, values=(nome_paciente, operacoes["Cadastro"], operacoes["Leito"], operacoes["Solicitado"]))


    # Adiciona uma barra de rolagem
    scrollbar = ttk.Scrollbar(log_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree.pack(expand=True, fill='both')

    # Botão OK para fechar a janela
    ok_button = tk.Button(log_window, text="OK", command=log_window.destroy)
    ok_button.pack(pady=10)

    log_window.mainloop()



