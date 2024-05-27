from time import sleep
import pandas as pd
from log import adicionar_log

def cadastrar_paciente(index, espera, dados_df, bot, not_found, operacoes_logs):
    """
    Cadastra novos pacientes no sistema.

    Esta função itera sobre uma lista de pacientes selecionados para realizar o cadastro de cada um no sistema, 
    usando automação de interface de usuário. Caso a lista de pacientes para cadastro esteja vazia, 
    a função termina prematuramente.

    Parâmetros:
        pacientes_para_cadastro (list): Lista de nomes dos pacientes selecionados para cadastro.
        espera (int): Tempo de espera (em segundos) para operações de automação, ajustando a sincronização com a interface do sistema.
        dados_df (DataFrame): DataFrame contendo os dados dos pacientes.
        bot (DesktopBot): Instância do bot para realizar as operações de automação.
        not_found (function): Função callback chamada se um elemento esperado não for encontrado.
        num_cliente (str): Número do cliente, usado nas operações de cadastro.
        operacoes_logs (dict): Dicionário para armazenar logs das operações realizadas.

    Retorna:
        None
    """
    #if not pacientes_para_cadastro:
    #    print("Nenhum paciente selecionado para cadastro.")
    #    return
#
    ## Filtra o DataFrame para incluir apenas os pacientes selecionados para cadastro
    #dados_df_filtrado = dados_df[dados_df['Nome'].isin(pacientes_para_cadastro)]
#
    ## Inicia o processo de cadastro no sistema
    #abrir_cadastro_paciente(bot, not_found)
    #
    ## Realiza o cadastro para cada paciente filtrado
    #for _, info_paciente in dados_df_filtrado.iterrows():
        
    # Sequência de comandos para inserir informações do paciente no sistema
    #inserir_codigo_cliente_cadastro(bot, not_found, num_cliente)
    #bot.enter()
    sleep(1)
    bot.enter()
    bot.kb_type(dados_df.loc[index, 'Paciente'])
    bot.enter()
    bot.enter()
    bot.enter()
    nr_atend = dados_df.loc[index, 'Nr. Atend.']
    bot.kb_type(nr_atend)
    bot.enter()
    nr_leito = dados_df.loc[index, 'Nr. Leito']
    print(nr_leito)
    bot.kb_type(nr_leito)
    bot.enter()
    bot.kb_type('ADULTO')  # Assume-se que todos os pacientes são adultos por padrão
    bot.enter()
    bot.enter()
    # Aguarda a sincronização com a interface do sistema
    sleep(espera)
    # Registra a operação de cadastro no log
    adicionar_log(operacoes_logs, dados_df.loc[index, 'Paciente'], "Cadastro do Paciente", dados_df.loc[index, 'Nr'], status = 0)

    print("Todos os pacientes selecionados foram cadastrados.")






