from inserir import *
from time import sleep
from leito import atualizar_leitos
from log_modulos import exibir_logs, adicionar_log
from tkinter import messagebox


'''
COLUNAS DA DF
['Nr', 'Nr. Atend.', 'Paciente', 'Unidade', 'Nr. Leito', 'Mudou Leito?',
       'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem', 'Módulo',
       'Quantidade\n(GR ou ML)', 'Apresen-tação', 'CodProduto Sistema',
       'Via Adm Sistema']
'''

def encontrar_linhas_adicionais(dados_df, index, row):
    # Identificar todas as linhas 'Ad ↑' relacionadas
    linhas_adicionais = []
    for i in range(index + 1, len(dados_df)):
        if dados_df.loc[i, 'Apresen-tação'] == 'Ad ↑' and dados_df.loc[i, 'Nr. Atend.'] == row['Nr. Atend.'] and dados_df.loc[i, 'Paciente'] == row['Paciente']:
            linhas_adicionais.append(dados_df.loc[i])

    return linhas_adicionais


def prescricao_modulos_suplementos(dados_df, bot, espera, not_found, numero_cliente, operacoes_logs, hora_entrega):
    # Criando Df para os que precisam alterar o leito
    print(f'ANTES FILTRO: {dados_df}')
    pacientes_mudaram_leito = dados_df[dados_df['Mudou Leito?'].astype(str).str.upper() == 'SIM']
    print(pacientes_mudaram_leito['Mudou Leito?'])
    print(f'DEPOIS FILTRO: {dados_df}')

    for index, row in pacientes_mudaram_leito.iterrows():
        atualizar_leitos(pacientes_mudaram_leito, index, espera, bot, not_found, numero_cliente, operacoes_logs)

    primeira_iteracao = True
    primeira_iteracao_suplemento = True

    for index, row in dados_df.iterrows():
        print(f'ENTROU FOR - Index: {index}')
        row = dados_df.loc[index]
        print(f'Processando linha: {row.to_dict()}')

        if row['Apresen-tação'] == 'Ad ↑':
            continue

        grupo = row['Grupo']
        repeticao = row['Segunda_Ocorrencia']
        quantitativo = dados_df.loc[index, 'Quantitativo Sistema']

        # Identificar todas as linhas 'Ad ↑' relacionadas
        linhas_adicionais = encontrar_linhas_adicionais(dados_df, index, row)
        #print(dados_df.loc[index+1, 'Apresen-tação'])
        print(f'LINHAS ADICIONAIS: {linhas_adicionais}')


        if grupo == 'Módulos':
            if repeticao or primeira_iteracao:
                print(f"Linha {index} - Módulos com Segunda_Ocorrencia: {row.to_dict()}")
                sleep(1)
                verificando_solicitacao(bot, not_found)
                sleep(1)
                inserir_codigo_cliente(bot, numero_cliente, not_found, espera)

            print(f"Linha {index} - Módulos sem Segunda_Ocorrencia: {row.to_dict()}")
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
            inserir_modulos(bot, not_found, index, dados_df, linhas_adicionais)
            primeira_iteracao = False

        elif grupo == 'Suplementos':
            print('ENTROU IF GRUPO Suplementos')
            if repeticao or primeira_iteracao:
                print(f"Linha {index} - Suplementos com Segunda_Ocorrencia: {row.to_dict()}")
                sleep(1)
                verificando_solicitacao(bot, not_found)
                sleep(1)
                inserir_codigo_cliente(bot, numero_cliente, not_found, espera)

            print(f"Linha {index} - Suplementos sem Segunda_Ocorrencia: {row.to_dict()}")
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
             

        elif grupo == 'Módulos em Dietas':
            primeira_iteracao = True
            print(f"ENTROU IF GRUPO Módulos em Dietas - Linha {index}: {row.to_dict()}")
            sleep(1)
            verificando_solicitacao(bot, not_found)
            sleep(1)
            inserir_codigo_cliente(bot, numero_cliente, not_found, espera)
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
            inserir_modulos(bot, not_found, index, dados_df, linhas_adicionais)
        
        # Log do progresso
        adicionar_log(operacoes_logs, dados_df.loc[index, 'Paciente'], "Cadastro do Módulo/Suplemento", dados_df.loc[index, 'Nr'], status = 0)     

    messagebox.showerror("Acabou","A automação chegou ao fim!")
    exibir_logs(operacoes_logs)
    print('Automação finalizada')



