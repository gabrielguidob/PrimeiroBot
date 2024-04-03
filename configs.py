# Importando biblioteca pandas
import pandas as pd

# 2 Leitura do arquivo Excel
caminho_do_arquivo = 'P:\LA VITA\TI\BotCity\Planilha de Dados HOMOLOGAÇÃO 01 - V4.xlsx'
dados_df = pd.read_excel(caminho_do_arquivo, skiprows=2)

#Criando a produtos_df
caminho_do_arquivo_produto = 'P:\LA VITA\TI\BotCity\Planilha de Configuração HOMOLOGAÇÃO 02.xlsx'
produtos_df = pd.read_excel(caminho_do_arquivo_produto, sheet_name='Produto')

#Criando a via_adm_df
caminho_do_arquivo_via_adm = 'P:\LA VITA\TI\BotCity\Planilha de Configuração HOMOLOGAÇÃO 02.xlsx'
via_adm_df = pd.read_excel(caminho_do_arquivo_via_adm, sheet_name='Via Adm')

#Adicionando a coluna CodProduto Sistema
dados_produtos_df = pd.merge(dados_df, produtos_df, left_on='Produto', right_on='Produto Prescrição', how='left')

# Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
dados_produtos_df.drop(columns=['Produto Prescrição'], inplace=True)

#Adicionando a coluna ViaAdm Sistema
dados_completos2_df = pd.merge(dados_df, via_adm_df, left_on='Via Adm', right_on='Via Adm Prescrição', how='left')

# Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
dados_completos2_df.drop(columns=['Via Adm Prescrição'], inplace=True)


#Criando a quantitativo_embalagens_df
caminho_do_arquivo_quantitativo_embalagens = 'P:\LA VITA\TI\BotCity\Planilha de Configuração HOMOLOGAÇÃO 02.xlsx'
quantitativo_embalagens_df = pd.read_excel(caminho_do_arquivo_quantitativo_embalagens, sheet_name='Quantitativo Embalagens')



def encontrar_quantitativo(row):
    recipiente = row['Recipiente']
    volume = row['Volume']
    
    # Filtra quantitativo_df pelo recipiente e verifica o intervalo de volume
    filtro = quantitativo_embalagens_df[(quantitativo_embalagens_df['Recipiente'] == recipiente) & (quantitativo_embalagens_df['Volume inicial'] <= volume) & (quantitativo_embalagens_df['Volume final'] >= volume)]
    
    if not filtro.empty:
        return filtro.iloc[0]['Quantitativo Sistema']  # Retorna o primeiro correspondente
    return None  # Retorna None se não houver correspondente

# Aplica a função a cada linha de dados_df para encontrar o quantitativo sistema correspondente
dados_completos2_df['Quantitativo Sistema'] = dados_completos2_df.apply(encontrar_quantitativo, axis=1)



#print(dados_completos2_df)
print(dados_completos2_df.drop(['Nome', 'Un. Internação', 'Volume', 'Horários', 'Via Adm'], axis=1))
print(dados_produtos_df['CodProduto Sistema'])
print(produtos_df)