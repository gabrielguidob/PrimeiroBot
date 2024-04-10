"""
Alterar paciente: 
Arquivos > Cadastro > Paciente > codigo cliente > F2 msm função pra escrever o nome > apos isso vai direto para o botao alterar, apenas apertar enter > depois apertar mais 4 enter > paste no numero do leito > mais 3 enter 
"""


from time import sleep
import pandas as pd
from inserir import (inserir_codigo_cliente_cadastro, abrir_cadastro_paciente,inserir_codigo_paciente_leito)
''' 
# Exemplo de como sua função atualizar_leitos pode usar a filtragem
def atualizar_leitos(pacientes_para_atualizar_leito, espera, dados_df, bot, not_found, num_cliente):
    if not pacientes_para_atualizar_leito:
        print("Nenhum paciente selecionado para atualização de leito.")
        return

    # Filtra a DataFrame para conter apenas os pacientes selecionados
    dados_df_filtrado = dados_df[dados_df['Nome'].isin(pacientes_para_atualizar_leito)]

    abrir_cadastro_paciente(bot, not_found)

    for nome_paciente in pacientes_para_atualizar_leito:
        # Obtém as informações do paciente atual na DataFrame filtrada
        info_paciente = dados_df_filtrado[dados_df_filtrado['Nome'] == nome_paciente].iloc[0]
        
        inserir_codigo_cliente_cadastro(bot, not_found, num_cliente)
        inserir_codigo_paciente_leito(bot, nome_paciente, espera, not_found)
     
        bot.enter()
        bot.enter()
        bot.enter()
        bot.enter()
        bot.enter()

        bot.kb_type(str(info_paciente['Leito']))
        bot.enter()
        bot.enter()
        bot.enter()
        # Exemplo de como atualizar o leito do paciente
        print(f"Atualizando leito do paciente: {nome_paciente}")

        print("Informações:", info_paciente.to_dict())
        print("\n")
        sleep(espera)

    print("Todos os leitos dos pacientes selecionados foram atualizados.")
    '''
def atualizar_leitos(pacientes_para_atualizar_leito, espera, dados_df, bot, not_found, num_cliente):
    if not pacientes_para_atualizar_leito:
        print("Nenhum paciente selecionado para atualização de leito.")
        return

    # Filtra a DataFrame para conter apenas os pacientes selecionados
    dados_df_filtrado = dados_df[dados_df['Nome'].isin(pacientes_para_atualizar_leito)]

    abrir_cadastro_paciente(bot, not_found)
    
    # Itera sobre cada linha do DataFrame filtrado
    for _, info_paciente in dados_df_filtrado.iterrows():
        inserir_codigo_cliente_cadastro(bot, not_found, num_cliente)
        inserir_codigo_paciente_leito(bot, info_paciente['Nome'], espera, not_found)
     
        bot.enter()
        bot.enter()
        bot.enter()
        bot.enter()
        bot.enter()

        bot.kb_type(str(info_paciente['Leito']))
        bot.enter()
        bot.kb_type('ADULTO')
        bot.enter()
        bot.enter()
        
        print(f"Atualizando leito do paciente: {info_paciente['Nome']}")
        print("Informações:", info_paciente.to_dict())
        print("\n")
        sleep(espera)

    print("Todos os leitos dos pacientes selecionados foram atualizados.")
