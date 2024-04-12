from datetime import datetime
from time import sleep
from horas import executar_acoes

# Variável global para a hora formatada, usada na inserção da hora
hora_formatada = datetime.now().strftime("%H%M")

def verificando_solicitacao(bot, not_found):
    """
    Verifica a existência de uma solicitação específica na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param not_found: Função a ser chamada caso o elemento não seja encontrado.
    """
    '''
    if bot.find( "mais so", matching=0.97, waiting_time=5000):
        bot.click_relative(6, 9)
        if bot.find( "solicitacao de dieta", matching=0.97, waiting_time=10000):
            bot.click()
        else:
            not_found("solicitacao de dieta")
    else:
        not_found("Solicitações de dieta aberta")
        
        if not bot.find( "Solicitacao dieta azul", matching=0.97, waiting_time=10000):
            not_found("Solicitacao dieta azul")
        bot.click()
        
        
        '''
    if bot.find( "mais so", matching=0.97, waiting_time=500) or bot.find( "mais so azul", matching=0.97, waiting_time=500):
        bot.click_relative(6, 9)
    else:
        print("Não encontrou solicitacao")

    # Tenta encontrar e clicar em "Cadastro"      
    if bot.find( "solicitacao de dieta", matching=0.97, waiting_time=500) or bot.find( "Solicitacao dieta azul", matching=0.97, waiting_time=500):
        bot.click()
    else:
        print("Não encontrou solicitacao de dieta")

def inserir_codigo_cliente(bot, num_cliente, not_found, espera):
    """
    Insere o código do cliente na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param num_cliente: String contendo o número do cliente a ser inserido.
    :param not_found: Função a ser chamada caso o elemento não seja encontrado.
    :param espera: Tempo de espera (em segundos) após ações de digitação ou clique.
    """
    if not bot.find( "Codigo Cliente", matching=0.97, waiting_time=10000):
        not_found("Codigo Cliente")
    bot.click_relative(23, 33)
    sleep(espera)
    bot.kb_type(num_cliente)
    sleep(espera)
    bot.enter()
    bot.enter()

def inserir_codigo_paciente(bot, dados_df, index, not_found, espera):
    """
    Insere o código do paciente baseado no índice do DataFrame fornecido.

    :param bot: Instância do bot para interação com a interface.
    :param dados_df: DataFrame contendo os dados dos pacientes.
    :param index: Índice da linha atual no DataFrame.
    :param not_found: Função a ser chamada caso o elemento não seja encontrado.
    :param espera: Tempo de espera (em segundos) após ações de digitação ou clique.
    """
    nome_paciente = dados_df.loc[index, 'Nome'].strip()[:-1]  # Removendo espaços e a última letra
    sleep(espera)
    bot.key_f2()
    sleep(0.5)
    bot.kb_type(nome_paciente)
    sleep(2)
    if not bot.find( "Descricao", matching=0.97, waiting_time=10000):
        not_found("Descricao")
    bot.click_relative(0, 33)
    sleep(espera)


def pop_up_erro(bot, not_found):
    """
    Detecta e lida com um popup de erro recorrente pressionando Enter sempre que ele aparecer.

    :param bot: Instância do bot para interação com a interface.
    :param not_found: Função a ser chamada caso o popup não seja encontrado.
    """
    contador = 0

    while True:
        contador += contador 
        # Tenta encontrar o popup de erro pela descrição
        if bot.find( "mensagem da pagina da web", matching=0.97, waiting_time=1000):
            # Pressiona Enter para fechar o popup
            bot.enter()
            sleep(1)
            

        else: 
            if contador > 1:
            # Após os pop-ups acabarem, o sistema vai para Horário de entrega e só sai se escolher um horario
                inserir_horario_entrega(bot, not_found)
                
                break
            else:
                # Se o popup não for encontrado, sai do loop
                break
                
def inserir_horario_entrega(bot, not_found, espera):
    if not bot.find( "horario entrega", matching=0.97, waiting_time=10000):
                    not_found("horario entrega")
    bot.click_relative(17, 20)
    #bot.click()
    sleep(espera)
    bot.type_down()
            
def inserir_hora(bot, espera, not_found, index):
    """
    Insere a hora atual na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param espera: Tempo de espera (em segundos) após ações de digitação ou clique.
    :param not_found: Função a ser chamada caso o elemento não seja encontrado.
    """
    if not bot.find( "hora pedido", matching=0.97, waiting_time=10000):
        not_found("hora pedido")
    bot.click_relative(13, 31)
    sleep(espera)

    
    if index == 0:
        # Inserindo o horário uma vez 
        bot.kb_type(hora_formatada)
        sleep(espera)
        # Clicando e escolhendo o Horario de entrega
        inserir_horario_entrega(bot, not_found, espera)

    else:
        if not bot.find( "No prescricao", matching=0.97, waiting_time=10000):
            not_found("No prescricao")
        bot.click_relative(14, 18)
        sleep(espera)
        inserir_horario_entrega(bot, not_found, espera)
           
    

def inserir_unidade_de_interacao(bot, dados_df, index, espera, not_found):
    """
    Insere a unidade de internação do paciente na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param dados_df: DataFrame contendo os dados completos, incluindo a unidade de internação.
    :param index: Índice da linha atual no DataFrame.
    :param espera: Tempo de espera (em segundos) após ações de digitação ou clique.
    :param not_found: Função a ser chamada caso o elemento não seja encontrado.
    """
    if not bot.find( "unidade de internacao", matching=0.97, waiting_time=10000):
        not_found("unidade de internacao")
    bot.click_relative(37, 17)
    sleep(espera)
    if not bot.find( "Selecione o local de entrega", matching=0.97, waiting_time=10000):
        not_found("Selecione o local de entrega")
    sleep(espera)
    bot.click()
    sleep(espera)
    unidade_internacao = dados_df.loc[index, 'Un. Internação']
    bot.kb_type(unidade_internacao)
    sleep(espera)
    

def inserir_crm_padrao(bot, espera, not_found):
    """
    Insere um CRM padrão na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param espera: Tempo de espera (em segundos) após ações de digitação ou clique.
    """
    if not bot.find( "crm ", matching=0.97, waiting_time=10000):
        not_found("crm ")
    bot.click_relative(9, 19)
    sleep(espera)
    bot.kb_type("9574")  # Este valor é mantido como solicitado
    sleep(espera)
    bot.enter()
    sleep(espera)
    bot.enter()

# Repetição de padrões de documentação e implementação para inserir_produto e outras funções.

def inserir_produto(bot, dados_df, index, espera):
    """
    Insere o código do produto na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param dados_df: DataFrame contendo os dados dos produtos, incluindo o código do sistema.
    :param index: Índice da linha atual no DataFrame.
    :param espera: Tempo de espera (em segundos) após ações de digitação ou clique.
    """
    sleep(espera)
    codigo_produto = str(dados_df.loc[index, 'CodProduto Sistema'])
    bot.kb_type(codigo_produto)
    sleep(espera)
    bot.enter()

def inserir_via_adm(bot, dados_df, index, espera):
    """
    Insere a via de administração do medicamento na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param dados_df: DataFrame contendo os dados completos, incluindo a via de administração.
    :param index: Índice da linha atual no DataFrame.
    """
    sleep(espera)
    via_adm = dados_df.loc[index, 'Via Adm Sistema']
    bot.kb_type(via_adm)
    bot.enter()

def inserir_recipiente(bot, dados_df, index, espera):
    """
    Insere o tipo de recipiente na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param dados_df: DataFrame contendo os dados completos, incluindo o tipo de recipiente.
    :param index: Índice da linha atual no DataFrame.
    """
    recipiente = dados_df.loc[index, 'Recipiente']
    sleep(espera)
    bot.kb_type(recipiente)
    sleep(espera)
    bot.enter()

def inserir_volume(bot, dados_df, index, espera):
    """
    Insere o volume do medicamento na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param dados_df: DataFrame contendo os dados completos, incluindo o volume do medicamento.
    :param index: Índice da linha atual no DataFrame.
    """
    volume = str(dados_df.loc[index, 'Volume'])
    sleep(espera)
    bot.kb_type(volume)
    sleep(espera)
    bot.enter()

def inserir_horarios(bot, dados_df, index, not_found, espera):
    """
    Insere os horários de administração do medicamento na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param dados_df: DataFrame contendo os dados completos, incluindo os horários de administração.
    :param index: Índice da linha atual no DataFrame.
    :param not_found: Função a ser chamada caso o elemento não seja encontrado.
    """
    sleep(espera)
    bot.kb_type("0")
    sleep(espera)
    bot.enter()
    sleep(espera)
    bot.kb_type("0")
    sleep(espera)
    bot.enter()

    if not bot.find( "hora 0", matching=0.97, waiting_time=10000):
        not_found("hora 0")
    bot.click_relative(5, 5)
    
    horarios = dados_df.loc[index, 'Horários'].split('/')
    horarios = [int(h) for h in horarios]
    executar_acoes(bot, horarios)

def inserir_quantitativo_embalagens(bot, quantitativo, not_found, espera):
    """
    Insere o quantitativo de embalagens na interface do usuário.

    :param bot: Instância do bot para interação com a interface.
    :param quantitativo: Valor do 'Quantitativo Sistema' a ser inserido.
    :param not_found: Função a ser chamada caso o elemento não seja encontrado.
    """
    if not bot.find( "Quantitativo de embalagens", matching=0.97, waiting_time=10000):
        not_found("Quantitativo de embalagens")
    bot.click_relative(12, 46)
    sleep(espera)
    if not bot.find( "Escolha uma opcao", matching=0.97, waiting_time=10000):
        not_found("Escolha uma opcao")
    bot.click_relative(242, 7)
    sleep(espera)  # Segundo clique necessário neste tipo de campo de informação
    bot.click()
    sleep(espera)
    bot.kb_type(quantitativo)
    sleep(espera)
    bot.enter()
    sleep(espera)
    bot.enter()



def inserir_codigo_cliente_cadastro(bot, not_found, num_cliente):
    """
    Insere o código do cliente na interface de cadastro.

    Esta função busca o campo "Código Cliente" na interface, insere o número do cliente fornecido
    e confirma a entrada. Se o campo não for encontrado, a função de callback `not_found` é chamada.

    Parâmetros:
        bot (DesktopBot): Instância do bot para interação com a interface.
        not_found (function): Função de callback chamada quando um elemento não é encontrado.
        num_cliente (str): Número do cliente a ser inserido no campo de código.

    Retorna:
        None
    """
    # Busca pelo campo "Código Cliente" e insere o número do cliente
    if not bot.find("Codigo Cliente", matching=0.97, waiting_time=10000):
        not_found("codigo_do_cliente_cadastro")
    bot.click_relative(12, 32)
    bot.control_a()
    bot.backspace()
    bot.kb_type(num_cliente)
    bot.enter()
    
def abrir_cadastro_paciente(bot, not_found):  
    """
    Navega até a interface de cadastro de paciente.

    Esta função tenta encontrar e clicar nos botões "Arquivos" e "Cadastro" para
    navegar até a interface de cadastro de paciente. Se algum dos botões não for encontrado,
    tenta uma abordagem alternativa. Se "Paciente" ou "Paciente Azul" não forem encontrados,
    chama a função `not_found`.

    Parâmetros:
        bot (DesktopBot): Instância do bot para interação com a interface.
        not_found (function): Função de callback chamada quando um elemento não é encontrado.

    Retorna:
        None
    """
    if bot.find( "arquivos", matching=0.97, waiting_time=500) or bot.find( "arquivo azul mais", matching=0.97, waiting_time=500):
        bot.click_relative(4, 6)
    else:
        print("Não encontrou 'Arquivos', tentando outra abordagem.")

    # Tenta encontrar e clicar em "Cadastro"      
    if bot.find( "cadastro", matching=0.97, waiting_time=500) or bot.find( "cadastro azul", matching=0.97, waiting_time=500):
        bot.click_relative(4, 7)
    else:
        print("Não encontrou 'Cadastro', tentando outra abordagem.")

    # Tenta encontrar e clicar em "Paciente" ou "Paciente Azul"
    if bot.find( "paciente", matching=0.97, waiting_time=500) or bot.find( "Paciente Azul", matching=0.97, waiting_time=500):
        bot.click()
    else:
        not_found("Paciente/Paciente Azul")

def inserir_codigo_paciente_leito(bot, nome_paciente, espera, not_found):
    """
    Insere o código do paciente para atualizar leito.

    Remove o último caractere do nome do paciente (presumindo que seja um espaço ou caracter especial),
    abre a busca por nome de paciente, digita o nome, e seleciona o paciente na lista de descrição.
    Se a descrição do paciente não for encontrada, chama a função `not_found`.

    Parâmetros:
        bot (DesktopBot): Instância do bot para interação com a interface.
        nome_paciente (str): Nome do paciente a ser buscado e selecionado.
        espera (int/float): Tempo de espera após certas ações, em segundos.
        not_found (function): Função de callback chamada quando um elemento não é encontrado.

    Retorna:
        None
    """
    nome_paciente = nome_paciente.strip()[:-1]
    sleep(espera)
    bot.key_f2()
    sleep(1)
    bot.kb_type(nome_paciente)
    sleep(2)
    if not bot.find( "Descricao", matching=0.97, waiting_time=10000):
        not_found("Descricao")
    bot.click_relative(0, 33)
    sleep(espera)
