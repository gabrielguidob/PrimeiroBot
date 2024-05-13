import re

def padronizar_horarios(horario):
    # Remover caracteres indesejados (tudo exceto dígitos e barra)
    horario_limpo = re.sub(r'[^\d/]', '', horario)
    # Dividir a string nos separadores de barra
    partes = horario_limpo.split('/')
    # Remover espaços em branco extras, zeros à esquerda e converter para formato desejado
    partes_limpias = [str(int(part.strip())) for part in partes if part.strip()]
    # Reunir tudo de volta com barras
    return '/'.join(partes_limpias)

# Exemplo de uso:
horario_exemplo = "H00/03/6 /07..."
horario_padronizado = padronizar_horarios(horario_exemplo)
print(horario_padronizado)

testes = [
    "00/03/6/07",
    "H00/H1/05/H06/",
    "0/ 6/ 7/ 09/",
    "0/3/6/7"
]

for teste in testes:
    print(padronizar_horarios(teste))





horarios = padronizar_horarios(horario_exemplo)

horarios = horarios.split('/')

horarios = [int(h) for h in horarios]

print(horarios)