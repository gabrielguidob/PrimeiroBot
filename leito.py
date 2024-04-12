from time import sleep
import pandas as pd
from log import adicionar_log
from inserir import (inserir_codigo_cliente_cadastro, abrir_cadastro_paciente,inserir_codigo_paciente_leito)

def atualizar_leitos(pacientes_para_atualizar_leito, espera, dados_df, bot, not_found, num_cliente, operacoes_logs):
    """
    Atualiza os leitos dos pacientes selecionados.

    Esta função itera sobre os pacientes selecionados para atualizar seus leitos no sistema, utilizando as funções de automação definidas.
    Se nenhum paciente for selecionado para a atualização, a função termina prematuramente.

    Parâmetros:
        pacientes_para_atualizar_leito (list): Lista de nomes dos pacientes selecionados para atualização de leito.
        espera (int): Tempo de espera (em segundos) para operações de automação, para garantir a sincronização com a interface do sistema.
        dados_df (DataFrame): DataFrame contendo os dados dos pacientes.
        bot (DesktopBot): Instância do bot para realizar as operações de automação.
        not_found (function): Função a ser chamada caso um elemento esperado não seja encontrado durante a automação.
        num_cliente (str): Número do cliente utilizado nas operações de cadastro e atualização de leitos.
        operacoes_logs (dict): Dicionário para armazenar os logs das operações realizadas.

    Retorna:
        None
    """
    if not pacientes_para_atualizar_leito:
        print("Nenhum paciente selecionado para atualização de leito.")
        return

    # Filtra a DataFrame para conter apenas os pacientes selecionados
    dados_df_filtrado = dados_df[dados_df['Nome'].isin(pacientes_para_atualizar_leito)]

    abrir_cadastro_paciente(bot, not_found)
    
    # Itera sobre cada linha do DataFrame filtrado para atualizar o leito de cada paciente
    for _, info_paciente in dados_df_filtrado.iterrows():
        inserir_codigo_cliente_cadastro(bot, not_found, num_cliente)
        inserir_codigo_paciente_leito(bot, info_paciente['Nome'], espera, not_found)
     
        # Sequência de comandos para inserir informações no sistema e atualizar o leito
        bot.enter()
        bot.enter()
        bot.enter()
        bot.enter()
        bot.enter()

        bot.kb_type(str(info_paciente['Leito']))
        bot.enter()
        bot.kb_type('ADULTO')  # Presume-se que todos os pacientes são adultos
        bot.enter()
        bot.enter()

        sleep(espera)  # Espera para garantir a sincronização com a interface do sistema

        # Adiciona a operação de atualização de leito ao log de operações
        adicionar_log(operacoes_logs, info_paciente['Nome'], "Atualização do Leito")

    print("Todos os leitos dos pacientes selecionados foram atualizados.")

