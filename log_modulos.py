import tkinter as tk
from tkinter import ttk



def adicionar_log(operacoes_logs, nome_paciente, operacao, nr_paciente, status):
    """
    Atualiza o dicionário de operações com o status de uma operação específica para um paciente.

    Esta função adiciona ou atualiza o status de uma operação (Cadastro, Leito, Solicitado) para um paciente
    específico no dicionário de logs de operações. Se o paciente ainda não estiver no dicionário,
    um novo registro é criado para ele.

    Parâmetros:
        operacoes_logs (dict): Dicionário contendo os logs das operações realizadas por paciente.
        nome_paciente (str): Nome do paciente a ser atualizado no log.
        operacao (str): Tipo de operação realizada ("Cadastro", "Leito" ou "Solicitado").

    Retorna:
        None
    """
    
    # Verifica se o paciente já possui registro no dicionário de operações
    if nome_paciente not in operacoes_logs:
        # Se não, cria um novo registro inicializando todas as operações como vazias
        operacoes_logs[nome_paciente] = {"Nr": nr_paciente, "Paciente": nome_paciente, "Cadastro do Paciente": "", "Atualização do Leito": "", "Cadastro do Módulo/Suplemento": ""}
    # Atualiza o status da operação específica para "Sucesso"
    if status == 0:
        operacoes_logs[nome_paciente][operacao] = "Sucesso"
    else:
        operacoes_logs[nome_paciente][operacao] = "Falha"

def exibir_logs(operacoes_logs):
    """
    Exibe uma janela de logs contendo o status das operações realizadas para cada paciente.

    Cria e exibe uma janela GUI com uma tabela (TreeView) que lista todos os pacientes e o status de cada
    operação realizada (Cadastro, Leito, Solicitado). Utiliza o dicionário de operações logs para preencher a tabela.

    Parâmetros:
        operacoes_logs (dict): Dicionário contendo os logs das operações realizadas por paciente.

    Retorna:
        None
    """
    # Criação da janela de logs
    log_window = tk.Toplevel()
    log_window.title("Status da Execução")
    log_window.geometry("750x400")

    # Configuração do estilo dos componentes da tabela
    style = ttk.Style(log_window)
    # Configuração do estilo dos cabeçalhos e das células da tabela, incluindo fonte, cor e borda
    style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'), foreground="blue")
    style.configure("Treeview", font=('Calibri', 10), rowheight=25)
    style.layout("Treeview.Item", [('Treeview.row', {'sticky': 'nswe'})])
    style.configure("Treeview", highlightthickness=1, bd=2)
    style.configure("Treeview.Heading", anchor=tk.CENTER)
    style.map("Treeview", background=[('selected', 'gray')])
    style.map("Treeview.Heading", background=[('active', 'lightblue')])

    # Criação e configuração da tabela (TreeView)
    tree = ttk.Treeview(log_window, columns=("Nr", "Paciente", "Cadastro do Paciente", "Atualização do Leito", "Cadastro do Módulo/Suplemento"), show="headings", style="Treeview")
    # Configuração dos cabeçalhos das colunas
    tree.heading("Nr", text="Nr", anchor=tk.CENTER)
    tree.heading("Paciente", text="Paciente", anchor=tk.CENTER)
    tree.heading("Cadastro do Paciente", text="Cadastro do Paciente", anchor=tk.CENTER)
    tree.heading("Atualização do Leito", text="Atualização do Leito", anchor=tk.CENTER)
    tree.heading("Cadastro do Módulo/Suplemento", text="Lançamento do Módulo/Suplemento", anchor=tk.CENTER)
    # Ajuste da largura das colunas
    tree.column("Nr", anchor=tk.CENTER, width=10)
    tree.column("Paciente", anchor=tk.CENTER, width=150)
    tree.column("Cadastro do Paciente", anchor=tk.CENTER, width=100)
    tree.column("Atualização do Leito", anchor=tk.CENTER, width=100)
    tree.column("Cadastro do Módulo/Suplemento", anchor=tk.CENTER, width=100)

    # Preenchimento da tabela com os dados dos logs de operações
    for nome_paciente, operacoes in operacoes_logs.items():
        tree.insert("", tk.END, values=(operacoes["Nr"], nome_paciente, operacoes["Cadastro do Paciente"], operacoes["Atualização do Leito"], operacoes["Cadastro do Módulo/Suplemento"]))

    # Adiciona uma barra de rolagem vertical à tabela
    scrollbar = ttk.Scrollbar(log_window, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill='y')

    # Exibição da tabela
    tree.pack(expand=True, fill='both')

    # Botão para fechar a janela de logs
    ok_button = tk.Button(log_window, text="OK", command=log_window.destroy)
    ok_button.pack(pady=10)

    # Mantém a janela aberta até que o usuário a feche
    log_window.mainloop()


#operacoes_logs = {
#    "John Doe": {"Cadastro do Paciente": "Sucesso", "Atualização do Leito": "Falha", "Cadastro do Módulo/Suplemento": "Sucesso"},
#    "Jane Smith": {"Cadastro do Paciente": "Falha", "Atualização do Leito": "Sucesso", "Cadastro do Módulo/Suplemento": "Falha"}
#}
#
#exibir_logs(operacoes_logs)


