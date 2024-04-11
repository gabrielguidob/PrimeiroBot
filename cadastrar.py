"""
    Cadastrar novo paciente: (Funciona ctrl v)
Arquivos > Cadastro > Paciente > codigo cliente > enter no codigo do paciente que gera um novo > colar o nome do paciente > enter > enter > enter > colar Nr. Atend. no registro hospitalar > numero do leito > deixar tudo adulto por enquanto > 2 enter
"""

from time import sleep
import pandas as pd
from inserir import inserir_codigo_cliente_cadastro, abrir_cadastro_paciente
from log import adicionar_log



def cadastrar_pacientes(pacientes_para_cadastro, espera, dados_df, bot, not_found, num_cliente, operacoes_logs):
    if not pacientes_para_cadastro:
        print("Nenhum paciente selecionado para cadastro.")
        return

    # Filtra a DataFrame para conter apenas os pacientes selecionados
    dados_df_filtrado = dados_df[dados_df['Nome'].isin(pacientes_para_cadastro)]

    abrir_cadastro_paciente(bot, not_found)
    
    # Itera sobre cada linha do DataFrame filtrado
    for _, info_paciente in dados_df_filtrado.iterrows():
        
        inserir_codigo_cliente_cadastro(bot, not_found, num_cliente)
          
        bot.enter()
        bot.kb_type(info_paciente['Nome'])
        bot.enter()
        bot.enter()
        bot.enter()

        bot.kb_type(str(info_paciente['Nr. Atend.']))
        bot.enter()

        bot.kb_type(str(info_paciente['Leito']))
        bot.enter()
        bot.kb_type('ADULTO')
        bot.enter()
        bot.enter()

        sleep(espera)

    adicionar_log(operacoes_logs, info_paciente['Nome'], "Cadastro")

    print("Todos os pacientes selecionados foram cadastrados.")





