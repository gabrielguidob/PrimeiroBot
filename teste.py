#import pyautogui
#
## Obtém a resolução do monitor principal
#largura, altura = pyautogui.size()
#
#print("Largura:", largura, "Altura:", altura)
#
import pygetwindow as gw

def listar_titulos_janelas():
    todas_janelas = gw.getAllWindows()
    print("Títulos das janelas abertas:")
    for janela in todas_janelas:
        if janela.title == 'WhatsApp':
            janela.minimize()
        if "matriz3:57772" in janela.title:
            print(janela.title.startswith("http://matriz3:57772"))
            janela.maximize()
        print(janela.title)

listar_titulos_janelas()