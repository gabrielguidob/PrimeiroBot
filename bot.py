# ETAPA 2 - FEITO
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

# ETAPA 3 - FEITO
# Trocar inicio da automatização para clics com o MOUSE FEITO
# 1 - Cod cliente > enter > enter > funcao codigo paciente ate clicar no nome >  enter pop up > (AS VEZES DA ERRO DEPOIS DO PRIMEIRO POP UP)/(AS VEZES VAI PARA O OK POR NADA) > hora pedido > horario de entrega > unidade... > mouse no CRM FEITO
# 2 - funcao codigo paciente ate clicar no nome > (foi para registro hospitalar)/(Precisa percorrer todos os campos antes de unidade) > Unidade... > CRM FEITO


# ETAPA 4 - FEITO
# Alterar na função onde separa os numeros das horas > retirar espaços em branco > as vezes vem 03/09... fazer com q funcione com o zero ou retirar 
# Telas estilo instalar software, avançar/voltar/cancelar
# Primeira tela escolhe a planilha
# Segunda tela: pergunta se existe novos pacientes a serem cadastrados > se sim > rodar função para cadastrar novos pacientes (Arquivo novo bot) 
# Segunda tela: se não > Avançar 
# Terceira tela: existe pacientes para atualizar leito? > Se sim > Mostrar a lista dos Nomes da dados_df dos pacientes com check box para a manipuladora escolher quais pacientes precisa atualizar o leito > rodar função para atualizar os leitos (arquivo novo do bot) > Tentar não mostrar os pacientes que precisam ser cadastrados
# Terceira tela: se não > avançar
# Quarta tela: aviso: sertifique-se que o sistema aporte esteja aberto e tela maximizada e visível + botão rodar/cancelar/rodar + escolher velocidade (rapida como padrao)
# Sequencia para rodar o bot: 1 > função atualizar leito; 2 > função cadastrar paciente; 3 > bot padrão 
# Criar interface de logs

# Etapa 5
"""
FAZER COM QUE SEJA POSSIVEL APENAS ATUALIZAR LEITO OU CADASTRAR PACIENTE SEM SOLICITAR OS PEDIDOS
COMENTAR TODAS AS DEFS NOVAS E ATUALIZAR AS ANTIGAS 
#Ultima letra; Final com " A", " B", etc; Clique relativo > Descrição > Primeira linha DIFICULDADE
"""




# Importações necessárias
from botcity.core import DesktopBot
from botcity.maestro import BotMaestroSDK
import pandas as pd
from openpyxl import load_workbook
import keyboard
from time import sleep
from leito import atualizar_leitos
from cadastrar import cadastrar_pacientes
from log import exibir_logs, adicionar_log
from inserir import (
    verificando_solicitacao, inserir_codigo_cliente, inserir_codigo_paciente,
    inserir_hora, inserir_unidade_de_interacao, inserir_crm_padrao, inserir_produto, inserir_via_adm, inserir_recipiente,
    inserir_volume, inserir_horarios, inserir_quantitativo_embalagens, pop_up_erro, inserir_horario_entrega)


# Desabilita erros se não estiver conectado ao Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def not_found(label):
    """
    Função chamada quando um elemento esperado não é encontrado na interface.
    
    :param label: Rótulo do elemento que não foi encontrado.
    """
    print(f"Elemento não encontrado: {label}")

def ler_numero_cliente(caminho_dados):
    """
    Lê o número do cliente de uma planilha Excel específica.

    :param caminho_dados: Caminho para a planilha de onde o número do cliente será lido.
    :return: Número do cliente como uma string.
    """
    workbook = load_workbook(caminho_dados)
    sheet = workbook.active
    return str(sheet["C1"].value)

def preparar_dados(caminho_dados, caminho_comum):
    """
    Prepara e retorna os DataFrames necessários para a automação a partir das planilhas do Excel.
     caminho_comum
    :param caminho_dados: Caminho para a planilha de dados específica.
    :param caminho_comum: Caminho comum para as planilhas de produtos e via de administração.
    :param caminho_comum: Caminho para a planilha de quantitativo de embalagens.
    """
    # Leitura da planilha de dados específica
    dados_df = pd.read_excel(caminho_dados, skiprows=2, sheet_name='Planilha1')

    # Leitura das planilhas com caminho comum
    produtos_df = pd.read_excel(caminho_comum, sheet_name='Produto')
    via_adm_df = pd.read_excel(caminho_comum, sheet_name='Via Adm')

    # Adicionando a coluna CodProduto Sistema
    dados_df = pd.merge(dados_df, produtos_df, left_on='Produto', right_on='Produto Prescrição', how='left')
    # Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
    dados_df.drop(columns=['Produto Prescrição'], inplace=True)

    # Adicionando a coluna Via Adm Prescrição
    dados_df = pd.merge(dados_df, via_adm_df, left_on='Via Adm', right_on='Via Adm Prescrição', how='left')
    # Após o merge, você pode querer remover a coluna duplicada de 'Produto Prescrição' se não precisar dela
    dados_df.drop(columns=['Via Adm Prescrição'], inplace=True)

    # Criando a quantitativo_embalagens_df
    quantitativo_embalagens_df = pd.read_excel(caminho_comum, sheet_name='Quantitativo Embalagens')

    return dados_df, quantitativo_embalagens_df

def encontrar_quantitativo(row, quantitativo_embalagens_df):
    """
    Encontra o quantitativo sistema correspondente a partir dos dados da linha e da tabela de quantitativo de embalagens.

    :param row: Linha de dados contendo informações sobre recipiente e volume.
    :param quantitativo_embalagens_df: DataFrame contendo informações sobre quantitativo de embalagens.
    :return: O quantitativo sistema correspondente.
    """
    recipiente = row['Recipiente']
    volume = row['Volume']

    # Filtra quantitativo_embalagens_df pelo recipiente e verifica o intervalo de volume
    filtro = quantitativo_embalagens_df[(quantitativo_embalagens_df['Recipiente'] == recipiente) & 
                                        (quantitativo_embalagens_df['Volume inicial'] <= volume) & 
                                        (quantitativo_embalagens_df['Volume final'] >= volume)]

    if not filtro.empty:
        return filtro.iloc[0]['Quantitativo Sistema']  # Retorna o primeiro correspondente
    return None  # Retorna None se não houver correspondente




def main(pacientes_para_cadastro, pacientes_para_atualizar_leito, espera, caminho_dados, caminho_comum):
    """
    Executa a automação baseada nos parâmetros fornecidos pela interface gráfica.

    :param pacientes_para_cadastro: Lista de pacientes selecionados para cadastro.
    :param pacientes_para_atualizar_leito: Lista de pacientes selecionados para atualização de leito.
    :param espera: Tempo de espera para as operações de automação.
    :param caminho_dados: Caminho para a planilha de dados específica.
    :param caminho_comum: Caminho para a planilha de configuração comum.
    """

    # Configuração inicial
    bot = DesktopBot()

    # Variável para os logs finais
    operacoes_logs = {}

    # Preparando os dados com os caminhos fornecidos pela interface
    dados_df, quantitativo_embalagens_df = preparar_dados(caminho_dados, caminho_comum)

    # Obtendo o número do cliente da planilha
    num_cliente = ler_numero_cliente(caminho_dados)

    # Se houver pacientes para cadastro, chama a função de cadastro
    if pacientes_para_cadastro:
        cadastrar_pacientes(pacientes_para_cadastro, espera, dados_df, bot, not_found, num_cliente, operacoes_logs)

    # Se houver pacientes para atualizar leito, chama a função de atualização de leito
    if pacientes_para_atualizar_leito:
        atualizar_leitos(pacientes_para_atualizar_leito, espera, dados_df, bot, not_found, num_cliente, operacoes_logs)



    # Aplicando a função para encontrar o 'Quantitativo Sistema' correspondente para cada linha
    dados_df['Quantitativo Sistema'] = dados_df.apply(encontrar_quantitativo, quantitativo_embalagens_df = quantitativo_embalagens_df, axis=1)

    # Verificando e abrindo o campo de SOLICITAÇÕES]
    verificando_solicitacao(bot, not_found)
    

    for index, row in dados_df.iterrows():
       # Variavel para testes
       passo_a_passo = False

       # Puxando a relação Quantitativo Sistema
       quantitativo = row['Quantitativo Sistema']

       # Ignora a primeira linha, para começar no segundo paciente
       if index == 0:

           inserir_codigo_cliente(bot, num_cliente, not_found, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 1")
                keyboard.wait('ctrl')


           inserir_codigo_paciente(bot, dados_df, index, not_found, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 2")
                keyboard.wait('ctrl')


           #Proximo enter fecha o popup
           sleep(1)
           bot.enter()

           pop_up_erro(bot, not_found)

            # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 3")
                keyboard.wait('ctrl')

                #sleep(1)
           inserir_horario_entrega(bot, not_found, espera)     
           inserir_hora(bot, espera, not_found, index)

           pop_up_erro(bot, not_found)

           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 4")
                keyboard.wait('ctrl')

           inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 5")
                keyboard.wait('ctrl')

           inserir_crm_padrao(bot, espera, not_found)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 6")
                keyboard.wait('ctrl')

           inserir_produto(bot, dados_df, index, espera)
           inserir_via_adm(bot, dados_df, index, espera)
           inserir_recipiente(bot, dados_df, index, espera)
           inserir_volume(bot, dados_df, index, espera)
           inserir_horarios(bot, dados_df, index, not_found, espera)
           inserir_quantitativo_embalagens(bot, quantitativo, not_found, espera)

           

       else:
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 1")
                keyboard.wait('ctrl')

           inserir_codigo_paciente(bot, dados_df, index, not_found, espera)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 2")
                keyboard.wait('ctrl')

           pop_up_erro(bot, not_found)

           inserir_hora(bot, espera, not_found, index)

           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 4")
                keyboard.wait('ctrl')

           inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 3")
                keyboard.wait('ctrl')

           inserir_crm_padrao(bot, espera, not_found)
           # Aguarda tecla para continuar, se solicitado
           if passo_a_passo:
                print("APERTA A TECLA KRAI 4")
                keyboard.wait('ctrl')

           inserir_produto(bot, dados_df, index, espera)
           inserir_via_adm(bot, dados_df, index, espera)
           inserir_recipiente(bot, dados_df, index, espera)
           inserir_volume(bot, dados_df, index, espera)
           inserir_horarios(bot, dados_df, index, not_found, espera)
           inserir_quantitativo_embalagens(bot, quantitativo, not_found, espera)
       
       # Log do progresso
       adicionar_log(operacoes_logs, dados_df.loc[index, 'Nome'], "Solicitado")

       
       
    exibir_logs(operacoes_logs)


if __name__ == '__main__':
    main()
    










