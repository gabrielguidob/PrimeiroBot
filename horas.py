def acao_0(bot):
    if not bot.find( "0", matching=0.97, waiting_time=10000):
        not_found("0")
    bot.click_relative(7, 8)

def acao_1(bot):
    if not bot.find( "1", matching=0.97, waiting_time=10000):
        not_found("1")
    bot.click_relative(9, 8)
def acao_2(bot):
    if not bot.find( "2", matching=0.97, waiting_time=10000):
        not_found("2")
    bot.click_relative(10, 8)
def acao_3(bot):
    if not bot.find( "3", matching=0.97, waiting_time=10000):
        not_found("3")
    bot.click_relative(8, 8)
def acao_4(bot):
    if not bot.find( "4", matching=0.97, waiting_time=10000):
        not_found("4")
    bot.click_relative(9, 6)
def acao_5(bot):
    if not bot.find( "5", matching=0.97, waiting_time=10000):
        not_found("5")
    bot.click_relative(9, 7)
def acao_6(bot):
    if not bot.find( "6", matching=0.97, waiting_time=10000):
        not_found("6")
    bot.click_relative(8, 7)
def acao_7(bot):
    if not bot.find( "7", matching=0.97, waiting_time=10000):
        not_found("7")
    bot.click_relative(8, 7)
def acao_8(bot):
    if not bot.find( "8", matching=0.97, waiting_time=10000):
        not_found("8")
    bot.click_relative(8, 7)
def acao_9(bot):
    if not bot.find( "9", matching=0.97, waiting_time=10000):
        not_found("9")
    bot.click_relative(8, 7)
def acao_10(bot):
    if not bot.find( "10", matching=0.97, waiting_time=10000):
        not_found("10")
    bot.click_relative(7, 7)
def acao_11(bot):
    if not bot.find( "11", matching=0.97, waiting_time=10000):
        not_found("11")
    bot.click_relative(6, 7)
def acao_12(bot):
    if not bot.find( "12", matching=0.97, waiting_time=10000):
        not_found("12")
    bot.click_relative(7, 9)
def acao_13(bot):
    if not bot.find( "13", matching=0.97, waiting_time=10000):
        not_found("13")
    bot.click_relative(8, 8)
def acao_14(bot):  
    if not bot.find( "14", matching=0.97, waiting_time=10000):
        not_found("14")
    bot.click_relative(9, 8)

def acao_15(bot):
    if not bot.find( "15", matching=0.97, waiting_time=10000):
        not_found("15")
    bot.click_relative(9, 8)
def acao_16(bot):
    if not bot.find( "16", matching=0.97, waiting_time=10000):
        not_found("16")
    bot.click_relative(10, 8)
def acao_17(bot):
    if not bot.find( "17", matching=0.97, waiting_time=10000):
        not_found("17")
    bot.click_relative(7, 7)
def acao_18(bot):
    if not bot.find( "18", matching=0.97, waiting_time=10000):
        not_found("18")
    bot.click_relative(9, 6)

def acao_19(bot):
    if not bot.find( "19", matching=0.97, waiting_time=10000):
        not_found("19")
    bot.click_relative(7, 7)
def acao_20(bot):
    if not bot.find( "20", matching=0.97, waiting_time=10000):
        not_found("20")
    bot.click_relative(6, 6)
def acao_21(bot):
    if not bot.find( "21", matching=0.97, waiting_time=10000):
        not_found("21")
    bot.click_relative(8, 7)
def acao_22(bot):
    if not bot.find( "22", matching=0.97, waiting_time=10000):
        not_found("22")
    bot.click_relative(9, 7)
def acao_23(bot):
    if not bot.find( "23", matching=0.97, waiting_time=10000):
        not_found("23")
    bot.click_relative(7, 7)
    

acoes = {
    0: acao_0,
    1: acao_1,
    2: acao_2,
    3: acao_3,
    4: acao_4,
    5: acao_5,
    6: acao_6,
    7: acao_7,
    8: acao_8,
    9: acao_9,
    10: acao_10,
    11: acao_11,
    12: acao_12,
    13: acao_13,
    14: acao_14,
    15: acao_15,
    16: acao_16,
    17: acao_17,
    18: acao_18,
    19: acao_19,
    20: acao_20,
    21: acao_21,
    22: acao_22,
    23: acao_23,
    24: acao_0,
    
}

def executar_acoes(bot, numeros):
    for numero in numeros:
        if numero in acoes:
            acoes[numero](bot)
        else:
            print(f"Ação para o número {numero} não definida.")






