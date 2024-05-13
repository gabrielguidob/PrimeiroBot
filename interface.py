import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from bot import preparar_dados, preparar_cabecalho_cliente, main
import sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

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

        #self.define_estilo()  # Aplica os estilos definidos para a interface

        # Inicializa variáveis de instância que serão utilizadas na aplicação
        self.espera = 0  # Tempo de espera (segundos) utilizado nas operações da automação
        self.planilha_path = tk.StringVar()  # Caminho da planilha selecionada pelo usuário
        self.dados_df = None  # DataFrame que armazenará os dados da planilha escolhida

        self.mostrar_primeira_tela()  # Exibe a primeira tela da interface
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Define o método on_close para ser chamado ao fechar a janela

    #def define_estilo(self):
    #    """
    #    Define os estilos visuais para os componentes da interface gráfica, como botões e títulos,
    #    utilizando a biblioteca ttk. Configura as cores de fundo, fontes, cores de texto, entre outros.
    #    """
    #    self.configure(background="#f0f0f0")  # Cor de fundo da janela principal
#
    #    # Cria e configura os estilos para os componentes ttk
    #    style = ttk.Style(self)
    #    style.configure("TButton", font=('Helvetica', 10, 'bold'), background="#4a8ad8",
    #                    foreground="black", padding=5, relief="flat", borderwidth=1)
    #    style.map("TButton", background=[('active', '#3673b3')], foreground=[('active', 'black')])
    #    style.configure("TLabel", font=('Helvetica', 12, 'bold'), background="#f0f0f0", foreground="#4a8ad8")


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

        self.pacientes_vars = {}

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
        caminho_dados = filedialog.askopenfilename(title="Escolha a planilha de dados", filetypes=[("Excel files", "*.xlsx *.xls")])
        if caminho_dados:
            self.planilha_path.set(caminho_dados)
            try:
                # Carrega os dados e o cabeçalho
                caminho_comum = 'P:/LA VITA/TI/BotCity/Planilha de Configuração HOMOLOGAÇÃO 03.xlsx'
                self.dados_df, self.quantitativo_embalagens_df, linhas_com_problemas = preparar_dados(caminho_dados, caminho_comum)
                self.numero_cliente, self.hora_entrega, self.data_formatada, self.nome_cliente = preparar_cabecalho_cliente(caminho_dados)
                if not linhas_com_problemas.empty:
                    self.mostrar_alerta_problemas(linhas_com_problemas)
                else:
                    self.mostrar_segunda_tela()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar a planilha: {e}")

    def mostrar_alerta_problemas(self, linhas_com_problemas):
        self.limpar_tela_principal()
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True)
        label = ttk.Label(frame, text="Alerta: Pacientes com dados incompletos!")
        label.pack()

        # Montar a mensagem detalhada para cada linha problemática
        mensagem_detalhada = ""
        for idx, row in linhas_com_problemas.iterrows():
            detalhes_linha = f"Nome: {row['Paciente']}: {row.get('Nr. Atend.', 'N/A')}\n"
            mensagem_detalhada += detalhes_linha

        # Mostrar a mensagem em uma caixa de diálogo
        messagebox.showerror("Dados Incompletos", f"Pacientes com dados incompletos foram detectados. Por favor, revise a planilha. Detalhes dos pacientes afetados:\n{mensagem_detalhada}")
        self.mostrar_segunda_tela()



    def toggle_all_checkboxes(self):
        all_selected = all(var.get() for var in self.pacientes_vars.values())
        new_value = not all_selected
        for var in self.pacientes_vars.values():
            var.set(new_value)

    def mostrar_segunda_tela(self):
        self.limpar_tela_principal()

        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x', expand=True)

        # Informações do cabeçalho do cliente
        info_cliente = f"Cliente: {self.nome_cliente} -\nHora de Entrega: {self.hora_entrega} - Data do Pedido: {self.data_formatada}"
        header_label = ttk.Label(main_frame, text=info_cliente, style="TLabel")
        header_label.pack(fill='x', expand=True, pady=(0, 10))

        # Título da lista de pacientes
        label = ttk.Label(main_frame, text="Selecione os pacientes para cadastrar:", style="TLabel")
        label.pack(fill='x', expand=True)

        # Configuração do scrollable frame
        container = ttk.Frame(self)
        container.pack(fill='both', expand=True, side='top')
        canvas = tk.Canvas(container, bd=0, highlightthickness=0, background="#f0f0f0")
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        scroll_frame = ttk.Frame(canvas, style="TFrame")
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.pacientes_vars = {}
        if self.dados_df is not None:
            for index, row in self.dados_df.iterrows():
                var = tk.BooleanVar(value=True)  # Checkboxes marcados por padrão
                chk = ttk.Checkbutton(scroll_frame, text=f"{row['Paciente']} ({row['Nr. Atend.']})", variable=var, style="TCheckbutton")
                chk.pack(anchor='w')
                self.pacientes_vars[row['Paciente']] = var

        # Botões de navegação, colocados de forma que sempre fiquem visíveis
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill='x', expand=False, side='bottom')
        toggle_button = ttk.Button(button_frame, text="Selecionar Tudo", command=self.toggle_all_checkboxes, style="TButton")
        toggle_button.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.mostrar_primeira_tela, style="TButton")
        button_voltar.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        button_avancar = ttk.Button(button_frame, text="Avançar", command=self.mostrar_quarta_tela, style="TButton")
        button_avancar.pack(side='right', padx=5, pady=5, fill='x', expand=True)






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

        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.voltar_segunda_tela, style="TButton")
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

    def coletar_pacientes_selecionados(self):
        """
        Coleta os pacientes selecionados a partir das variáveis associadas aos checkboxes.
        """
        return [nome for nome, var in self.pacientes_vars.items() if var.get()]

    
    def executar_bot(self):
        """
        Este método é chamado pelo botão 'Rodar' na quarta tela da interface gráfica. Ele captura a opção de
        velocidade escolhida pelo usuário, transforma o valor em um número flutuante para uso posterior na
        execução do bot, e prepara para a execução subsequente do bot com os parâmetros definidos pelo usuário.
        """
        # Coleta os pacientes selecionados
        pacientes_selecionados = self.coletar_pacientes_selecionados()
        
        # Coleta a velocidade escolhida
        espera = float(self.velocidade.get())

        # Coleta o caminho dos dados
        caminho_dados = self.planilha_path.get()
        caminho_comum = "P:/LA VITA/TI/BotCity/Planilha de Configuração HOMOLOGAÇÃO 03.xlsx"

        # Fecha a interface gráfica
        self.destroy()

        # Chama a função main do bot.py com todos os parâmetros necessários
        main(pacientes_selecionados, espera, caminho_dados, caminho_comum)

        
        
    



        


if __name__ == "__main__":
    app = Application()
    app.mainloop()  # Executa a interface gráfica e espera até que ela seja fechada



