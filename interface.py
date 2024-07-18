import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from bot import preparar_dados, preparar_cabecalho_cliente, main
from preparar_modulos import preparar_dados_modulos
import sys
import pyautogui
import alerta_problemas
import threading
from datetime import datetime
import re
import warnings
import pandas as pd
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Automação de Cadastro de Prescrição")

        self.espera = 0
        self.planilha_path = tk.StringVar()
        self.dados_df = None
        self.hospitais = []
        self.tipo_automacao = tk.StringVar()
        self.mostrar_primeira_tela()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def verificar_resolucao(self):
        largura, altura = pyautogui.size()
        if largura != 1366 or altura != 768:
            messagebox.showerror("Resolução Incompatível", "Por favor, ajuste a resolução do seu monitor para 1366x768 antes de continuar.")
            self.destroy()

    def mostrar_primeira_tela(self):
        self.limpar_tela_principal()
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill='x', expand=True)

        self.pacientes_vars = {}

        label = ttk.Label(frame, text="Escolha a planilha de dados DIETA:", style="TLabel")
        label.pack(fill='x', expand=True)

        button_escolher_prescricao = ttk.Button(frame, text="Escolher Planilha", command=self.escolher_planilha_dieta, style="TButton")
        button_escolher_prescricao.pack(fill='x', expand=True)

        label = ttk.Label(frame, text="", style="TLabel")
        label.pack(fill='x', pady=20, expand=True)

        label = ttk.Label(frame, text="Escolha a planilha de dados MÓDULOS/SUPLEMENTOS:", style="TLabel")
        label.pack(fill='x', expand=True)

        button_escolher_modulos = ttk.Button(frame, text="Escolher Planilha", command=self.escolher_planilha_modulos, style="TButton")
        button_escolher_modulos.pack(fill='x', expand=True)

    def limpar_tela_principal(self):
        for widget in self.winfo_children():
            widget.destroy()

    def escolher_planilha_dieta(self):
        caminho_dados = filedialog.askopenfilename(title="Escolha a planilha de dados DIETA", filetypes=[("Excel files", "*.xlsx *.xls")])
        if caminho_dados:
            self.planilha_path.set(caminho_dados)
            self.tipo_automacao.set("dieta")
            try:
                caminho_comum = 'P:/LA VITA/TI/OptiVita/Bots/01-Lançamento Prescrição/Planilha de Configuração.xlsx'
                self.carregar_hospitais(caminho_comum)
                self.dados_df, self.quantitativo_embalagens_df, linhas_com_problemas = preparar_dados(caminho_dados, caminho_comum)
                self.numero_cliente, self.hora_entrega, self.data_formatada, self.nome_cliente = preparar_cabecalho_cliente(caminho_dados)
                if not linhas_com_problemas.empty:
                    self.mostrar_segunda_tela()
                    alerta_problemas.mostrar_alerta_problemas(linhas_com_problemas)
                else:
                    self.mostrar_segunda_tela()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar a planilha: {e}")

    def escolher_planilha_modulos(self):
        caminho_dados = filedialog.askopenfilename(title="Escolha a planilha de dados MÓDULOS/SUPLEMENTOS", filetypes=[("Excel files", "*.xlsx *.xls")])
        if caminho_dados:
            self.planilha_path.set(caminho_dados)
            self.tipo_automacao.set("modulos")
            try:
                caminho_comum = 'P:/LA VITA/TI/OptiVita/Bots/01-Lançamento Prescrição/Planilha de Configuração.xlsx/Planilha de Configuração.xlsx'
                self.numero_cliente, self.hora_entrega, self.data_formatada, self.nome_cliente = preparar_cabecalho_cliente(caminho_dados)
                self.dados_df, self.quantitativo_embalagens_df, linhas_com_problemas = preparar_dados_modulos(caminho_dados, caminho_comum, self.numero_cliente)
                if not linhas_com_problemas.empty:
                    self.mostrar_segunda_tela()
                    alerta_problemas.mostrar_alerta_problemas(linhas_com_problemas)
                else:
                    self.mostrar_segunda_tela()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar a planilha: {e}")

    def mostrar_alerta_problemas(self, linhas_com_problemas):
        alerta_janela = tk.Toplevel(self)
        alerta_janela.title("Problemas Detectados")
        alerta_janela.geometry("600x400")

        frame = ttk.Frame(alerta_janela)
        frame.pack(fill='both', expand=True)

        label_titulo = ttk.Label(frame, text="Alerta: Pacientes com dados incompletos!", font=('Helvetica', 14, 'bold'), foreground="#b22222")
        label_titulo.pack(pady=(10, 10))

        container = ttk.Frame(frame)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bd=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        scroll_frame = ttk.Frame(canvas)
        canvas.create_window((0,0), window=scroll_frame, anchor='nw')

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for idx, row in linhas_com_problemas.iterrows():
            print(row['Nr'], row['Paciente'], row.get('Nr. Atend.', 'N/A'))
            detalhes_linha = f"Paciente: {row['Paciente']}, Atendimento: {row.get('Nr. Atend.', 'N/A')}, Nr: {linhas_com_problemas.loc[idx, 'Nr']}"
            label_detalhe = ttk.Label(scroll_frame, text=detalhes_linha, font=('Helvetica', 12))
            label_detalhe.pack(anchor='w', padx=10, pady=5)

        button_fechar = ttk.Button(frame, text="Fechar", command=alerta_janela.destroy)
        button_fechar.pack(side=tk.BOTTOM, pady=10)

    def toggle_all_checkboxes(self):
        all_selected = True
        for var_list in self.pacientes_vars.values():
            if not all(var.get() for var in var_list):
                all_selected = False
                break

        new_value = not all_selected

        for var_list in self.pacientes_vars.values():
            for var in var_list:
                var.set(new_value)

    def mostrar_segunda_tela(self):
        self.limpar_tela_principal()

        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x', expand=True)

        info_cliente = f"Cliente: {self.nome_cliente} - Número: {self.numero_cliente}\nHora de Entrega: {self.hora_entrega} - Data do Pedido: {self.data_formatada}"
        header_label = ttk.Label(main_frame, text=info_cliente, style="TLabel")
        header_label.pack(fill='x', expand=True, pady=(0, 10))

        label = ttk.Label(main_frame, text="Selecione os pacientes para cadastrar:", style="TLabel")
        label.pack(fill='x', expand=True)

        container = ttk.Frame(self)
        container.pack(fill='both', expand=True, side='top')
        canvas = tk.Canvas(container, bd=0, highlightthickness=0, background="#f0f0f0")
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        scroll_frame = ttk.Frame(canvas, style="TFrame")
        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.pacientes_vars = {}
        if self.dados_df is not None:
            for index, row in self.dados_df.iterrows():
                if 'Apresen-tação' in row and row['Apresen-tação'] == 'Ad ↑':
                    pass
                else:
                    var = tk.BooleanVar(value=True)
                    chk = ttk.Checkbutton(scroll_frame, text=f"{row['Nr']} - {row['Paciente']} ({row['Nr. Atend.']})", variable=var, style="TCheckbutton")
                    chk.pack(anchor='w')
                    if row['Paciente'] not in self.pacientes_vars:
                        self.pacientes_vars[row['Paciente']] = []
                    self.pacientes_vars[row['Paciente']].append(var)

        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill='x', expand=False, side='bottom')
        toggle_button = ttk.Button(button_frame, text="Selecionar Tudo", command=self.toggle_all_checkboxes, style="TButton")
        toggle_button.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.mostrar_primeira_tela, style="TButton")
        button_voltar.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        button_avancar = ttk.Button(button_frame, text="Avançar", command=self.mostrar_quarta_tela, style="TButton")
        button_avancar.pack(side='right', padx=5, pady=5, fill='x', expand=True)

    def voltar_segunda_tela(self):
        self.pacientes_vars = {}
        self.mostrar_segunda_tela()
    
    def carregar_hospitais(self, caminho_comum):
        df_hospitais = pd.read_excel(caminho_comum, sheet_name='Hospitais para Cálculo')
        self.hospitais = df_hospitais['Número Hospital'].astype(str).tolist()


    def padronizar_horarios(self, horario):
        horario_limpo = re.sub(r'[^\d/]', '', horario)
        partes = horario_limpo.split('/')
        partes_limpias = [str(int(part.strip())) for part in partes if part.strip()]
        return '/'.join(partes_limpias)

    def calcular_seringas_cheias(self, dados_df, numero_cliente, hospitais):
        resultados = []
        if str(numero_cliente) in hospitais:
            dados_df['Volume (ml)'] = dados_df['Volume (ml)'].astype(int)  # Converte a coluna para inteiro
            dietas_seringa = dados_df[(dados_df['Embalagem'].str.upper() == 'SERINGA') & (dados_df['Volume (ml)'] >= 20)]
            for dieta, grupo in dietas_seringa.groupby('Dieta'):
                total_seringas = 0
                for index, row in grupo.iterrows():
                    horarios = self.padronizar_horarios(row['Horários']).split('/')
                    horarios = [int(h) for h in horarios]
                    volume = row['Volume (ml)']
                    if 20 <= volume <= 39:
                        total_seringas += 1 * len(horarios)
                    elif 40 <= volume <= 59:
                        total_seringas += 2 * len(horarios)
                    elif 60 <= volume <= 79:
                        total_seringas += 3 * len(horarios)
                    elif 80 <= volume <= 99:
                        total_seringas += 4 * len(horarios)
                    elif 100 <= volume <= 119:
                        total_seringas += 5 * len(horarios)
                    elif 120 <= volume <= 139:
                        total_seringas += 6 * len(horarios)
                    elif 140 <= volume <= 159:
                        total_seringas += 7 * len(horarios)
                    elif 160 <= volume <= 179:
                        total_seringas += 8 * len(horarios)
                    elif 180 <= volume <= 199:
                        total_seringas += 9 * len(horarios)
                resultado = (dieta, total_seringas, total_seringas * 20)
                resultados.append(resultado)

            # Ordenar a lista de resultados em ordem decrescente pela quantidade de seringas cheias
            resultados.sort(key=lambda x: x[1], reverse=True)

            # Formatar os resultados para a saída final
            resultados_formatados = [f"{dieta} --> {seringas} seringas cheias ({volume}ml)" for dieta, seringas, volume in resultados]
            return resultados_formatados
        return resultados



    def calcular_seringas_descascar(self, dados_df):
        """
        Calcula o número total de seringas a descascar.
    
        :param dados_df: DataFrame com os dados
        :return: Números totais de seringas de 10ml e 20ml
        """
        total_10ml = 0
        total_20ml = 0
        dados_df['Volume (ml)'] = dados_df['Volume (ml)'].astype(int)  # Converte a coluna para inteiro
        dados_seringa = dados_df[dados_df['Embalagem'].str.upper() == 'SERINGA']
        
        for index, row in dados_seringa.iterrows():
            horarios = self.padronizar_horarios(row['Horários']).split('/')
            horarios = [int(h) for h in horarios]
            volume = row['Volume (ml)']
            if 1 <= volume <= 10:
                total_10ml += 1 * len(horarios)
            elif 11 <= volume <= 20:
                total_20ml += 1 * len(horarios)
            elif 21 <= volume <= 30:
                total_10ml += 1 * len(horarios)
                total_20ml += 1 * len(horarios)
            elif 31 <= volume <= 40:
                total_20ml += 2 * len(horarios)
            elif 41 <= volume <= 50:
                total_10ml += 1 * len(horarios)
                total_20ml += 2 * len(horarios)
            elif 51 <= volume <= 60:
                total_20ml += 3 * len(horarios)
            elif 61 <= volume <= 70:
                total_10ml += 1 * len(horarios)
                total_20ml += 3 * len(horarios)
            elif 71 <= volume <= 80:
                total_20ml += 4 * len(horarios)
            elif 81 <= volume <= 90:
                total_10ml += 1 * len(horarios)
                total_20ml += 4 * len(horarios)
            elif 91 <= volume <= 100:
                total_20ml += 5 * len(horarios)
            elif 101 <= volume <= 110:
                total_10ml += 1 * len(horarios)
                total_20ml += 5 * len(horarios)
            elif 111 <= volume <= 120:
                total_20ml += 6 * len(horarios)
            elif 121 <= volume <= 130:
                total_10ml += 1 * len(horarios)
                total_20ml += 6 * len(horarios)
            elif 131 <= volume <= 140:
                total_20ml += 7 * len(horarios)
            elif 141 <= volume <= 150:
                total_10ml += 1 * len(horarios)
                total_20ml += 7 * len(horarios)
            elif 151 <= volume <= 160:
                total_20ml += 8 * len(horarios)
            elif 161 <= volume <= 170:
                total_10ml += 1 * len(horarios)
                total_20ml += 8 * len(horarios)
            elif 171 <= volume <= 180:
                total_20ml += 9 * len(horarios)
            elif 181 <= volume <= 190:
                total_10ml += 1 * len(horarios)
                total_20ml += 9 * len(horarios)
            elif 191 <= volume <= 200:
                total_20ml += 10 * len(horarios)
        return total_10ml, total_20ml
    

    def gerar_texto_final(self, numero_cliente, nome_cliente, hora_entrega, resultados_seringas_cheias, total_10ml, total_20ml):
        data_atual = datetime.now().strftime("%d/%m/%Y")
        texto = f"HOSPITAL {nome_cliente.upper()}  |  {data_atual}  |  Entrega das {hora_entrega}\n"
        texto += "-" * 75 + "\n"
        if resultados_seringas_cheias:
            texto += "SERINGAS 20 ML CHEIAS\n"
            for resultado in resultados_seringas_cheias:
                texto += f"{resultado}\n"
        texto += "\nSERINGAS A SEREM DESCASCADAS AO TODO\n"
        texto += f"{total_10ml} Seringas de 10ml\n"
        texto += f"{total_20ml} Seringas de 20ml\n"
        texto += "-" * 75 + "\n"
        return texto

    def mostrar_quarta_tela(self):
        self.limpar_tela_principal()
        
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill='x', expand=True)

        label = ttk.Label(main_frame, text="Certifique-se de que o sistema esteja aberto, maximizado e visível.", style="TLabel")
        label.pack(pady=(0, 20))

        label_velocidade = ttk.Label(main_frame, text="Escolha a velocidade da execução:", style="TLabel")
        label_velocidade.pack()

        opcoes_velocidade = {"Rápida": "0", "Média (Rede Lenta)": "0.1", "Lenta (Rede Muito Lenta)": "0.5"}
        self.velocidade = tk.StringVar(value="0")
        for texto, valor in opcoes_velocidade.items():
            rb = ttk.Radiobutton(main_frame, text=texto, variable=self.velocidade, value=valor, style="TRadiobutton")
            rb.pack(anchor='w')

        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=20, fill='x')

        if self.tipo_automacao.get() == 'dieta':
            self.button_copiar = ttk.Button(button_frame, text="Copiar Dados Seringas", command=self.copiar_texto, style="TButton")
            self.button_copiar.pack(side=tk.RIGHT, padx=5)
        
            self.button_iniciar = ttk.Button(button_frame, text="Rodar", command=self.executar_bot, style="TButton", state=tk.DISABLED)
            self.button_iniciar.pack(side=tk.RIGHT, padx=5)

        if self.tipo_automacao.get() == 'modulos':
            self.button_iniciar = ttk.Button(button_frame, text="Rodar", command=self.executar_bot, style="TButton")
            self.button_iniciar.pack(side=tk.RIGHT, padx=5)

        button_cancelar = ttk.Button(button_frame, text="Cancelar", command=self.cancelar, style="TButton")
        button_cancelar.pack(side=tk.RIGHT, padx=5)

        button_voltar = ttk.Button(button_frame, text="Voltar", command=self.voltar_segunda_tela, style="TButton")
        button_voltar.pack(side=tk.LEFT, padx=5, pady=5)

    def copiar_texto(self):
        resultados_seringas_cheias = self.calcular_seringas_cheias(self.dados_df, self.numero_cliente, self.hospitais)
        total_10ml, total_20ml = self.calcular_seringas_descascar(self.dados_df)
        texto_final = self.gerar_texto_final(self.numero_cliente, self.nome_cliente, self.hora_entrega, resultados_seringas_cheias, total_10ml, total_20ml)
        self.clipboard_clear()
        self.clipboard_append(texto_final)
        self.button_iniciar.config(state=tk.NORMAL)

    def cancelar(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.destroy()
            sys.exit()
    
    def on_close(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.destroy()
            sys.exit()

    def coletar_pacientes_selecionados(self):
        pacientes_selecionados = []
        for nome_paciente, var_list in self.pacientes_vars.items():
            if any(var.get() for var in var_list):
                pacientes_selecionados.append(nome_paciente)
        return pacientes_selecionados

    def executar_bot(self):
        pacientes_selecionados = self.coletar_pacientes_selecionados()
        espera = float(self.velocidade.get())
        caminho_dados = self.planilha_path.get()
        caminho_comum = "P:/LA VITA/TI/BotCity/Planilha de Configuração HOMOLOGAÇÃO 03.xlsx"
        tipo_automacao = self.tipo_automacao.get()
        self.iconify()
        main(pacientes_selecionados, espera, caminho_dados, caminho_comum, tipo_automacao)
        self.deiconify()
        self.destroy()

def restart_app():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    restart_app()
