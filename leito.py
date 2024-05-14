from time import sleep
import pandas as pd
from log import adicionar_log
from inserir import (inserir_codigo_cliente_cadastro, abrir_cadastro_paciente,inserir_codigo_paciente_leito)

def atualizar_leitos(pacientes_mudaram_leito, index, espera, bot, not_found, numero_cliente, operacoes_logs):
    """
    Atualiza os leitos dos pacientes selecionados.

    Esta função itera sobre os pacientes selecionados para atualizar seus leitos no sistema, utilizando as funções de automação definidas.
    Se nenhum paciente for selecionado para a atualização, a função termina prematuramente.

    Parâmetros:
        pacientes_para_atualizar_leito (list): Lista de nomes dos pacientes selecionados para atualização de leito.
        espera (int): Tempo de espera (em segundos) para operações de automação, para garantir a sincronização com a interface do sistema.
        pacientes_mudaram_leito (DataFrame): DataFrame contendo os dados dos pacientes.
        bot (DesktopBot): Instância do bot para realizar as operações de automação.
        not_found (function): Função a ser chamada caso um elemento esperado não seja encontrado durante a automação.
        numero_cliente (str): Número do cliente utilizado nas operações de cadastro e atualização de leitos.
        operacoes_logs (dict): Dicionário para armazenar os logs das operações realizadas.

    Retorna:
        None
    """
    #if not pacientes_mudaram_leito:
    #    print("Nenhum paciente selecionado para atualização de leito.")
    #    return
    

    abrir_cadastro_paciente(bot, not_found)
    

    inserir_codigo_cliente_cadastro(bot, not_found, numero_cliente)
    print(pacientes_mudaram_leito)
    #nome_paciente = str(pacientes_mudaram_leito['Paciente'])
    inserir_codigo_paciente_leito(bot, pacientes_mudaram_leito.loc[index, 'Paciente'], espera, not_found)
    
    # Sequência de comandos para inserir informações no sistema e atualizar o leito
    bot.enter()
    bot.enter()
    bot.enter()
    bot.enter()
    bot.control_a()
    bot.control_c()
    registro = bot.get_clipboard()
    if registro == pacientes_mudaram_leito.loc[index, 'Nr. Atend.']:
        bot.enter()
        leito = pacientes_mudaram_leito.loc[index, 'Nr. Leito']
        bot.kb_type(leito)
        bot.enter()
        bot.kb_type('ADULTO')  # Presume-se que todos os pacientes são adultos
        bot.enter()
        bot.enter()

        sleep(espera)  # Espera para garantir a sincronização com a interface do sistema

        # Adiciona a operação de atualização de leito ao log de operações
        adicionar_log(operacoes_logs, pacientes_mudaram_leito.loc[index, 'Paciente'], "Atualização do Leito", status = 0)

        print("Todos os leitos dos pacientes selecionados foram atualizados.")
    else: 
        if not bot.find("cancelar", matching=0.97, waiting_time=10000):
            not_found("cancelar")
        bot.click()
            
        adicionar_log(operacoes_logs, pacientes_mudaram_leito.loc[index, 'Paciente'], "Atualização do Leito", status = 1)

        print("Todos os leitos dos pacientes selecionados foram atualizados.")
