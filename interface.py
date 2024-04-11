import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from bot import preparar_dados, main
import sys

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Automação de Cadastro de Pacientes")

        self.define_estilo()  # Define o estilo dos componentes

        # Inicialização das variáveis que serão usadas
        self.espera = 0  # Adicionando variável de instância para armazenar o valor de espera
        self.planilha_path = tk.StringVar()
        self.dados_df = None  # DataFrame será armazenado aqui após escolha da planilha

        # Iniciar a interface com a primeira tela
        self.mostrar_primeira_tela()
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Chama on_close quando a janela é fechada


    def define_estilo(self):
        # Define o estilo geral da janela
        self.configure(background="#f0f0f0")

        # Cria e configura estilos para botões e títulos
        style = ttk.Style(self)
        
        # Estilo para botões
        style.configure("TButton", font=('Helvetica', 10, 'bold'), background="#4a8ad8", foreground="black", padding=5, relief="flat", borderwidth=1)
        style.map("TButton", background=[('active', '#3673b3')], foreground=[('active', 'black')])

        # Estilo para títulos
        style.configure("TLabel", font=('Helvetica', 12, 'bold'), background="#f0f0f0", foreground="#4a8ad8")

    def mostrar_primeira_tela(self):
        self.limpar_tela_principal()  # Adicione essa linha no início de cada método de tela para garantir limpeza
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill='x', expand=True)

        label = ttk.Label(frame, text="Escolha a planilha de dados:", style="TLabel")
        label.pack(fill='x', expand=True)

        button_escolher = ttk.Button(frame, text="Escolher Planilha", command=self.escolher_planilha, style="TButton")
        button_escolher.pack(fill='x', expand=True)

        #button_avancar = ttk.Button(frame, text="Avançar", command=self.mostrar_segunda_tela, style="TButton")
        #button_avancar.pack(fill='x', expand=True)

    # Adicione este método para limpar a tela principal corretamente antes de mudar de tela
    def limpar_tela_principal(self):
        for widget in self.winfo_children():
            widget.destroy()


    def escolher_planilha(self):
        filepath = filedialog.askopenfilename(title="Escolha a planilha de dados", filetypes=[("Excel files", "*.xlsx *.xls")])
        if filepath:  # Se um arquivo de dados foi escolhido
            self.planilha_path.set(filepath)
            #print("Planilha de dados escolhida:", self.planilha_path.get())  # Para verificação

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
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x')

        label = ttk.Label(main_frame, text="Selecione os pacientes para cadastrar:", style="TLabel")
        label.pack(fill='x', expand=True)

        # Frame para conter o Canvas e o Scrollbar
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bd=0, highlightthickness=0, background="#f0f0f0")
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame que conterá os checkboxes dentro do Canvas
        scroll_frame = ttk.Frame(canvas, style="TFrame")
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
                chk = ttk.Checkbutton(scroll_frame, text=row['Nome'], variable=var, style="TCheckbutton")
                chk.pack(anchor='w')
                self.pacientes_vars[row['Nome']] = var

        # Frame para os botões "Voltar" e "Avançar"
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill='x')

        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.mostrar_primeira_tela, style="TButton")
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)

        button_avancar = ttk.Button(button_frame, text="Avançar", command=self.avancar_para_cadastro, style="TButton")
        button_avancar.pack(side=tk.RIGHT, padx=5, pady=5)



    def avancar_para_cadastro(self):
        selecionados = [nome for nome, var in self.pacientes_vars.items() if var.get()]
        self.pacientes_selecionados_para_cadastro = selecionados
        print("Pacientes selecionados para cadastro:", selecionados)
        # Não chame cadastrar_pacientes aqui. Apenas armazene os selecionados.
        self.mostrar_terceira_tela()  # Prossegue para a próxima tela


    def voltar_segunda_tela(self):
        # Zera as variáveis necessárias
        self.pacientes_vars = {}
        # Volta para a segunda tela
        self.mostrar_segunda_tela()

    def voltar_terceira_tela(self):
        # Zera as variáveis necessárias
        self.pacientes_vars = {}
        # Volta para a segunda tela
        self.mostrar_terceira_tela()



    def mostrar_terceira_tela(self):
        self.limpar_tela_principal()

        # Frame principal para os componentes fixos (label e botões)
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x')

        label = ttk.Label(main_frame, text="Selecione os pacientes para atualizar o leito:", style="TLabel")
        label.pack(fill='x', expand=True)

        # Frame para conter o Canvas e o Scrollbar
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bd=0, highlightthickness=0, background="#f0f0f0")
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame que conterá os checkboxes dentro do Canvas
        scroll_frame = ttk.Frame(canvas, style="TFrame")
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
                chk = ttk.Checkbutton(scroll_frame, text=row['Nome'], variable=var, style="TCheckbutton")
                chk.pack(anchor='w')
                self.pacientes_vars[row['Nome']] = var

        # Frame para os botões "Voltar" e "Avançar"
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill='x')

        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.voltar_segunda_tela, style="TButton")
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)

        button_avancar = ttk.Button(button_frame, text="Avançar", command=self.atualizar_leitos_selecionados, style="TButton")
        button_avancar.pack(side=tk.RIGHT, padx=5, pady=5)



    def atualizar_leitos_selecionados(self):
        selecionados = [nome for nome, var in self.pacientes_vars.items() if var.get()]
        self.pacientes_selecionados_para_atualizacao_leitos = selecionados
        print("Pacientes selecionados para atualizar leito:", selecionados)
        # Não chame atualizar_leitos aqui. Apenas armazene os selecionados.
        self.mostrar_quarta_tela()  
   


    def mostrar_quarta_tela(self):
        self.limpar_tela_principal()

        # Frame para o texto de instrução e escolha de velocidade
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x', expand=True)

        # Instruções para o usuário
        label = ttk.Label(main_frame, text="Certifique-se de que o sistema esteja aberto, maximizado e visível.", style="TLabel")
        label.pack(pady=(0, 20))

        # Escolha de velocidade
        label_velocidade = ttk.Label(main_frame, text="Escolha a velocidade da execução:", style="TLabel")
        label_velocidade.pack()

        opcoes_velocidade = {"Rápida": "0", "Média": "0.5", "Lenta": "1"}
        self.velocidade = tk.StringVar(value="0")  # Padrão é rápida
        for texto, valor in opcoes_velocidade.items():
            rb = ttk.Radiobutton(main_frame, text=texto, variable=self.velocidade, value=valor, style="TRadiobutton")
            rb.pack(anchor='w')

        # Botões para iniciar ou cancelar
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=20, fill='x')

        button_iniciar = ttk.Button(button_frame, text="Rodar", command=self.executar_bot, style="TButton")
        button_iniciar.pack(side=tk.LEFT, padx=5)

        button_cancelar = ttk.Button(button_frame, text="Cancelar", command=self.cancelar, style="TButton")
        button_cancelar.pack(side=tk.RIGHT, padx=5)

        # Botão "Voltar"
        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.voltar_terceira_tela, style="TButton")
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)


    def cancelar(self):
         # Este método é chamado pelo botão Cancelar
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.destroy()  # Destruir a janela
            sys.exit()  # Encerra o programa

    def on_close(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.destroy()  # Destruir a janela
            sys.exit()  # Encerra o programa

    def executar_bot(self):
        # Obtenha a velocidade/espera escolhida pelo usuário
        espera = float(self.velocidade.get())
        print('A velocidade escolhida:', espera)
        # Feche a interface gráfica
        self.destroy()



        


if __name__ == "__main__":
    app = Application()
    app.mainloop()  # Executa a interface gráfica e espera até que ela seja fechada

    # Após o fechamento da interface, coleta os parâmetros necessários
    espera_escolhida = float(app.velocidade.get())
    pacientes_para_cadastro = app.pacientes_selecionados_para_cadastro if hasattr(app, 'pacientes_selecionados_para_cadastro') else []
    pacientes_para_atualizacao_leito = app.pacientes_selecionados_para_atualizacao_leitos if hasattr(app, 'pacientes_selecionados_para_atualizacao_leitos') else []

    # Supondo que os caminhos dos arquivos sejam definidos na interface ou sejam fixos, defina-os aqui:
    caminho_dados = app.planilha_path.get()  # Ou o caminho fixo, se aplicável
    caminho_comum = 'P:\LA VITA\TI\BotCity\Planilha de Configuração HOMOLOGAÇÃO 02.xlsx'

    # Faz a chamada para a função main com os parâmetros coletados
    main(pacientes_para_cadastro, pacientes_para_atualizacao_leito, espera_escolhida, caminho_dados, caminho_comum)

