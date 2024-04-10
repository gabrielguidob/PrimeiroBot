import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from bot import preparar_dados, main


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Automação de Cadastro de Pacientes")

        # Inicialização das variáveis que serão usadas
        self.espera = 0  # Adicionando variável de instância para armazenar o valor de espera
        self.planilha_path = tk.StringVar()
        self.dados_df = None  # DataFrame será armazenado aqui após escolha da planilha

        # Iniciar a interface com a primeira tela
        self.mostrar_primeira_tela()

    def mostrar_primeira_tela(self):
        self.limpar_tela_principal()  # Adicione essa linha no início de cada método de tela para garantir limpeza
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, fill='x', expand=True)

        label = tk.Label(frame, text="Escolha a planilha de dados:")
        label.pack(fill='x', expand=True)

        button_escolher = tk.Button(frame, text="Escolher Planilha", command=self.escolher_planilha)
        button_escolher.pack(fill='x', expand=True)

        button_avancar = tk.Button(frame, text="Avançar", command=self.mostrar_segunda_tela)
        button_avancar.pack(fill='x', expand=True)

    # Adicione este método para limpar a tela principal corretamente antes de mudar de tela
    def limpar_tela_principal(self):
        for widget in self.winfo_children():
            widget.destroy()


    def escolher_planilha(self):
        filepath = filedialog.askopenfilename(title="Escolha a planilha de dados", filetypes=[("Excel files", "*.xlsx *.xls")])
        if filepath:  # Se um arquivo de dados foi escolhido
            self.planilha_path.set(filepath)
            print("Planilha de dados escolhida:", self.planilha_path.get())  # Para verificação

            # Caminho fixo para os dados comuns (como produtos e via de administração)
            caminho_comum = 'P:\LA VITA\TI\BotCity\Planilha de Configuração HOMOLOGAÇÃO 02.xlsx'

            try:
                # Chamada da função preparar_dados com o caminho escolhido pelo usuário para os dados e o caminho fixo para os dados comuns
                self.dados_df, self.quantitativo_embalagens_df = preparar_dados(filepath, caminho_comum)
                self.mostrar_segunda_tela()  # Avança automaticamente para a segunda tela após a leitura
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar a planilha: {e}")
                # Trata erros durante a leitura da planilha e mostra uma mensagem de erro



    def limpar_tela(self, frame):
        # Uma função utilitária para limpar a tela atual antes de mostrar a próxima
        for widget in frame.winfo_children():
            widget.destroy()
        frame.pack_forget()


    def mostrar_segunda_tela(self):
        self.limpar_tela_principal()

        # Frame principal para os componentes fixos (label e botões)
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x')

        label = tk.Label(main_frame, text="Selecione os pacientes para cadastrar:")
        label.pack(fill='x', expand=True)

        # Frame para conter o Canvas e o Scrollbar
        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bd=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame que conterá os checkboxes dentro do Canvas
        scroll_frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Variável para armazenar os CheckBoxes dos pacientes
        self.pacientes_vars = {}

        if self.dados_df is not None:
            for index, row in self.dados_df.iterrows():
                var = tk.BooleanVar()
                chk = tk.Checkbutton(scroll_frame, text=row['Nome'], variable=var)
                chk.pack(anchor='w')
                self.pacientes_vars[row['Nome']] = var

        # Frame para os botões "Voltar" e "Avançar"
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill='x')

        button_voltar = tk.Button(button_frame, text="Voltar", command=self.mostrar_primeira_tela)
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)

        button_avancar = tk.Button(button_frame, text="Avançar", command=self.avancar_para_cadastro)
        button_avancar.pack(side=tk.RIGHT, padx=5, pady=5)


    def avancar_para_cadastro(self):
        selecionados = [nome for nome, var in self.pacientes_vars.items() if var.get()]
        self.pacientes_selecionados_para_cadastro = selecionados
        print("Pacientes selecionados para cadastro:", selecionados)
        # Não chame cadastrar_pacientes aqui. Apenas armazene os selecionados.
        self.mostrar_terceira_tela()  # Prossegue para a próxima tela


    def mostrar_terceira_tela(self):
        self.limpar_tela_principal()

        # Frame principal para os componentes fixos (label e botões)
        main_frame = tk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x')

        label = tk.Label(main_frame, text="Selecione os pacientes para atualizar o leito:")
        label.pack(fill='x', expand=True)

        # Frame para conter o Canvas e o Scrollbar
        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bd=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame que conterá os checkboxes dentro do Canvas
        scroll_frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        self.pacientes_vars = {}  # Dicionário para armazenar as variáveis dos checkboxes

        if self.dados_df is not None:
            for index, row in self.dados_df.iterrows():
                var = tk.BooleanVar()
                chk = tk.Checkbutton(scroll_frame, text=row['Nome'], variable=var)
                chk.pack(anchor='w')
                self.pacientes_vars[row['Nome']] = var

        # Frame para os botões "Voltar" e "Avançar"
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill='x')

        button_voltar = tk.Button(button_frame, text="Voltar", command=self.mostrar_segunda_tela)
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)

        button_avancar = tk.Button(button_frame, text="Avançar", command=self.atualizar_leitos_selecionados)
        button_avancar.pack(side=tk.RIGHT, padx=5, pady=5)


    def atualizar_leitos_selecionados(self):
        selecionados = [nome for nome, var in self.pacientes_vars.items() if var.get()]
        self.pacientes_selecionados_para_atualizacao_leitos = selecionados
        print("Pacientes selecionados para atualizar leito:", selecionados)
        # Não chame atualizar_leitos aqui. Apenas armazene os selecionados.
        self.mostrar_quarta_tela()  # Ou finalize a interface, se for o último passo.
   

    def mostrar_quarta_tela(self):
        self.limpar_tela_principal()
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10, fill='x', expand=True)
        

        label = tk.Label(frame, text="Certifique-se de que o sistema esteja aberto, maximizado e visível.")
        label.pack()

        label_velocidade = tk.Label(frame, text="Escolha a velocidade da execução:")
        label_velocidade.pack()

        # Opções de velocidade
        opcoes_velocidade = {"Rápida": "0", "Média": "1", "Lenta": "2"}
        self.velocidade = tk.StringVar(value="0")  # Padrão é rápida
        for texto, valor in opcoes_velocidade.items():
            rb = tk.Radiobutton(frame, text=texto, variable=self.velocidade, value=valor)
            rb.pack(anchor='w')

        button_iniciar = tk.Button(frame, text="Rodar", command=self.executar_bot)
        button_iniciar.pack(side=tk.LEFT, padx=5)

        button_cancelar = tk.Button(frame, text="Cancelar", command=self.cancelar)
        button_cancelar.pack(side=tk.RIGHT, padx=5)

        # Adicionando o botão "Voltar"
        button_voltar = tk.Button(frame, text="Voltar", command=self.mostrar_terceira_tela)
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)

    def cancelar(self):
        self.destroy()  # Fecha a aplicação

    def executar_bot(self):
        # Obtenha a velocidade/espera escolhida pelo usuário
        espera = int(self.velocidade.get())
        print('A velocidade escolhida:', espera)
        # Feche a interface gráfica
        self.destroy()



        


if __name__ == "__main__":
    app = Application()
    app.mainloop()  # Executa a interface gráfica e espera até que ela seja fechada

    # Após o fechamento da interface, coleta os parâmetros necessários
    espera_escolhida = int(app.velocidade.get())
    pacientes_para_cadastro = app.pacientes_selecionados_para_cadastro if hasattr(app, 'pacientes_selecionados_para_cadastro') else []
    pacientes_para_atualizacao_leito = app.pacientes_selecionados_para_atualizacao_leitos if hasattr(app, 'pacientes_selecionados_para_atualizacao_leitos') else []

    # Supondo que os caminhos dos arquivos sejam definidos na interface ou sejam fixos, defina-os aqui:
    caminho_dados = app.planilha_path.get()  # Ou o caminho fixo, se aplicável
    caminho_comum = 'P:\LA VITA\TI\BotCity\Planilha de Configuração HOMOLOGAÇÃO 02.xlsx'

    # Faz a chamada para a função main com os parâmetros coletados
    main(pacientes_para_cadastro, pacientes_para_atualizacao_leito, espera_escolhida, caminho_dados, caminho_comum)

