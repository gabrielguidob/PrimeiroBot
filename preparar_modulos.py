import pandas as pd
from bot import *

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
    colunas_para_remover = ['N', 'M', 'D', 'E', 'Observações Gerais']
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


    # Criação da coluna temporária 'Produto_Prescricao_Temp' usando 'Dieta' ou 'Módulo'
    dados_df['Produto_Prescricao_Temp'] = dados_df['Dieta'].combine_first(dados_df['Módulo'])

    # Fazendo o merge com a nova coluna temporária
    dados_df = pd.merge(dados_df, produtos_df, left_on='Produto_Prescricao_Temp', right_on='Produto Prescrição', how='left')

    # Removendo as colunas duplicadas e a coluna temporária
    dados_df.drop(columns=['Produto Prescrição', 'Produto_Prescricao_Temp'], inplace=True)

    
    print(dados_df.isnull().sum())  # Isso mostrará a quantidade de NaNs em cada coluna após o merge.

    # Adicionando a coluna Via Adm Prescrição
    dados_df = pd.merge(dados_df, via_adm_df, left_on='Via Adm', right_on='Via Adm Prescrição', how='left')
    # Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
    dados_df.drop(columns=['Via Adm Prescrição'], inplace=True)

    # Criando a quantitativo_embalagens_df
    quantitativo_embalagens_df = pd.read_excel(caminho_comum, sheet_name='Quantitativo Embalagens Módulos', dtype=str)

    quantitativo_embalagens_df = normalize_dataframe(quantitativo_embalagens_df)

    print(dados_df['Dieta'])


    print(f'DADOS DF {dados_df}')
    print(f'DADOS COLUNAS {dados_df.columns}')


    # Define condições para linhas com problemas
    problemas = (
        (dados_df['Apresen-tação'].notna() & (dados_df['Módulo'].isna() | dados_df['Quantidade\n(GR ou ML)'].isna())) |
        (dados_df['Embalagem'].isna()) |
        ((dados_df['Apresen-tação'] == 'M') & (dados_df['Dieta'].isna() | dados_df['Volume (ml)'].isna()))
    )

    # Adiciona uma coluna indicando se a linha tem problemas
    dados_df['Tem Problema'] = problemas

    # Processamento adicional para casos especiais com Apresen-tação == 'Ad ↑'
    for i in range(1, len(dados_df)):
        if dados_df.loc[i, 'Apresen-tação'] == 'Ad ↑':
            # A linha com 'Ad ↑' herda o problema da linha anterior
            if dados_df.loc[i-1, 'Tem Problema']:
                dados_df.loc[i, 'Tem Problema'] = True
            # A linha com 'Ad ↑' deve ter os mesmos valores de 'Nr. Atend.' e 'Paciente' que a linha anterior
            if dados_df.loc[i, 'Nr. Atend.'] != dados_df.loc[i-1, 'Nr. Atend.'] or dados_df.loc[i, 'Paciente'] != dados_df.loc[i-1, 'Paciente']:
                dados_df.loc[i, 'Tem Problema'] = True

    # Separar linhas com problemas
    linhas_com_problemas_df = dados_df[dados_df['Tem Problema']].copy()
    dados_df = dados_df[~dados_df['Tem Problema']].copy()

    # Remover a coluna de marcação de problemas
    linhas_com_problemas_df.drop(columns=['Tem Problema'], inplace=True)
    dados_df.drop(columns=['Tem Problema'], inplace=True)

    # Separar o DataFrame em três partes
    modulos_df = dados_df[dados_df['Apresen-tação'].isin(['MA', 'S', 'Ad ↑'])].copy()
    suplementos_df = dados_df[dados_df['Apresen-tação'].isna()].copy()
    modulos_dietas_df = dados_df[dados_df['Apresen-tação'] == 'M'].copy()

    # Adiciona uma nova coluna identificando o grupo
    modulos_df['Grupo'] = 'Módulos'
    suplementos_df['Grupo'] = 'Suplementos'
    modulos_dietas_df['Grupo'] = 'Módulos em Dietas'

    # Recombinar os DataFrames na sequência requisitada
    dados_df_final = pd.concat([modulos_df, suplementos_df, modulos_dietas_df], ignore_index=True)


    # Realizar as alterações finais nas colunas
    dados_df_final.loc[dados_df_final['Grupo'] == 'Módulos', 'CodProduto Sistema'] = 999
    dados_df_final.loc[(dados_df_final['Grupo'] == 'Módulos') & (dados_df_final['Apresen-tação'] == 'S'), 'Volume (ml)'] = 0

    # Atualizar a coluna Embalagem
    dados_df_final.loc[dados_df_final['Embalagem'] == 'Original do produto', 'Embalagem'] = 'Separado'
    
    # Exibe o DataFrame final
    print(dados_df_final)

    # Exibe o DataFrame de linhas com problemas
    print(linhas_com_problemas_df)



    return dados_df_final, quantitativo_embalagens_df, linhas_com_problemas_df