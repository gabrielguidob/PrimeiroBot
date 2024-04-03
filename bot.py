#Criar repositorio no GitHub FEITO
#Separar tudo em funções FEITO
#Implementar abrir solicitações/solicitações de dietas FEITO
#Incluir primeiro pedido dentro do for quando o index == 0 FEITO
#Para buscar nome do paciente: Tecla F2 para abrir; FEITO
#Para o produto: Criar um de para com a outra tabela referencia FEITO
#Para a Via Adm: Criar um de para com a outra tabela referencia FEITO
#Para Quantitativo de embalagens: Criar um de para com a outra tabela referencia + Condições de Volume/Recipiente FEITO
#Baixar o plugin BotCity no vscode
#Ultima letra; Final com " A", " B", etc; Clique relativo > Descrição > Primeira linha DIFICULDADE

# ETAPA 3
# Trocar inicio da automatização para clics com o MOUSE 
# 1 - Cod cliente > enter > enter > funcao codigo paciente ate clicar no nome >  enter pop up > (AS VEZES DA ERRO DEPOIS DO PRIMEIRO POP UP)/(AS VEZES VAI PARA O OK POR NADA) > hora pedido > horario de entrega > unidade... > mouse no CRM
# 2 - funcao codigo paciente ate clicar no nome > (foi para registro hospitalar)/(Precisa percorrer todos os campos antes de unidade) > Unidade... > CRM

# Import for the Desktop Bot
from botcity.core import DesktopBot

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Importando biblioteca pandas
import pandas as pd

# Importando biblioteca Openpyxl
from openpyxl import Workbook, load_workbook


import keyboard

from inserir import verificando_solicitacao, inserir_codigo_cliente, inserir_codigo_paciente, inserir_hora, inserir_unidade_de_interacao, inserir_unidade_de_interacao2, inserir_crm_padrao, inserir_produto, inserir_via_adm, inserir_recipiente, inserir_volume, inserir_horarios,  inserir_quantitativo_embalagens

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():

    espera = int(input('Tempo de espera: '))

    bot = DesktopBot()


    verificando_solicitacao(bot, not_found)
    
    # 1 Leitura do arquivo Excel + variavel Num do Cliente
    planilha = load_workbook ('P:\LA VITA\TI\BotCity\Planilha de Dados HOMOLOGAÇÃO 01 - V4.xlsx')
    aba_ativa = planilha.active
    num_cliente = str(aba_ativa["C1"].value) 


    # 2 Leitura do arquivo Excel
    caminho_do_arquivo = 'P:\LA VITA\TI\BotCity\Planilha de Dados HOMOLOGAÇÃO 02.xlsx'
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

    #Adicionando a coluna Via Adm Prescrição
    dados_completos_df = pd.merge(dados_df, via_adm_df, left_on='Via Adm', right_on='Via Adm Prescrição', how='left')
    # Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
    dados_completos_df.drop(columns=['Via Adm Prescrição'], inplace=True)


    #Criando a quantitativo_embalagens_df
    caminho_do_arquivo_quantitativo_embalagens = 'P:\LA VITA\TI\BotCity\Planilha de Configuração HOMOLOGAÇÃO 02.xlsx'
    quantitativo_embalagens_df = pd.read_excel(caminho_do_arquivo_quantitativo_embalagens, sheet_name='Quantitativo Embalagens')


    passo_a_passo = True


    def encontrar_quantitativo(row):
        recipiente = row['Recipiente']
        volume = row['Volume']

        # Filtra quantitativo_df pelo recipiente e verifica o intervalo de volume
        filtro = quantitativo_embalagens_df[(quantitativo_embalagens_df['Recipiente'] == recipiente) & (quantitativo_embalagens_df['Volume inicial'] <= volume) & (quantitativo_embalagens_df['Volume final'] >= volume)]

        if not filtro.empty:
            return filtro.iloc[0]['Quantitativo Sistema']  # Retorna o primeiro correspondente
        return None  # Retorna None se não houver correspondente

    # Aplica a função a cada linha de dados_df para encontrar o quantitativo sistema correspondente
    dados_completos_df['Quantitativo Sistema'] = dados_completos_df.apply(encontrar_quantitativo, axis=1)


    #Inicio do FOR para cadastrar do segundo paciente em diante
    for index, row in dados_completos_df.iterrows():
       # Ignora a primeira linha, para começar no segundo paciente
       if index == 0:

           inserir_codigo_cliente(bot, num_cliente, not_found, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 1")
                keyboard.wait('ctrl')


           inserir_codigo_paciente(bot, dados_completos_df, index, not_found, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 2")
                keyboard.wait('ctrl')


           #Proximo enter fecha o popup
           bot.enter()
           #bot.enter()
            # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 3")
                keyboard.wait('ctrl')

                #sleep(1)
           inserir_hora(bot, espera)
           #bot.enter()
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 4")
                keyboard.wait('ctrl')

           inserir_unidade_de_interacao(bot, dados_completos_df, index, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 5")
                keyboard.wait('ctrl')

           inserir_crm_padrao(bot, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 6")
                keyboard.wait('ctrl')

           inserir_produto(bot, dados_produtos_df, index, espera)
           inserir_via_adm(bot, dados_completos_df, index)
           inserir_recipiente(bot, dados_completos_df, index)
           inserir_volume(bot, dados_completos_df, index)
           inserir_horarios(bot, dados_completos_df, index, not_found)
           inserir_quantitativo_embalagens(bot, dados_completos_df, index, not_found)

       else:
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 1")
                keyboard.wait('ctrl')

           inserir_codigo_paciente(bot, dados_completos_df, index, not_found, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 2")
                keyboard.wait('ctrl')

                #bot.enter()
           #sleep(1)
           #inserir_hora(bot)
           inserir_unidade_de_interacao2(bot, dados_completos_df, index, not_found, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 3")
                keyboard.wait('ctrl')

           inserir_crm_padrao(bot, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 4")
                keyboard.wait('ctrl')

           inserir_produto(bot, dados_produtos_df, index, espera)
           inserir_via_adm(bot, dados_completos_df, index)
           inserir_recipiente(bot, dados_completos_df, index)
           inserir_volume(bot, dados_completos_df, index)
           inserir_horarios(bot, dados_completos_df, index, not_found)
           inserir_quantitativo_embalagens(bot, dados_completos_df, index, not_found)    
       
       print(index)
       





def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()










