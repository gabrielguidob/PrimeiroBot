##import pyautogui
##
### Obtém a resolução do monitor principal
##largura, altura = pyautogui.size()
##
##print("Largura:", largura, "Altura:", altura)
##
##import pygetwindow as gw
##
##def listar_titulos_janelas():
##    todas_janelas = gw.getAllWindows()
##    print("Títulos das janelas abertas:")
##    for janela in todas_janelas:
##        if janela.title == 'WhatsApp':
##            janela.minimize()
##        if janela.title[:20] == "http://matriz3:57772":
##            #print(janela.title.startswith("http://matriz3:57772"))
##            janela.maximize()
##        print(janela.title)
##
##listar_titulos_janelas()
#
#import pandas as pd
#
#def preparar_dados():
#
#    caminho_comum = '.\Planilha de Configuração.xlsx'
#    caminho_dados = ".\PLANILHA TESTE.xlsx"
#    # Leitura da planilha de dados específica
#    dados_df = pd.read_excel(caminho_dados, skiprows=7, dtype=str)
#
#    # Filtra as linhas onde 'Nr. Atend.' e 'Paciente' são ambos NaN (nulos) ou onde 'Dieta' é 'DIETA ZERO'
#    dados_df = dados_df.dropna(subset=['Nr. Atend.', 'Paciente'], how='all')  # Remove se ambas as colunas forem NaN
#    dados_df = dados_df[dados_df['Dieta'] != 'DIETA ZERO']  # Remove se a dieta for 'DIETA ZERO'
#
#    # Remover colunas que não são necessárias
#    colunas_para_remover = ['N', 'M', 'D', 'E', 'Módulo', 'Quantidade\n(GR ou ML)', 'Apresen-tação', 'Observações Gerais']
#    dados_df = dados_df.drop(columns=colunas_para_remover)
#
#
#    # Leitura das planilhas com caminho comum
#    produtos_df = pd.read_excel(caminho_comum, sheet_name='Produto', dtype=str)
#    via_adm_df = pd.read_excel(caminho_comum, sheet_name='Via Adm')
#
#    produtos_df['Produto Prescrição'] = produtos_df['Produto Prescrição'].str.strip().str.lower()
#    dados_df['Dieta'] = dados_df['Dieta'].str.strip().str.lower()
#    produtos_df['Produto Prescrição'] = produtos_df['Produto Prescrição'].str.strip().str.upper()
#    dados_df['Dieta'] = dados_df['Dieta'].str.strip().str.upper()
#
#
#    # Adicionando a coluna CodProduto Sistema
#    dados_df = pd.merge(dados_df, produtos_df, left_on='Dieta', right_on='Produto Prescrição', how='left')
#    # Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
#    dados_df.drop(columns=['Produto Prescrição'], inplace=True)
#    
#    
#
#    # Adicionando a coluna Via Adm Prescrição
#    dados_df = pd.merge(dados_df, via_adm_df, left_on='Via Adm', right_on='Via Adm Prescrição', how='left')
#    # Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
#    dados_df.drop(columns=['Via Adm Prescrição'], inplace=True)
#
#    # Criando a quantitativo_embalagens_df
#    quantitativo_embalagens_df = pd.read_excel(caminho_comum, sheet_name='Quantitativo Embalagens', dtype=str)
#
#    
#
#
#    # Define colunas para verificar
#    colunas_verificar = ['Nr. Atend.', 'Paciente', 'Unidade', 'Nr. Leito', 'Mudou Leito?', 'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem ', 'CodProduto Sistema', 'Via Adm Sistema']
#    cota_extra_verificar = ['Paciente', 'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem ', 'CodProduto Sistema', 'Via Adm Sistema']
#
#    # Separação de dados
#    cota_extra_df = dados_df[dados_df['Paciente'] == 'COTA EXTRA'].copy()
#    outros_df = dados_df[dados_df['Paciente'] != 'COTA EXTRA'].copy()
#
#    # Identifica linhas com problemas nas colunas especificadas
#    linhas_com_problemas_df = outros_df[outros_df[colunas_verificar].isna().any(axis=1)]
#    linhas_cota_extra_problemas_df = cota_extra_df[cota_extra_df[cota_extra_verificar].isna().any(axis=1)]
#
#    # Aplica filtro para NaN com as colunas apropriadas
#    outros_df.dropna(subset=colunas_verificar, inplace=True)
#    cota_extra_df.dropna(subset=cota_extra_verificar, inplace=True)
#
#    # Combinação de dataframes após limpeza
#    dados_df = pd.concat([cota_extra_df, outros_df])
#
#    # Combina os registros problemáticos para exibição ou log
#    linhas_com_problemas_df = pd.concat([linhas_com_problemas_df, linhas_cota_extra_problemas_df])
#    
#    
#    
#
#    return dados_df, quantitativo_embalagens_df, linhas_com_problemas_df
#
#
#dados_df, quantitativo_embalagens_df, linhas_com_problemas_df = preparar_dados()
#
#print('Linhas com problemas:')
#print(linhas_com_problemas_df)
#print(dados_df[['Paciente', 'Volume (ml)', 'Nr. Leito', 'Mudou Leito?', 'Dieta', 'Horários', 'Via Adm']])
##print(dados_df[['Nr. Atend.', 'Paciente', 'Volume (ml)', 'Unidade', 'Nr. Leito', 'Mudou Leito?', 'Dieta', 'Horários', 'Via Adm', 'Embalagem ', 'CodProduto Sistema', 'Via Adm Sistema']])
#from inserir import inserir_unidade_de_interacao
from bot import not_found
import pandas as pd
from time import sleep
from botcity.core import DesktopBot
import unicodedata

bot = DesktopBot()
caminho_dados = ".\ROYAL.xlsx"
dados_df = pd.read_excel(caminho_dados, skiprows=7, dtype=str)

def preparar_dados(caminho_dados, caminho_comum):

    caminho_comum = '.\Planilha de Configuração.xlsx'
    # Leitura da planilha de dados específica
    dados_df = pd.read_excel(caminho_dados, skiprows=7, dtype=str)
    dados_df = normalize_dataframe(dados_df)

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
    colunas_verificar = ['Nr. Atend.', 'Paciente', 'Nr. Leito', 'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem ', 'CodProduto Sistema', 'Via Adm Sistema']
    cota_extra_verificar = ['Paciente', 'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem ', 'CodProduto Sistema', 'Via Adm Sistema']

    # Separação de dados
    cota_extra_df = dados_df[dados_df['Paciente'] == 'COTA EXTRA'].copy()
    outros_df = dados_df[dados_df['Paciente'] != 'COTA EXTRA'].copy()

    # Identifica linhas com problemas nas colunas especificadas
    linhas_com_problemas_df = outros_df[outros_df[colunas_verificar].isna().any(axis=1)]
    linhas_cota_extra_problemas_df = cota_extra_df[cota_extra_df[cota_extra_verificar].isna().any(axis=1)]

    # Aplica filtro para NaN com as colunas apropriadas
    outros_df.dropna(subset=colunas_verificar, inplace=True)
    cota_extra_df.dropna(subset=cota_extra_verificar, inplace=True)

    # Combinação de dataframes após limpeza
    dados_df = pd.concat([cota_extra_df, outros_df])

    # Combina os registros problemáticos para exibição ou log
    linhas_com_problemas_df = pd.concat([linhas_com_problemas_df, linhas_cota_extra_problemas_df])
    print('Linhas com problemas:')
    print(linhas_com_problemas_df)

    # Normalização dos DataFrames
    



    return dados_df, quantitativo_embalagens_df, linhas_com_problemas_df

def inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found):
    """
    Insere a unidade de internação do paciente na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param dados_df: DataFrame contendo os dados completos, incluindo a unidade de internação.
    :param index: Índice da linha atual no DataFrame.
    :param espera: Tempo de espera (em segundos) após ações de digitação ou clique.
    :param not_found: Função a ser chamada caso o elemento não seja encontrado.
    """
    nome_paciente = dados_df.loc[index, 'Paciente']
    if  nome_paciente == 'COTA EXTRA' or not dados_df.loc[index, 'Unidade']:
        if not bot.find( "No. prescricao", matching=0.97, waiting_time=10000):
            not_found("No. prescricao")
        bot.click_relative(8, 17)
        sleep(0.1 + espera)
        

    else:
        if not bot.find( "unidade de internacao", matching=0.97, waiting_time=10000):
            not_found("unidade de internacao")
        bot.click_relative(37, 17)
        sleep(0.1 + espera)
        bot.click()
        #if not bot.find( "unidade de internacao", matching=0.97, waiting_time=10000):
        #    not_found("unidade de internacao")
        #bot.click_relative(37, 17)
        ##if not bot.find( "Selecione o local de entrega", matching=0.97, waiting_time=10000):
        ##    not_found("Selecione o local de entrega")
        #sleep(0.1 + espera)
        #bot.click()
        #sleep(0.1 + espera)
        unidade_internacao = dados_df.loc[index, 'Unidade']
        print(unidade_internacao)
        bot.kb_type(unidade_internacao)
        if not bot.find( "No. prescricao", matching=0.97, waiting_time=10000):
            not_found("No. prescricao")
        bot.click_relative(8, 17)



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



caminho_comum = ""
dados_df, quantitativo_embalagens_df, linhas_com_problemas_df = preparar_dados(caminho_dados, caminho_comum)


dados_df = normalize_dataframe(dados_df)
index = 0
espera = 0
print(dados_df.loc[index, 'Unidade'])
inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found)