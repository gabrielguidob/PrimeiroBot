#import pyautogui
#
## Obtém a resolução do monitor principal
#largura, altura = pyautogui.size()
#
#print("Largura:", largura, "Altura:", altura)
#
#import pygetwindow as gw
#
#def listar_titulos_janelas():
#    todas_janelas = gw.getAllWindows()
#    print("Títulos das janelas abertas:")
#    for janela in todas_janelas:
#        if janela.title == 'WhatsApp':
#            janela.minimize()
#        if janela.title[:20] == "http://matriz3:57772":
#            #print(janela.title.startswith("http://matriz3:57772"))
#            janela.maximize()
#        print(janela.title)
#
#listar_titulos_janelas()

import pandas as pd

def preparar_dados():

    caminho_comum = '.\Planilha de Configuração.xlsx'
    caminho_dados = ".\PLANILHA TESTE.xlsx"
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
    
    

    # Adicionando a coluna Via Adm Prescrição
    dados_df = pd.merge(dados_df, via_adm_df, left_on='Via Adm', right_on='Via Adm Prescrição', how='left')
    # Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
    dados_df.drop(columns=['Via Adm Prescrição'], inplace=True)

    # Criando a quantitativo_embalagens_df
    quantitativo_embalagens_df = pd.read_excel(caminho_comum, sheet_name='Quantitativo Embalagens', dtype=str)

    


    # Define colunas para verificar
    colunas_verificar = ['Nr. Atend.', 'Paciente', 'Unidade', 'Nr. Leito', 'Mudou Leito?', 'Dieta', 'Volume (ml)', 'Horários', 'Via Adm', 'Embalagem ', 'CodProduto Sistema', 'Via Adm Sistema']
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
    
    
    

    return dados_df, quantitativo_embalagens_df, linhas_com_problemas_df


dados_df, quantitativo_embalagens_df, linhas_com_problemas_df = preparar_dados()

print('Linhas com problemas:')
print(linhas_com_problemas_df)
print(dados_df[['Paciente', 'Volume (ml)', 'Nr. Leito', 'Mudou Leito?', 'Dieta', 'Horários', 'Via Adm']])
#print(dados_df[['Nr. Atend.', 'Paciente', 'Volume (ml)', 'Unidade', 'Nr. Leito', 'Mudou Leito?', 'Dieta', 'Horários', 'Via Adm', 'Embalagem ', 'CodProduto Sistema', 'Via Adm Sistema']])
