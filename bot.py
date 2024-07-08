# Importações necessárias
from botcity.core import DesktopBot
from botcity.maestro import BotMaestroSDK
import pandas as pd
from openpyxl import load_workbook
import keyboard
from datetime import datetime
from time import sleep
from leito import atualizar_leitos
from cadastrar import cadastrar_paciente
from log import exibir_logs, adicionar_log
import pygetwindow as gw
import pyautogui
from inserir import (
    verificando_solicitacao, inserir_codigo_cliente, inserir_codigo_paciente,
    inserir_hora, inserir_unidade_de_interacao, inserir_crm_padrao, inserir_produto, inserir_via_adm, inserir_recipiente,
    inserir_volume, inserir_horarios, inserir_quantitativo_embalagens, pop_up_erro, inserir_horario_entrega, encontrar_mensagem_cadastrar_paciente)
import unicodedata

from tkinter import messagebox


# para baixar o executavel pyinstaller --noconsole --onefile --add-data "resources;resources" interface.py


def normalize_spaces(text):
    if pd.isna(text):
        return text  # Retorna o valor original se for NaN
    return ''.join(' ' if unicodedata.category(char) == 'Zs' else char for char in text)

def normalize_dataframe(df):
    # Aplica a normalização de espaços a todas as colunas do tipo string
    for col in df.columns:
        if df[col].dtype == 'O':  # Verifica se o tipo da coluna é 'object', geralmente usado para strings
            df[col] = df[col].apply(normalize_spaces)
    return df

# Desabilita erros se não estiver conectado ao Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def not_found(label):
    """
    Função chamada quando um elemento esperado não é encontrado na interface.
    
    :param label: Rótulo do elemento que não foi encontrado.
    """
    print(f"Elemento não encontrado: {label}")

def preparar_cabecalho_cliente(caminho_dados):
    """
    Lê informações específicas do cliente de uma planilha Excel.

    :param caminho_dados: Caminho para a planilha de onde as informações serão lidas.
    :return: Uma tupla contendo o número do cliente, a hora de entrega e a data do pedido formatada.
    """
 
    workbook = load_workbook(caminho_dados)
    sheet = workbook.active
    
    numero_cliente_completo = str(sheet["G5"].value)
    # Divide a string pelo hífen
    partes = numero_cliente_completo.split('-')
    numero_cliente = partes[0].strip()
    nome_cliente = partes[1].strip() if len(partes) > 1 else ''
    hora_entrega = str(sheet["L5"].value)
    data_pedido = sheet["P5"].value
    workbook.close()

    # Converte data_pedido para datetime se não estiver no formato correto
    if not isinstance(data_pedido, datetime):
        # Assume que data_pedido é uma string no formato 'yyyy-mm-dd HH:MM:SS'
        data_pedido = datetime.strptime(data_pedido, "%Y-%m-%d %H:%M:%S")

    # Formata a data no formato 'dd/mm/yyyy'
    data_formatada = data_pedido.strftime('%d/%m/%Y')

    return numero_cliente, hora_entrega, data_formatada, nome_cliente

def preparar_dados(caminho_dados, caminho_comum):

    caminho_comum = '.\Planilha de Configuração.xlsx'
    # Leitura da planilha de dados específica
    dados_df = pd.read_excel(caminho_dados, skiprows=7, dtype=str)
    dados_df = normalize_dataframe(dados_df)
    dados_df.columns = dados_df.columns.str.strip()


    # Filtra as linhas onde 'Nr. Atend.' e 'Paciente' são ambos NaN (nulos) ou onde 'Dieta' é 'DIETA ZERO'
    dados_df = dados_df.dropna(subset=['Nr. Atend.', 'Paciente'], how='all')  # Remove se ambas as colunas forem NaN
    dados_df = dados_df[dados_df['Dieta'] != 'DIETA ZERO']  # Remove se a dieta for 'DIETA ZERO'

    # Remover colunas que não são necessárias
    colunas_para_remover = ['N', 'M', 'D', 'E', 'Módulo', 'Quantidade\n(GR ou ML)', 'Apresen-tação', 'Observações Gerais']
    dados_df = dados_df.drop(columns=colunas_para_remover)


    # Leitura das planilhas com caminho comum
    produtos_df = pd.read_excel(caminho_comum, sheet_name='Produto', dtype=str)
    via_adm_df = pd.read_excel(caminho_comum, sheet_name='Via Adm')

    produtos_df = normalize_dataframe(produtos_df)
    via_adm_df = normalize_dataframe(via_adm_df)

    produtos_df['Produto Prescrição'] = produtos_df['Produto Prescrição'].str.strip().str.lower()
    dados_df['Dieta'] = dados_df['Dieta'].str.strip().str.lower()
    produtos_df['Produto Prescrição'] = produtos_df['Produto Prescrição'].str.strip().str.upper()
    dados_df['Dieta'] = dados_df['Dieta'].str.strip().str.upper()


    # Adicionando a coluna CodProduto Sistema
    dados_df = pd.merge(dados_df, produtos_df, left_on='Dieta', right_on='Produto Prescrição', how='left')
    # Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
    dados_df.drop(columns=['Produto Prescrição'], inplace=True)
    
    print(dados_df.isnull().sum())  # Isso mostrará a quantidade de NaNs em cada coluna após o merge.

    # Adicionando a coluna Via Adm Prescrição
    dados_df = pd.merge(dados_df, via_adm_df, left_on='Via Adm', right_on='Via Adm Prescrição', how='left')
    # Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
    dados_df.drop(columns=['Via Adm Prescrição'], inplace=True)

    # Criando a quantitativo_embalagens_df
    quantitativo_embalagens_df = pd.read_excel(caminho_comum, sheet_name='Quantitativo Embalagens', dtype=str)

    quantitativo_embalagens_df = normalize_dataframe(quantitativo_embalagens_df)

    print(dados_df['Dieta'])


    # Define colunas para verificar
    colunas_verificar = ['Nr. Atend.', 'Paciente', 'Nr. Leito', 'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem', 'CodProduto Sistema', 'Via Adm Sistema']
    cota_extra_verificar = ['Paciente', 'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem', 'CodProduto Sistema', 'Via Adm Sistema']

    # Remover espaços em branco no final dos valores da coluna 'Paciente'
    dados_df['Paciente'] = dados_df['Paciente'].str.strip()

    # Separação de dados
    cota_extra_df = dados_df[dados_df['Paciente'] == 'COTA EXTRA'].copy()
    outros_df = dados_df[dados_df['Paciente'] != 'COTA EXTRA'].copy()
    print(f'Cota EXtra verificar: {cota_extra_df}')

    # Identifica linhas com problemas nas colunas especificadas
    linhas_com_problemas_df = outros_df[outros_df[colunas_verificar].isna().any(axis=1)]
    linhas_cota_extra_problemas_df = cota_extra_df[cota_extra_df[cota_extra_verificar].isna().any(axis=1)]

    # Aplica filtro para NaN com as colunas apropriadas
    outros_df.dropna(subset=colunas_verificar, inplace=True)
    cota_extra_df.dropna(subset=cota_extra_verificar, inplace=True)

    # Combinação de dataframes após limpeza
    dados_df = pd.concat([cota_extra_df, outros_df])

    # Combina os registros problemáticos para exibição ou log
    print(f' Linhas com Problemas DF: {linhas_com_problemas_df}')
    print(f' Linhas com Problemas COTA EXTRA: {linhas_cota_extra_problemas_df}')
    linhas_com_problemas_df = pd.concat([linhas_com_problemas_df, linhas_cota_extra_problemas_df])
    print('Linhas com problemas:')
    print(linhas_com_problemas_df)

    # Normalização dos DataFrames
    print(f' Linhas com Problemas: {linhas_com_problemas_df}')



    return dados_df, quantitativo_embalagens_df, linhas_com_problemas_df

def marcar_duplicatas(df, coluna):
    # Inicializa a nova coluna com False
    df['Segunda_Ocorrencia'] = False
    
    # Verifica onde as duplicatas começam, exceto a primeira ocorrência
    mask = df.duplicated(coluna, keep='first')
    
    # Marca as duplicatas subsequentes com True
    df.loc[mask, 'Segunda_Ocorrencia'] = True
    
     # Reordena o DataFrame para colocar as duplicatas ao final
    df = df.sort_values(by='Segunda_Ocorrencia', ascending=True)

    return df

def encontrar_quantitativo(row, quantitativo_embalagens_df, numero_cliente):
    embalagem= row['Embalagem'].strip().upper()  # Certifique-se de remover espaços extras
    volume = float(row['Volume (ml)'])

    # Certifique-se de que os tipos de dados para comparação sejam apropriados
    quantitativo_embalagens_df['Código Cliente'] = quantitativo_embalagens_df['Código Cliente'].astype(str)
    numero_cliente = str(numero_cliente).strip()  # Converta e limpe espaços

    # Filtra quantitativo_embalagens_df pelo código do cliente, ou usa '*' se o cliente específico não for encontrado
    filtro_cliente = quantitativo_embalagens_df[quantitativo_embalagens_df['Código Cliente'] == numero_cliente]
    if filtro_cliente.empty:
        filtro_cliente = quantitativo_embalagens_df[quantitativo_embalagens_df['Código Cliente'] == '*']

    # Filtrar por embalageme intervalo de volume
    filtro_final = filtro_cliente[(filtro_cliente['Recipiente'].str.strip() == embalagem) &
                                  (filtro_cliente['Volume inicial'].astype(float) <= volume) &
                                  (filtro_cliente['Volume final'].astype(float) >= volume)]

    if not filtro_final.empty:
        return filtro_final.iloc[0]['Quantitativo Sistema']  # Retorna o primeiro correspondente
    return None  # Retorna None se não houver correspondente

def ajustar_janelas(abrir_fechar):
    todas_janelas = gw.getAllWindows()
    #janela_ie = None

    for janela in todas_janelas:
        # Verifica se a janela é do Internet Explorer
        if "matriz3:57772" in janela.title:
            #janela_ie = janela
            if abrir_fechar == 0:
                janela.maximize()
            else: 
                janela.minimize()
    #    else:
    #        # Minimiza todas as outras janelas
    #        janela.minimize()
    #
    ## Se encontrou a janela do Internet Explorer, maximiza ela
    #if janela_ie:
    #    janela_ie.maximize()
    #else:
    #    print("Janela do Internet Explorer não encontrada.")


def ordenar_pacientes(dados_df):

    dados_df['Nr'] = pd.to_numeric(dados_df['Nr'], errors='coerce')

    # Separando os pacientes com 'Segunda_Ocorrencia' marcada como True e False
    pacientes_segunda_ocorrencia = dados_df[dados_df['Segunda_Ocorrencia']]
    pacientes_primeira_ocorrencia = dados_df[~dados_df['Segunda_Ocorrencia']]
    
    # Ordenando os pacientes sem 'Segunda_Ocorrencia' pela coluna 'Nr'

    pacientes_primeira_ocorrencia = pacientes_primeira_ocorrencia.sort_values(by='Nr')
    
    # Concatenando os dois DataFrames
    dados_df_ordenado = pd.concat([pacientes_primeira_ocorrencia, pacientes_segunda_ocorrencia], ignore_index=True)
    
    return dados_df_ordenado


def main(pacientes_selecionados, espera, caminho_dados, caminho_comum):
    """
    Executa a automação baseada nos parâmetros fornecidos pela interface gráfica.

    :param pacientes_para_cadastro: Lista de pacientes selecionados para cadastro.
    :param pacientes_para_atualizar_leito: Lista de pacientes selecionados para atualização de leito.
    :param espera: Tempo de espera para as operações de automação.
    :param caminho_dados: Caminho para a planilha de dados específica.
    :param caminho_comum: Caminho para a planilha de configuração comum.
    """
    print(pacientes_selecionados)

    # Configuração inicial
    bot = DesktopBot()
    #http://matriz3:57772/csp/homologacao/sneenteral.CSP - Pessoal — Microsoft​ Edge
    abrir_fechar = 0
    ajustar_janelas(abrir_fechar)

    # Variável para os logs finais
    operacoes_logs = {}

    # Preparando os dados com os caminhos fornecidos pela interface
    dados_df, quantitativo_embalagens_df, linhas_com_problemas_df = preparar_dados(caminho_dados, caminho_comum)

    # Obtendo o número do cliente da planilha
    numero_cliente, hora_entrega, data_formatada, nome_cliente  = preparar_cabecalho_cliente(caminho_dados)

    dados_df = marcar_duplicatas(dados_df, ['Paciente', 'CodProduto Sistema', 'Via Adm Sistema', 'Embalagem'])
    print(dados_df[['Paciente', 'Volume (ml)', 'Unidade', 'Nr. Leito', 'Mudou Leito?', 'Dieta', 'Horários', 'Via Adm']])
    
    # Filtrar o DataFrame para incluir apenas as linhas com pacientes selecionados
    dados_df = dados_df[dados_df['Paciente'].isin(pacientes_selecionados)]

    #Criando Df para os que precisam alterar o leito
    pacientes_mudaram_leito = dados_df[dados_df['Mudou Leito?'].astype(str).str.upper() == 'SIM']
    print(pacientes_mudaram_leito['Mudou Leito?'])

    for index, row in pacientes_mudaram_leito.iterrows():
        # Aplicando a função para encontrar o 'Quantitativo Sistema' correspondente para cada linha
        # Assegure-se de que 'quantitativo_embalagens_df' esteja definido e disponível neste escopo
        atualizar_leitos(pacientes_mudaram_leito, index, espera, bot, not_found, numero_cliente, operacoes_logs)     
    
    dados_df = ordenar_pacientes(dados_df)

    # Verificando e abrindo o campo de SOLICITAÇÕES
    verificando_solicitacao(bot, not_found)
  
    primeira_iteracao = True
    for index, row in dados_df.iterrows():
       print(f"Nr do Paciente a ser inserido: {row['Nr']}")
      # Aplicando a função para encontrar o 'Quantitativo Sistema' correspondente para cada linha
       # Assegure-se de que 'quantitativo_embalagens_df' esteja definido e disponível neste escopo
       dados_df['Quantitativo Sistema'] = dados_df.apply(
           lambda row: encontrar_quantitativo(row, quantitativo_embalagens_df, numero_cliente), axis=1) 
       # Puxando a relação Quantitativo Sistema
       quantitativo = dados_df.loc[index, 'Quantitativo Sistema']
       
       print(f"Paciente: {row['Paciente']}, Nr. Atend.: {row['Nr. Atend.']}, Quantitativo Sistema: {quantitativo}, Via Adm Sistema: {row['Via Adm Sistema']}, CodProduto Sistema: {row['CodProduto Sistema']}, Volume: {row['Volume (ml)']}")

       # Ignora a primeira linha, para começar no segundo paciente
       if primeira_iteracao and not dados_df.loc[index, 'Segunda_Ocorrencia']:
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
           primeira_iteracao = False  # Atualiza a variável para garantir que o bloco não seja mais executado

       elif not dados_df.loc[index, 'Segunda_Ocorrencia']:
           
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
       
       else:
           print(f"Paciente: {row['Paciente']}, Segunda Ocorrencia: {row['Segunda_Ocorrencia']}")
           sleep(1)
           verificando_solicitacao(bot, not_found)
           sleep(1)
           inserir_codigo_cliente(bot, numero_cliente, not_found, espera)         
           inserir_codigo_paciente(bot, dados_df, index, not_found, espera, numero_cliente)
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
           


       # Log do progresso
       adicionar_log(operacoes_logs, dados_df.loc[index, 'Paciente'], "Cadastro da Prescrição", dados_df.loc[index, 'Nr'], status = 0)     

    messagebox.showerror("Acabou","A automação chegou ao fim!")
    exibir_logs(operacoes_logs)

    
    
   



if __name__ == '__main__':
    main()
    










