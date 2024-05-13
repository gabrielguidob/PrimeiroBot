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
from inserir import (
    verificando_solicitacao, inserir_codigo_cliente, inserir_codigo_paciente,
    inserir_hora, inserir_unidade_de_interacao, inserir_crm_padrao, inserir_produto, inserir_via_adm, inserir_recipiente,
    inserir_volume, inserir_horarios, inserir_quantitativo_embalagens, pop_up_erro, inserir_horario_entrega, encontrar_mensagem_cadastrar_paciente)


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

    # Converte data_pedido para datetime se não estiver no formato correto
    if not isinstance(data_pedido, datetime):
        # Assume que data_pedido é uma string no formato 'yyyy-mm-dd HH:MM:SS'
        data_pedido = datetime.strptime(data_pedido, "%Y-%m-%d %H:%M:%S")

    # Formata a data no formato 'dd/mm/yyyy'
    data_formatada = data_pedido.strftime('%d/%m/%Y')

    return numero_cliente, hora_entrega, data_formatada, nome_cliente

def preparar_dados(caminho_dados, caminho_comum):

    caminho_comum = 'P:/LA VITA/TI/BotCity/Planilha de Configuração HOMOLOGAÇÃO 03.xlsx'
    # Leitura da planilha de dados específica
    dados_df = pd.read_excel(caminho_dados, skiprows=7, dtype=str)

    # Filtra as linhas onde 'Nr. Atend.' e 'Paciente' são ambos NaN (nulos) ou onde 'Dieta' é 'DIETA ZERO'
    dados_df = dados_df.dropna(subset=['Nr. Atend.', 'Paciente'], how='all')  # Remove se ambas as colunas forem NaN
    dados_df = dados_df[dados_df['Dieta'] != 'DIETA ZERO']  # Remove se a dieta for 'DIETA ZERO'

    # Remover colunas que não são necessárias
    colunas_para_remover = ['N', 'M', 'D', 'E', 'Módulo', 'Quantidade\n(GR ou ML)', 'Apresen-tação', 'Observações Gerais']
    dados_df = dados_df.drop(columns=colunas_para_remover)


    # Leitura das planilhas com caminho comum
    produtos_df = pd.read_excel(caminho_comum, sheet_name='Produto', dtype=str)
    via_adm_df = pd.read_excel(caminho_comum, sheet_name='Via Adm')

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

    print(dados_df['Dieta'])

    # Separa dados de "COTA EXTRA"
    cota_extra_df = dados_df[dados_df['Paciente'] == 'COTA EXTRA'].copy()
    outros_df = dados_df[dados_df['Paciente'] != 'COTA EXTRA'].copy()

    # Filtra linhas com NaN nas colunas especificadas, exceto para "COTA EXTRA"
    colunas_verificar = ['Nr. Atend.', 'Paciente', 'Unidade', 'Nr. Leito', 'Mudou Leito?', 'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem ', 'CodProduto Sistema', 'Via Adm Sistema']
    cota_extra_verificar = ['Paciente', 'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem ', 'CodProduto Sistema', 'Via Adm Sistema']

    # Identificar linhas com problemas antes de aplicar dropna
    linhas_com_problemas_df = outros_df[outros_df.isna().any(axis=1)]
    linhas_cota_extra_problemas_df = cota_extra_df[cota_extra_df.isna().any(axis=1)]

    # Aplica filtros para NaN
    outros_df.dropna(subset=colunas_verificar, inplace=True)
    cota_extra_df.dropna(subset=cota_extra_verificar, inplace=True)

    # Combina os dados novamente
    dados_df = pd.concat([cota_extra_df, outros_df])
    

    linhas_com_problemas_df = pd.concat([linhas_com_problemas_df, linhas_cota_extra_problemas_df])
    print(dados_df)
    print('Linhas com problemas:')
    print(linhas_com_problemas_df)

    return dados_df, quantitativo_embalagens_df, linhas_com_problemas_df

def encontrar_quantitativo(row, quantitativo_embalagens_df, numero_cliente):
    embalagem = row['Embalagem '].strip().upper()  # Certifique-se de remover espaços extras
    volume = float(row['Volume (ml)'])

    # Certifique-se de que os tipos de dados para comparação sejam apropriados
    quantitativo_embalagens_df['Código Cliente'] = quantitativo_embalagens_df['Código Cliente'].astype(str)
    numero_cliente = str(numero_cliente).strip()  # Converta e limpe espaços

    # Filtra quantitativo_embalagens_df pelo código do cliente, ou usa '*' se o cliente específico não for encontrado
    filtro_cliente = quantitativo_embalagens_df[quantitativo_embalagens_df['Código Cliente'] == numero_cliente]
    if filtro_cliente.empty:
        filtro_cliente = quantitativo_embalagens_df[quantitativo_embalagens_df['Código Cliente'] == '*']

    # Filtrar por embalagem e intervalo de volume
    filtro_final = filtro_cliente[(filtro_cliente['Recipiente'].str.strip() == embalagem) &
                                  (filtro_cliente['Volume inicial'].astype(float) <= volume) &
                                  (filtro_cliente['Volume final'].astype(float) >= volume)]

    if not filtro_final.empty:
        return filtro_final.iloc[0]['Quantitativo Sistema']  # Retorna o primeiro correspondente
    return None  # Retorna None se não houver correspondente




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

    # Variável para os logs finais
    operacoes_logs = {}

    # Preparando os dados com os caminhos fornecidos pela interface
    dados_df, quantitativo_embalagens_df, linhas_com_problemas_df = preparar_dados(caminho_dados, caminho_comum)

    # Obtendo o número do cliente da planilha
    numero_cliente, hora_entrega, data_formatada, nome_cliente  = preparar_cabecalho_cliente(caminho_dados)

    # Filtrar o DataFrame para incluir apenas as linhas com pacientes selecionados
    dados_df = dados_df[dados_df['Paciente'].isin(pacientes_selecionados)]

    #Criando Df para os que precisam alterar o leito
    pacientes_mudaram_leito = dados_df[dados_df['Mudou Leito?'] == 'Sim']
    print(pacientes_mudaram_leito['Mudou Leito?'])
    for index, row in pacientes_mudaram_leito.iterrows():
        # Aplicando a função para encontrar o 'Quantitativo Sistema' correspondente para cada linha
        # Assegure-se de que 'quantitativo_embalagens_df' esteja definido e disponível neste escopo
        atualizar_leitos(pacientes_mudaram_leito, index, espera, bot, not_found, numero_cliente, operacoes_logs)
         
    # Verificando e abrindo o campo de SOLICITAÇÕES
    verificando_solicitacao(bot, not_found)
  
    for index, row in dados_df.iterrows():

      # Aplicando a função para encontrar o 'Quantitativo Sistema' correspondente para cada linha
       # Assegure-se de que 'quantitativo_embalagens_df' esteja definido e disponível neste escopo
       dados_df['Quantitativo Sistema'] = dados_df.apply(
           lambda row: encontrar_quantitativo(row, quantitativo_embalagens_df, numero_cliente), axis=1) 
       # Puxando a relação Quantitativo Sistema
       quantitativo = dados_df.loc[index, 'Quantitativo Sistema']
       
       print(f"Paciente: {row['Paciente']}, Nr. Atend.: {row['Nr. Atend.']}, Quantitativo Sistema: {quantitativo}, Via Adm Sistema: {row['Via Adm Sistema']}, CodProduto Sistema: {row['CodProduto Sistema']}")

       # Ignora a primeira linha, para começar no segundo paciente
       if (index == 0):

           inserir_codigo_cliente(bot, numero_cliente, not_found, espera)
           
           inserir_codigo_paciente(bot, dados_df, index, not_found, espera, numero_cliente)
           encontrar_mensagem_cadastrar_paciente(index, espera, dados_df, bot, not_found, operacoes_logs)
           sleep(1)
           bot.enter()
           pop_up_erro(bot, not_found)                       
           inserir_horario_entrega(bot, not_found, espera, hora_entrega)     
           inserir_hora(bot, espera, not_found, index, hora_entrega)
           pop_up_erro(bot, not_found)           
           inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found)           
           inserir_crm_padrao(bot, espera, not_found)
           inserir_produto(bot, dados_df, index, espera)
           inserir_via_adm(bot, dados_df, index, espera)
           inserir_recipiente(bot, dados_df, index, espera)
           inserir_volume(bot, dados_df, index, espera)
           inserir_horarios(bot, dados_df, index, not_found, espera)
           inserir_quantitativo_embalagens(bot, quantitativo, not_found, espera)

       else:   
           
           inserir_codigo_paciente(bot, dados_df, index, not_found, espera, numero_cliente)
           encontrar_mensagem_cadastrar_paciente(index, espera, dados_df, bot, not_found, operacoes_logs)
           pop_up_erro(bot, not_found)
           inserir_hora(bot, espera, not_found, index, hora_entrega)
           inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found)
           inserir_crm_padrao(bot, espera, not_found)
           inserir_produto(bot, dados_df, index, espera)
           inserir_via_adm(bot, dados_df, index, espera)
           inserir_recipiente(bot, dados_df, index, espera)
           inserir_volume(bot, dados_df, index, espera)
           inserir_horarios(bot, dados_df, index, not_found, espera)
           inserir_quantitativo_embalagens(bot, quantitativo, not_found, espera)
       
       # Log do progresso
       adicionar_log(operacoes_logs, dados_df.loc[index, 'Paciente'], "Cadastro da Prescrição")     
       
    exibir_logs(operacoes_logs)


if __name__ == '__main__':
    main()
    










