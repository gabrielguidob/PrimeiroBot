app_instance = None  # Variável global para armazenar a instância da aplicação

def set_app_instance(instance):
    global app_instance
    app_instance = instance

def chamar_mostrar_primeira_tela():
    if app_instance:
        app_instance.mostrar_primeira_tela()