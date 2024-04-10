"""
    Cadastrar novo paciente: (Funciona ctrl v)
Arquivos > Cadastro > Paciente > codigo cliente > enter no codigo do paciente que gera um novo > colar o nome do paciente > enter > enter > enter > colar Nr. Atend. no registro hospitalar > numero do leito > deixar tudo adulto por enquanto > 2 enter
"""

from time import sleep
import pandas as pd
from inserir import inserir_codigo_cliente_cadastro, abrir_cadastro_paciente

# Exemplo de como sua função cadastrar_pacientes pode usar a filtragem
'''
def cadastrar_pacientes(pacientes_para_cadastro, espera, dados_df, bot, not_found, num_cliente):
    if not pacientes_para_cadastro:
        print("Nenhum paciente selecionado para cadastro.")
        return

    # Filtra a DataFrame para conter apenas os pacientes selecionados
    dados_df_filtrado = dados_df[dados_df['Nome'].isin(pacientes_para_cadastro)]

    abrir_cadastro_paciente(bot, not_found)
        

    for nome_paciente in pacientes_para_cadastro:
        # Obtém as informações do paciente atual na DataFrame filtrada
        info_paciente = dados_df_filtrado[dados_df_filtrado['Nome'] == nome_paciente].iloc[0]
        
        inserir_codigo_cliente_cadastro(bot, not_found, num_cliente)

        bot.enter()
        bot.kb_type(nome_paciente)
        bot.enter()
        bot.enter()
        bot.enter()

        # Agora acessamos diretamente os valores usando .iloc[0] e convertemos para string
        bot.kb_type(str(info_paciente['Nr. Atend.']))
        bot.enter()

        # Se Leito for numérico, converta para string; caso contrário, apenas use como está
        bot.kb_type(str(info_paciente['Leito']))
        bot.enter()
        bot.enter()
        bot.enter()
        bot.enter()
        
        print(f"Cadastrando paciente: {nome_paciente}")
        # Para imprimir as informações, podemos usar o método to_dict('records')[0] diretamente no info_paciente sem filtrar novamente
        print("Informações:", info_paciente.to_dict())
        print("\n")
        sleep(espera)

    print("Todos os pacientes selecionados foram cadastrados.")
'''

def cadastrar_pacientes(pacientes_para_cadastro, espera, dados_df, bot, not_found, num_cliente):
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

        
        print(f"Cadastrando paciente: {info_paciente['Nome']}")
        print("Informações:", info_paciente.to_dict())
        print("\n")
        sleep(espera)

    print("Todos os pacientes selecionados foram cadastrados.")





