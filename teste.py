import pygetwindow as gw

def listar_titulos_janelas():
    todas_janelas = gw.getAllWindows()
    print("Títulos das janelas abertas:")
    for janela in todas_janelas:
        print(janela.title)

listar_titulos_janelas()
