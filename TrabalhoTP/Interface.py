import Principal
from tkinter import * 
from json import *


JanelaPrincipal = Tk()
JanelaPrincipal.geometry("700x400")
JanelaPrincipal.resizable(False, False)
JanelaPrincipal.iconbitmap("Icones\\iconhome.ico")

def AdicionarAluno():
  #Configurações do PopUp {
  PopUp = Toplevel()
  PopUp.geometry("300x170")
  PopUp.resizable(False, False)
  PopUp.iconbitmap("Icones\\iconadd.ico")
  #Configurações do PopUp }
  
  #Função de confirmar e cancelar {
  def Confirmar():
    NomeDigitado = DigitarNome.get()
    Principal.AddAluno(NomeDigitado)
    PopUp.destroy()

  def Cancelar():
    PopUp.destroy()
  #Função de confirmar e cancelar }

  #Elementos no PopUp {  
  Label(PopUp, text = "Digite o nome do aluno(a)").pack(pady = 15)

  DigitarNome = Entry(PopUp)
  DigitarNome.pack(pady = 15)

 
  BotaoConfirmar = Button(PopUp, text = "Confirmar", command = Confirmar).pack(pady = 5, padx = 25, side = "left")
  BotaoCancelar = Button(PopUp, text = "Cancelar", command = Cancelar).pack(pady= 5, padx= 25, side = "right")
  #Elementos no PopUp }  
  
Botao1 = Button(JanelaPrincipal, text = "Adicionar aluno", command = AdicionarAluno)
Botao1.pack()

mainloop()

  

