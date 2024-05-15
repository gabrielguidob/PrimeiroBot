import tkinter as tk
from tkinter import ttk

def mostrar_alerta_problemas(linhas_com_problemas):
    janela_alerta = tk.Toplevel()
    janela_alerta.title("Alerta de Problemas")
    janela_alerta.geometry("500x300")

    frame = ttk.Frame(janela_alerta)
    frame.pack(fill='both', expand=True)

    label_titulo = ttk.Label(frame, text="Inconsistência de dados nos seguintes pacientes:", font=('Helvetica', 10, 'bold'), foreground="#b22222")
    label_titulo.pack(pady=10)

    for paciente, atendimento in zip(linhas_com_problemas["Paciente"], linhas_com_problemas["Nr. Atend."]):
        label = ttk.Label(frame, text=f"Paciente: {paciente}, Nr. Atend.: {atendimento}")
        label.pack()

    janela_alerta.mainloop()
