# Importando biblioteca pandas
import pandas as pd

# 2 Leitura do arquivo Excel
caminho_do_arquivo = 'P:\LA VITA\TI\BotCity\Planilha de Dados HOMOLOGAÇÃO 01 - V4.xlsx'
dados_df = pd.read_excel(caminho_do_arquivo, skiprows=2)

#Criando a produtos_df
caminho_do_arquivo_produto = 'P:\LA VITA\TI\BotCity\Planilha de Configuração HOMOLOGAÇÃO 02.xlsx'
produtos_df = pd.read_excel(caminho_do_arquivo_produto, sheet_name='Produto')

#Adicionando a coluna CodProduto Sistema
dados_completos_df = pd.merge(dados_df, produtos_df, left_on='Produto', right_on='Produto Prescrição', how='left')

# Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
dados_completos_df.drop(columns=['Produto Prescrição'], inplace=True)

print(dados_completos_df['CodProduto Sistema'])