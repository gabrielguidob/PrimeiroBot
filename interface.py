import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from bot import preparar_dados, main
import sys

class Application(tk.Tk):
    def __init__(self):
        """
        Inicializa a aplicação, definindo tamanho e título da janela principal, estilos dos componentes,
        inicializando variáveis e configurando a primeira tela a ser exibida. Também define o comportamento
        ao fechar a janela principal para garantir uma saída segura da aplicação.

        Parâmetros:
            Não possui parâmetros.
        """
        super().__init__()
        self.geometry("600x400")  # Define o tamanho da janela
        self.title("Automação de Cadastro de Prescrição")  # Define o título da janela

        self.define_estilo()  # Aplica os estilos definidos para a interface

        # Inicializa variáveis de instância que serão utilizadas na aplicação
        self.espera = 0  # Tempo de espera (segundos) utilizado nas operações da automação
        self.planilha_path = tk.StringVar()  # Caminho da planilha selecionada pelo usuário
        self.dados_df = None  # DataFrame que armazenará os dados da planilha escolhida

        self.mostrar_primeira_tela()  # Exibe a primeira tela da interface
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Define o método on_close para ser chamado ao fechar a janela

    def define_estilo(self):
        """
        Define os estilos visuais para os componentes da interface gráfica, como botões e títulos,
        utilizando a biblioteca ttk. Configura as cores de fundo, fontes, cores de texto, entre outros.
        """
        self.configure(background="#f0f0f0")  # Cor de fundo da janela principal

        # Cria e configura os estilos para os componentes ttk
        style = ttk.Style(self)
        style.configure("TButton", font=('Helvetica', 10, 'bold'), background="#4a8ad8",
                        foreground="black", padding=5, relief="flat", borderwidth=1)
        style.map("TButton", background=[('active', '#3673b3')], foreground=[('active', 'black')])
        style.configure("TLabel", font=('Helvetica', 12, 'bold'), background="#f0f0f0", foreground="#4a8ad8")


    def mostrar_primeira_tela(self):
        """
        Configura e exibe a primeira tela da interface. Esta tela permite ao usuário escolher uma planilha de dados
        para processamento. A tela inclui um rótulo informativo e um botão para selecionar a planilha.

        Parâmetros:
            Não possui parâmetros.
        """
        self.limpar_tela_principal()  # Limpa a tela principal para garantir que a interface esteja limpa antes de adicionar novos elementos
        frame = ttk.Frame(self)  # Cria um frame como contêiner para os elementos desta tela
        frame.pack(padx=10, pady=10, fill='x', expand=True)  # Posiciona o frame na janela

        # Cria e configura um rótulo informativo
        label = ttk.Label(frame, text="Escolha a planilha de dados:", style="TLabel")
        label.pack(fill='x', expand=True)  # Posiciona o rótulo no frame

        # Cria e configura um botão que permite ao usuário escolher a planilha
        button_escolher = ttk.Button(frame, text="Escolher Planilha", command=self.escolher_planilha, style="TButton")
        button_escolher.pack(fill='x', expand=True)  # Posiciona o botão no frame

    def limpar_tela_principal(self):
        """
        Limpa todos os widgets presentes na tela principal da aplicação. Este método é chamado antes de
        configurar uma nova tela para garantir que a tela anterior seja completamente removida.

        Parâmetros:
            Não possui parâmetros.
        """
        for widget in self.winfo_children():
            widget.destroy()  # Destroi cada widget filho da janela principal, limpando a tela



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


    def mostrar_segunda_tela(self):
        """
        Prepara e exibe a segunda tela da aplicação. Esta tela permite ao usuário selecionar pacientes para cadastro
        a partir de uma lista dinâmica, gerada com base nos dados da planilha escolhida. Inclui um mecanismo de
        rolagem para acomodar listas longas de pacientes.

        Parâmetros:
            Não possui parâmetros.
        """
        self.limpar_tela_principal()  # Limpa a tela principal para preparar para novos elementos

        # Configura o frame principal que contém os elementos estáticos da tela, como rótulos e botões
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x')

        # Rótulo informativo para o usuário
        label = ttk.Label(main_frame, text="Selecione os pacientes para cadastrar:", style="TLabel")
        label.pack(fill='x', expand=True)

        # Configura container para a lista de pacientes com scrollbar
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bd=0, highlightthickness=0, background="#f0f0f0")
        canvas.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame para os checkboxes de seleção de pacientes, dentro do canvas
        scroll_frame = ttk.Frame(canvas, style="TFrame")
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Popula a lista de pacientes com checkboxes
        self.pacientes_vars = {}  # Reinicia o dicionário para armazenar as variáveis dos checkboxes
        if self.dados_df is not None:
            for index, row in self.dados_df.iterrows():
                var = tk.BooleanVar()
                chk = ttk.Checkbutton(scroll_frame, text=row['Nome'], variable=var, style="TCheckbutton")
                chk.pack(anchor='w')
                self.pacientes_vars[row['Nome']] = var

        # Configura os botões "Voltar" e "Avançar"
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill='x')
        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.mostrar_primeira_tela, style="TButton")
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)
        button_avancar = ttk.Button(button_frame, text="Avançar", command=self.avancar_para_cadastro, style="TButton")
        button_avancar.pack(side=tk.RIGHT, padx=5, pady=5)


    def avancar_para_cadastro(self):
        """
        Avança para a tela de cadastro após a seleção dos pacientes. Coleta os pacientes selecionados pelos
        checkboxes e armazena as seleções para uso posterior na aplicação. Em seguida, procede para a próxima
        tela, onde serão realizadas as ações de cadastro ou atualização de leitos.

        Parâmetros:
            Não possui parâmetros.
        """
        selecionados = [nome for nome, var in self.pacientes_vars.items() if var.get()]
        self.pacientes_selecionados_para_cadastro = selecionados
        print("Pacientes selecionados para cadastro:", selecionados)
        self.mostrar_terceira_tela()  # Transição para a próxima tela de interface

    def voltar_segunda_tela(self):
        """
        Função para retornar à segunda tela do aplicativo. É chamada quando o usuário deseja voltar para a tela
        anterior a partir da terceira tela. Antes de retornar, zera a variável que armazena as seleções dos
        pacientes, garantindo que as escolhas anteriores sejam descartadas.

        Parâmetros:
            Não possui parâmetros.
        """
        self.pacientes_vars = {}  # Zera as seleções feitas anteriormente
        self.mostrar_segunda_tela()  # Retorna para a tela anterior

    def voltar_terceira_tela(self):
        """
        Retorna à terceira tela da aplicação. Esta função é chamada para desfazer a ação de avançar para a quarta
        tela, permitindo que o usuário revise ou altere as seleções de pacientes para atualização de leito antes
        de prosseguir. Antes de retornar, zera a variável que armazena as seleções dos pacientes.

        Parâmetros:
            Não possui parâmetros.
        """
        self.pacientes_vars = {}  # Zera as seleções feitas na terceira tela
        self.mostrar_terceira_tela()  # Retorna para a terceira tela


    def mostrar_terceira_tela(self):
        """
        Exibe a terceira tela da interface gráfica, permitindo que o usuário selecione os pacientes para atualizar
        o leito. A tela é composta por uma lista de checkboxes, cada um correspondendo a um paciente disponível
        na planilha carregada. O usuário pode selecionar um ou mais pacientes e, em seguida, proceder para
        atualizar os leitos ou voltar à tela anterior para realizar outras seleções.

        Esta tela utiliza um canvas com uma barra de rolagem para acomodar um grande número de pacientes,
        garantindo que a interface permaneça usável mesmo com muitos registros.
        """
        self.limpar_tela_principal()

        # Criação do frame principal e título da tela.
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x')
        label = ttk.Label(main_frame, text="Selecione os pacientes para atualizar o leito:", style="TLabel")
        label.pack(fill='x', expand=True)

        # Configuração do container para os checkboxes com barra de rolagem.
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True)
        canvas = tk.Canvas(container, bd=0, highlightthickness=0, background="#f0f0f0")
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        # Criação do frame interno para alocar os checkboxes dentro do canvas.
        scroll_frame = ttk.Frame(canvas, style="TFrame")
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Inicialização dos checkboxes para seleção dos pacientes.
        self.pacientes_vars = {}
        if self.dados_df is not None:
            for index, row in self.dados_df.iterrows():
                var = tk.BooleanVar()
                chk = ttk.Checkbutton(scroll_frame, text=row['Nome'], variable=var, style="TCheckbutton")
                chk.pack(anchor='w')
                self.pacientes_vars[row['Nome']] = var

        # Botões para navegação entre as telas.
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill='x')
        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.voltar_segunda_tela, style="TButton")
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)
        button_avancar = ttk.Button(button_frame, text="Avançar", command=self.atualizar_leitos_selecionados, style="TButton")
        button_avancar.pack(side=tk.RIGHT, padx=5, pady=5)




    def atualizar_leitos_selecionados(self):
        """
        Coleta os pacientes selecionados na terceira tela para atualização de leito e avança para a quarta tela.
        Esta função é acionada quando o usuário clica no botão 'Avançar' na terceira tela. Ela compila uma lista
        dos pacientes que foram selecionados para terem seus leitos atualizados. Esta lista é armazenada na variável
        de instância self.pacientes_selecionados_para_atualizacao_leitos para uso posterior. Após a coleta dos
        pacientes selecionados, a função direciona o usuário para a quarta tela, onde podem ser tomadas mais ações
        ou iniciada a execução das operações de atualização no sistema.

        Nota: A atualização de leitos em si não é realizada nesta função; este passo apenas coleta e armazena
        os pacientes selecionados e prepara a interface para o próximo passo.
        """
        selecionados = [nome for nome, var in self.pacientes_vars.items() if var.get()]
        self.pacientes_selecionados_para_atualizacao_leitos = selecionados
        print("Pacientes selecionados para atualizar leito:", selecionados)
        self.mostrar_quarta_tela()  # Avança para a próxima tela após a seleção.

   


    def mostrar_quarta_tela(self):
        """
        Mostra a quarta tela da interface gráfica, onde o usuário pode finalizar a preparação para a execução
        do bot. Esta tela inclui instruções finais, opções para a velocidade de execução do bot, e botões
        para iniciar a automação, cancelar ou voltar à tela anterior.

        Instruções detalhadas são fornecidas para garantir que o sistema de destino esteja pronto para a automação,
        incluindo estar aberto, maximizado e visível na tela. O usuário também pode escolher a velocidade da
        execução, com opções que variam de 'Rápida' a 'Lenta'. Essas escolhas são feitas por meio de botões
        de rádio, com 'Rápida' sendo a opção padrão.

        Além disso, a tela apresenta botões para 'Rodar' a automação com as configurações escolhidas, 'Cancelar'
        a operação e fechar a interface, ou 'Voltar' à tela anterior para possíveis ajustes nas seleções feitas.
        """

        self.limpar_tela_principal()

        # Criação e configuração do frame principal para texto de instrução e escolha de velocidade
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x', expand=True)

        # Adiciona instruções para o usuário
        label = ttk.Label(main_frame, text="Certifique-se de que o sistema esteja aberto, maximizado e visível.", style="TLabel")
        label.pack(pady=(0, 20))

        # Adiciona opção para escolha da velocidade de execução
        label_velocidade = ttk.Label(main_frame, text="Escolha a velocidade da execução:", style="TLabel")
        label_velocidade.pack()

        opcoes_velocidade = {"Rápida": "0", "Média": "0.5", "Lenta": "1"}
        self.velocidade = tk.StringVar(value="0")  # Define o padrão como rápido
        for texto, valor in opcoes_velocidade.items():
            rb = ttk.Radiobutton(main_frame, text=texto, variable=self.velocidade, value=valor, style="TRadiobutton")
            rb.pack(anchor='w')

        # Criação e configuração do frame para botões de ação
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=20, fill='x')

        # Adiciona botões para iniciar, cancelar ou voltar
        button_iniciar = ttk.Button(button_frame, text="Rodar", command=self.executar_bot, style="TButton")
        button_iniciar.pack(side=tk.RIGHT, padx=5)

        button_cancelar = ttk.Button(button_frame, text="Cancelar", command=self.cancelar, style="TButton")
        button_cancelar.pack(side=tk.RIGHT, padx=5)

        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.voltar_terceira_tela, style="TButton")
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)



    def cancelar(self):
        """
        Método invocado pelo botão 'Cancelar'. Este método exibe uma caixa de diálogo perguntando ao usuário se
        ele realmente deseja sair da aplicação. Se o usuário escolher 'OK', a aplicação será encerrada; caso
        contrário, a aplicação continua em execução.
        """
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.destroy()  # Fecha a janela da interface gráfica
            sys.exit()  # Encerra a execução do programa
    
    def on_close(self):
        """
        Método chamado quando a janela da aplicação é fechada pelo usuário, seja clicando no botão de fechar
        da janela ('X') ou através de outro método de fechamento. Similar ao método 'cancelar', este método
        exibe uma caixa de diálogo perguntando ao usuário se ele deseja realmente sair. Caso afirmativo, a
        aplicação é encerrada; caso contrário, nada acontece e a aplicação continua em execução.
        """
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.destroy()  # Fecha a janela da interface gráfica
            sys.exit()  # Encerra a execução do programa
    
    def executar_bot(self):
        """
        Este método é chamado pelo botão 'Rodar' na quarta tela da interface gráfica. Ele captura a opção de
        velocidade escolhida pelo usuário, transforma o valor em um número flutuante para uso posterior na
        execução do bot, e exibe esse valor no console para verificação. Após capturar a escolha de velocidade,
        a interface gráfica é fechada, preparando para a execução subsequente do bot com os parâmetros definidos
        pelo usuário.
        """
        espera = float(self.velocidade.get())  # Converte a escolha de velocidade para float
        print('A velocidade escolhida:', espera)  # Exibe a velocidade escolhida no console
        self.destroy()  # Fecha a interface gráfica
    



        


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

