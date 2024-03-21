#Criar repositorio no GitHub
#Separar tudo em funções
#Implementar abrir solicitações/solicitações de dietas
#Para buscar nome do paciente: Tecla F2 para abrir; Ultima letra; Final com " A", " B", etc; Clique relativo > Descrição > Primeira linha
#Para o produto: Criar um de para com a outra tabela referencia 
#Para a Via Adm: Criar um de para com a outra tabela referencia 
#Para Quantitativo de embalagens: Criar um de para com a outra tabela referencia + Condições de Volume/Recipiente
#Baixar o plugin BotCity no vscode
#Incluir primeiro pedido dentro do for quando o index == 0

# Import for the Desktop Bot
from botcity.core import DesktopBot

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Importando biblioteca pandas
import pandas as pd

# Importando biblioteca Openpyxl
from openpyxl import Workbook, load_workbook

#Importando arquivo horas.py
from horas import executar_acoes

from time import sleep

#Importando datetime
from datetime import datetime

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():

    bot = DesktopBot()

    # 1 Leitura do arquivo Excel + variavel Num do Cliente
    planilha = load_workbook ('P:\LA VITA\TI\BotCity\Planilha de Dados HOMOLOGAÇÃO 01.xlsx')

    aba_ativa = planilha.active

    num_cliente = str(aba_ativa["C1"].value) 


    # 2 Leitura do arquivo Excel
    caminho_do_arquivo = 'P:\LA VITA\TI\BotCity\Planilha de Dados HOMOLOGAÇÃO 01.xlsx'
    dados_df = pd.read_excel(caminho_do_arquivo, skiprows=2)


    #Pegando hora atual e modificando
    hora_atual = datetime.now()
    hora_formatada = hora_atual.strftime("%H%M")

    if not bot.find( "Codigo Cliente", matching=0.97, waiting_time=10000):
        not_found("Codigo Cliente")
    bot.click_relative(23, 33)

    # Codigo Cliente
    bot.kb_type(num_cliente)
    bot.enter()
    bot.enter()

    # Codigo Paciente
    bot.kb_type(str(dados_df.loc[0, 'Nome']))
    bot.enter()
    bot.enter()

    # Horario Sistema 
    # IMPLEMENTAR FUNÇAO QUE BUSCA HORA DE AGORA
    bot.kb_type(hora_formatada)
    bot.enter()
    bot.enter()
    bot.enter()
    sleep(0.1)

    # Unidade de internação
    bot.kb_type(dados_df.loc[0, 'Un. Internação'])
    sleep(0.1)
    bot.enter()

    # Entrar com CRM padrão
    bot.kb_type("9574")
    bot.enter()
    bot.enter()

    # Produto 
    bot.kb_type(str(dados_df.loc[0, 'Produto']))
    bot.enter()

    # Via ADM
    bot.kb_type(dados_df.loc[0, 'Via Adm'])
    bot.enter()

    # Recipiente
    bot.kb_type(dados_df.loc[0, 'Recipiente'])
    bot.enter()

    # Volume 
    bot.kb_type(str(dados_df.loc[0, 'Volume']))
    bot.enter()
    
    # Escolha de Horários
    bot.kb_type("0")
    bot.enter()
    bot.kb_type("0")
    bot.enter()
    if not bot.find( "0 Hora", matching=0.97, waiting_time=10000):
        not_found("0 Hora")
    bot.click_relative(7, 8)

    #Separando e marcando os horários
    hora = dados_df.loc[0, 'Horários']
    hora_separada = hora.split('/')
    hora_separada = [int(h) for h in hora_separada]
    executar_acoes(bot, hora_separada)

     # Achando e Escrevendo Quantitativo de embalagens
    if not bot.find( "Quantitativo de embalagens", matching=0.97, waiting_time=10000):
         not_found("Quantitativo de embalagens")
    bot.click_relative(12, 46)

    if not bot.find( "Escolha uma opcao", matching=0.97, waiting_time=10000):
        not_found("Escolha uma opcao")
    bot.click_relative(242, 7)
    #Segundo CLick se mostrou necessário neste tipo de campo de informação
    bot.click()

    bot.kb_type(dados_df.loc[0, 'Quantidade de embalagens'])
    bot.enter()
    bot.enter()

    #print(dados_df)
    
    #Inicio do FOR para cadastrar do segundo paciente em diante
    
    for index, row in dados_df.iterrows():
       # Ignora a primeira linha, para começar no segundo paciente
       if index == 0:
           continue
       
       # Inicio do cadastro
       # Codigo Paciente
       bot.kb_type(str(dados_df.loc[index, 'Nome']))
       bot.enter()
       bot.enter()

       # Horario Sistema 
       # IMPLEMENTAR FUNÇAO QUE BUSCA HORA DE AGORA
       bot.kb_type(hora_formatada)
       bot.enter()
       bot.enter()
       bot.enter()

       # Unidade de internação
       bot.kb_type(dados_df.loc[index, 'Un. Internação'])
       bot.enter()

       # Entrar com CRM padrão
       bot.kb_type("9574")
       bot.enter()
       bot.enter()

       # Produto 
       bot.kb_type(str(dados_df.loc[index, 'Produto']))
       bot.enter()

       # Via ADM
       bot.kb_type(dados_df.loc[index, 'Via Adm'])
       bot.enter()

       # Recipiente
       bot.kb_type(dados_df.loc[index, 'Recipiente'])
       bot.enter()

       # Volume 
       bot.kb_type(str(dados_df.loc[index, 'Volume']))
       bot.enter()
    
       
       # Escolha de Horários
       bot.kb_type("0")
       bot.enter()
       bot.kb_type("0")
       bot.enter()
       if not bot.find( "0 Hora", matching=0.97, waiting_time=10000):
           not_found("0 Hora")
       bot.click_relative(7, 8)

       #Separando e marcando os horários
       hora = dados_df.loc[index, 'Horários']
       hora_separada = hora.split('/')
       hora_separada = [int(h) for h in hora_separada]
       #print(hora_separada)
       executar_acoes(bot, hora_separada)

       # Achando e Escrevendo Quantitativo de embalagens
       if not bot.find( "Quantitativo de embalagens", matching=0.97, waiting_time=10000):
           not_found("Quantitativo de embalagens")
       bot.click_relative(12, 46)

       if not bot.find( "Escolha uma opcao", matching=0.97, waiting_time=10000):
           not_found("Escolha uma opcao")
       bot.click_relative(242, 7)
       #Segundo CLick se mostrou necessário neste tipo de campo de informação
       bot.click()

       bot.kb_type(dados_df.loc[index, 'Quantidade de embalagens'])
       bot.enter()
       bot.enter()    

       print(index)



def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()








