#Importando datetime
from datetime import datetime

from time import sleep
#Importando arquivo horas.py
from horas import executar_acoes

import keyboard

#Concertar essa função
def verificando_solicitacao(bot, not_found):
    if bot.find( "mais so", matching=0.97, waiting_time=5000):
        bot.click_relative(6, 9)
        if bot.find( "solicitacao de dieta", matching=0.97, waiting_time=10000):
            bot.click()
        not_found("solicitacao de dieta")
    else:
        not_found("Solicitações de dieta aberta")    
    
 
#Pegando hora atual e modificando
hora_atual = datetime.now()
hora_formatada = hora_atual.strftime("%H%M")


def inserir_codigo_cliente(bot, num_cliente, not_found, espera):
     if not bot.find( "Codigo Cliente", matching=0.97, waiting_time=10000):
         not_found("Codigo Cliente")
     bot.click_relative(23, 33)
     sleep(espera)
     # Codigo Cliente
     bot.kb_type(num_cliente)
     sleep(espera)
     bot.enter()
     bot.enter()

def inserir_codigo_paciente(bot, dados_completos_df, index, not_found, espera):
    nome_paciente = str(dados_completos_df.loc[index, 'Nome'])
    # Removendo os espaços em branco no final
    nome_paciente_sem_espacos = nome_paciente.rstrip()
    # Agora, removendo apenas uma letra adicional após a remoção dos espaços
    nome_final = nome_paciente_sem_espacos[:-1] 
    bot.key_f2()
    bot.kb_type(nome_final)
    sleep(espera * 2)

    if not bot.find( "Descricao", matching=0.97, waiting_time=10000):
        not_found("Descricao")
    bot.click_relative(0, 33)
    sleep(espera)
    #Proximo enter fecha o popup
    #bot.enter()
    
#Depois de inserir o codigo do paciente o sistema foi direto para o campo do CRM
#Inserindo o CRM o sistema foi para o OK e depois direto para PRODUTO


def inserir_hora(bot, espera):
    sleep(espera)
    bot.kb_type(hora_formatada)
    sleep(espera)
    bot.enter()
    sleep(espera)
    bot.enter()
    sleep(espera)
    #sleep(0.1)
    bot.type_down()
    sleep(espera)
    bot.enter()
    #sleep(0.1)

def inserir_unidade_de_interacao2(bot, dados_completos_df, index, not_found, espera):
    if not bot.find( "UnidadeDeInternacao", matching=0.97, waiting_time=10000):
        not_found("UnidadeDeInternacao")
    bot.click_relative(66, 19)
    sleep(espera)
    bot.click()
    sleep(espera)
    bot.kb_type(dados_completos_df.loc[index, 'Un. Internação'])
    sleep(espera)
    bot.enter()

def inserir_unidade_de_interacao(bot, dados_completos_df, index, espera):
    sleep(espera)
    bot.kb_type(dados_completos_df.loc[index, 'Un. Internação'])
    sleep(espera)
    bot.enter()


def inserir_crm_padrao(bot, espera):
    sleep(espera)
    bot.kb_type("9574")
    sleep(espera)
    bot.enter()
    sleep(espera)
    bot.enter()


def inserir_produto(bot, dados_produtos_df, index, espera):
    sleep(espera)
    bot.kb_type(str(dados_produtos_df.loc[index, 'CodProduto Sistema']))
    sleep(espera)
    bot.enter()


def inserir_via_adm(bot, dados_completos_df, index):
    bot.kb_type(dados_completos_df.loc[index, 'Via Adm Sistema'])
    bot.enter()


def inserir_recipiente(bot, dados_completos_df, index):
    bot.kb_type(dados_completos_df.loc[index, 'Recipiente'])
    bot.enter()


def inserir_volume(bot, dados_completos_df, index): 
    bot.kb_type(str(dados_completos_df.loc[index, 'Volume']))
    bot.enter()

#Clica nas caixinhas de horarios
def inserir_horarios(bot, dados_completos_df, index, not_found):
    bot.kb_type("0")
    bot.enter()
    bot.kb_type("0")
    bot.enter()

    if not bot.find( "hora 0", matching=0.97, waiting_time=10000):
        not_found("hora 0")
    bot.click_relative(5, 5)
    
    
    #Separando e marcando os horários
    hora = dados_completos_df.loc[index, 'Horários']
    hora_separada = hora.split('/')
    hora_separada = [int(h) for h in hora_separada]
    executar_acoes(bot, hora_separada)


def inserir_quantitativo_embalagens(bot, dados_completos_df, index, not_found):
    if not bot.find( "Quantitativo de embalagens", matching=0.97, waiting_time=10000):
        not_found("Quantitativo de embalagens")
    bot.click_relative(12, 46)
    if not bot.find( "Escolha uma opcao", matching=0.97, waiting_time=10000):
        not_found("Escolha uma opcao")
    bot.click_relative(242, 7)
    #Segundo CLick se mostrou necessário neste tipo de campo de informação
    bot.click()
    bot.kb_type(dados_completos_df.loc[index, 'Quantitativo Sistema'])
    bot.enter()
    bot.enter()


