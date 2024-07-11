from inserir import *
from time import sleep
from leito import atualizar_leitos


'''
COLUNAS DA DF
['Nr', 'Nr. Atend.', 'Paciente', 'Unidade', 'Nr. Leito', 'Mudou Leito?',
       'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem', 'Módulo',
       'Quantidade\n(GR ou ML)', 'Apresen-tação', 'CodProduto Sistema',
       'Via Adm Sistema']
'''

def prescricao_modulos_suplementos(dados_df, bot, espera, not_found, numero_cliente, operacoes_logs, hora_entrega):

    #Criando Df para os que precisam alterar o leito
    pacientes_mudaram_leito = dados_df[dados_df['Mudou Leito?'].astype(str).str.upper() == 'SIM']
    print(pacientes_mudaram_leito['Mudou Leito?'])

    for index, row in pacientes_mudaram_leito.iterrows():
        # Aplicando a função para encontrar o 'Quantitativo Sistema' correspondente para cada linha
        # Assegure-se de que 'quantitativo_embalagens_df' esteja definido e disponível neste escopo
        atualizar_leitos(pacientes_mudaram_leito, index, espera, bot, not_found, numero_cliente, operacoes_logs)

    primeira_iteracao = True
    

    for index, row in dados_df.iterrows():
        grupo = row['Grupo']
        repeticao = row['Segunda_Ocorrencia']
        quantitativo = dados_df.loc[index, 'Quantitativo Sistema']
        
        if grupo == 'Módulos':
            if repeticao or primeira_iteracao:
                # Adicione aqui a lógica específica para Módulos com Segunda_Ocorrencia = True
                sleep(1)
                verificando_solicitacao(bot, not_found)
                sleep(1)
                inserir_codigo_cliente(bot, numero_cliente, not_found, espera)
                print(f"Linha {index} - Módulos com Segunda_Ocorrencia: {row.to_dict()}")
                
            
            inserir_codigo_paciente(bot, dados_df, index, not_found, espera, numero_cliente)
            encontrar_mensagem_cadastrar_paciente(index, espera, dados_df, bot, not_found, operacoes_logs)
            sleep(1)
            bot.enter()
            pop_up_erro(bot, not_found, espera, hora_entrega)                       
            inserir_horario_entrega(bot, not_found, espera, hora_entrega)     
            inserir_hora(bot, espera, not_found, index, hora_entrega, primeira_iteracao, dados_df)
            pop_up_erro(bot, not_found, espera, hora_entrega)           
            inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found)           
            inserir_crm_padrao(bot, espera, not_found)
            inserir_produto(bot, dados_df, index, espera)
            inserir_via_adm(bot, dados_df, index, espera)
            inserir_recipiente(bot, dados_df, index, espera)
            inserir_volume(bot, dados_df, index, espera, not_found)
            inserir_horarios(bot, dados_df, index, not_found, espera)
            inserir_quantitativo_embalagens(bot, quantitativo, not_found, espera, dados_df, index)
            print(f"Linha {index} - Módulos sem Segunda_Ocorrencia: {row.to_dict()}")
            primeira_iteracao = False
            

        elif grupo == 'Suplementos':
            if repeticao:
                # Adicione aqui a lógica específica para Suplementos com Segunda_Ocorrencia = True
                sleep(1)
                verificando_solicitacao(bot, not_found)
                sleep(1)
                inserir_codigo_cliente(bot, numero_cliente, not_found, espera)
                print(f"Linha {index} - Suplementos com Segunda_Ocorrencia: {row.to_dict()}")
            
            inserir_codigo_paciente(bot, dados_df, index, not_found, espera, numero_cliente)
            encontrar_mensagem_cadastrar_paciente(index, espera, dados_df, bot, not_found, operacoes_logs)
            pop_up_erro(bot, not_found, espera, hora_entrega)
            inserir_hora(bot, espera, not_found, index, hora_entrega, primeira_iteracao, dados_df)
            inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found)
            inserir_crm_padrao(bot, espera, not_found)
            inserir_produto(bot, dados_df, index, espera)
            inserir_via_adm(bot, dados_df, index, espera)
            inserir_recipiente(bot, dados_df, index, espera)
            inserir_volume(bot, dados_df, index, espera, not_found)
            inserir_horarios(bot, dados_df, index, not_found, espera)
            inserir_quantitativo_embalagens(bot, quantitativo, not_found, espera, dados_df, index)
            print(f"Linha {index} - Suplementos sem Segunda_Ocorrencia: {row.to_dict()}")

        elif grupo == 'Módulos em Dietas':
            sleep(1)
            verificando_solicitacao(bot, not_found)
            sleep(1)
            inserir_codigo_cliente(bot, numero_cliente, not_found, espera)
            inserir_codigo_paciente(bot, dados_df, index, not_found, espera, numero_cliente)
            encontrar_mensagem_cadastrar_paciente(index, espera, dados_df, bot, not_found, operacoes_logs)
            pop_up_erro(bot, not_found, espera, hora_entrega)
            inserir_hora(bot, espera, not_found, index, hora_entrega, primeira_iteracao, dados_df)
            inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found)
            inserir_crm_padrao(bot, espera, not_found)
            inserir_produto(bot, dados_df, index, espera)
            inserir_via_adm(bot, dados_df, index, espera)
            inserir_recipiente(bot, dados_df, index, espera)
            inserir_volume(bot, dados_df, index, espera, not_found)
            inserir_horarios(bot, dados_df, index, not_found, espera)
            inserir_quantitativo_embalagens(bot, quantitativo, not_found, espera, dados_df, index)
            print(f"Linha {index} - Módulos com Segunda_Ocorrencia: {row.to_dict()}")



