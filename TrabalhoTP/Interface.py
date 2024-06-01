import Principal
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from tkinter import * 
from json import *

#Configurações da janela principal {
JanelaPrincipal = Tk()
JanelaPrincipal.geometry("700x400") #Tamanho
JanelaPrincipal.resizable(False, False)# Tamanho reajustável
JanelaPrincipal.iconbitmap("Icones\\iconhome.ico") #Ícone
JanelaPrincipal.title("Registros de alunos") #Título da janela
#Configurações da janela principal }

def AdicionarAluno():

  #Configurações do PopUp {
  PopUpAddAluno = Toplevel()
  PopUpAddAluno.geometry("300x350") #Tamanho
  PopUpAddAluno.resizable(False, False) #Tamanho reajustável 
  PopUpAddAluno.iconbitmap("Icones\\iconadd.ico") #Ícone
  PopUpAddAluno.title("Adicionar novo aluno") #Título
  PopUpAddAluno.configure(bg = "#212529") #Cor do fundo 
  #Configurações do PopUp }
  
  #Função de confirmar e cancelar {
  def Confirmar():
    NomeDigitado = DigitarNome.get() #Armazena o nome digitado no Entry
    
    #Exibe um erro caso o Entry esteja em branco, se não, adiciona o aluno
    if NomeDigitado == "":
      messagebox.showerror(title = "Erro", message = "A caixa está em branco, digite um nome!") 
    else:
      Principal.AddAluno(NomeDigitado)
      PopUpAddAluno.destroy()

  #Destroi o Popup
  def Cancelar():
    PopUpAddAluno.destroy()
  #Função de confirmar e cancelar }

  #Elementos no PopUp {  
  FrameElementos = Frame(PopUpAddAluno, padx = 10, pady = 10, relief = "groove") #Frame para posicionar os botões
  FrameElementos["bg"] = "#343A40" #Cor de fundo do Frame
  FrameElementos.place(relx = 0.5, rely = 0.5, anchor = "center") #Posicionamento do Frame
  
  #Texto em cima
  Fonte = font.Font(size = 10, weight = "bold")
  Label(
  FrameElementos, #Elemento pai
  font = Fonte,
  text = "Digite o nome do aluno(a)", #Texto no Label
  bg= "#343A40", #Cor de fundo
  fg= "White").pack(pady = 15) # Cor do texto e posição
  
  #Caixa de texto
  DigitarNome = Entry(FrameElementos, width = 24)
  DigitarNome.pack(pady = 15)

  FonteBotoes = font.Font(size = 10, weight = "bold")
  #Botão de confirmar
  BotaoConfirmar = Button(
  FrameElementos, #Elemento pai
  font = FonteBotoes, #Fonte
  text = "Confirmar", #Texto do botão
  command = Confirmar, #Função que ele executa
  width = 20, #Tamanho
  bg = "#343A40", #Cor do botão
  fg = "White", #Cor do texto do botão
  cursor = "hand2") #Cursor exibido quando o mouse passa pelo botão
  BotaoConfirmar.pack(pady = 10, padx = 25)

  #Eventos botões
  def MouseEnterConfirm(evento):
    BotaoConfirmar["bg"] = "#1E4D2B" #Cor do botão
  def MouseLeaveConfirm(evento):
    BotaoConfirmar["bg"] = "#343A40" #Cor do botão

  BotaoConfirmar.bind("<Enter>", MouseEnterConfirm) #Evento que executa uma função quando o mouse passa por cima do botão
  BotaoConfirmar.bind("<Leave>", MouseLeaveConfirm) #Evento que executa uma função quando o mouse sai do botão

  #Botão de cancelar
  BotaoCancelar = Button(
  FrameElementos, #Elemento pai
  font = FonteBotoes, #Fonte
  text = "Cancelar", #Texto no botão
  command = Cancelar, #Funçaõ que ele executa
  width = 20, #Tamanho do botão
  bg= "#343A40", #Cor do botão
  fg= "White", #Cor do texto
  cursor = "hand2",) #Cursor exibido quando o mouse passa pelo botão

  #Eventos botões
  def MouseEnterCancel(evento):
    BotaoCancelar["bg"] = "#7C0902" #Cor do botão
  def MouseLeaveCancel(evento):
    BotaoCancelar["bg"] = "#343A40" #Cor do botão

  BotaoCancelar.bind("<Enter>", MouseEnterCancel)#Evento que executa uma função quando o mouse passa por cima do botão
  BotaoCancelar.bind("<Leave>", MouseLeaveCancel)#Evento que executa uma função quando o mouse sai do botão

  BotaoCancelar.pack(pady= 10, padx= 25) #posicionamento do botão
   
  #Elementos no PopUp }  

def RemoverAluno():  

  #Configurações do Popup {
  PopUpRemAluno = Toplevel()
  PopUpRemAluno.geometry("500x300") #Tamanho
  PopUpRemAluno.title("Remover aluno") #Título
  PopUpRemAluno.iconbitmap("Icones\\iconrem.ico") #Ícone
  PopUpRemAluno["bg"] = "#212529" #Cor do fundo
  PopUpRemAluno.resizable(False, False) #Tamanho reajustável
  
  #Texto exibido no PopUp 
  Fonte = font.Font(size = 12, weight = "bold")
  Label(
  PopUpRemAluno, #Widget pai 
  font = Fonte, #Fonte
  text = "Dê um duplo clique no aluno que deseja remover", #Texto 
  fg = "#CED4DA", #Cor do texto
  bg = "#212529", #Cor do fundo 
  ).pack(pady = 10)
  
  #Configurações do Popup }


  #Frame para posicionar a tabela 
  FrameTabela = Frame(PopUpRemAluno)
  FrameTabela.pack(anchor = "center", pady= 25)  #Posicionamento do Frame

  #Estrutura da tabela
  TabelaAlunos = ttk.Treeview(FrameTabela, columns = ("Nome", "Matrícula"), show = "headings")

  #Configurações da tabela
  TabelaAlunos.heading("Nome", text = "Nome")
  TabelaAlunos.heading("Matrícula", text = "Matrícula")  
  TabelaAlunos.pack(anchor = "center")
  
  def AtualizarTabela():
    #Remove os dados da tabela
    for j in TabelaAlunos.get_children():
      TabelaAlunos.delete(j)

    #Adiciona os dados do Json na tabela 
    for i in Principal.LoadJson("Registros.json"):
      TabelaAlunos.insert("", "end", values = (i["Nome"], i["Matricula"]))
  
  #Carrega os dados da tabela após sua criação
  AtualizarTabela()

  #Excluir aluno do Json e da tabela {
  def ExcluirAluno(evento):
    AlunosSelecionados = TabelaAlunos.selection() #Identifica quais salunos foram selecionados na tabela
    DadosDoAluno = TabelaAlunos.item(AlunosSelecionados[0], "values") #Armazena os dados do primeiro aluno selecionado
    
    #Exibe mensagem de confirmação da exclusão  
    ConfirmarExclusao = messagebox.askyesno("Confirmar exclusão?", f"Deseja excluir o aluno: {DadosDoAluno[0]}?")

    if ConfirmarExclusao == True: #Se confirmada a exclusão executa 
      AlunosCadastrados = Principal.LoadJson("Registros.json") #Carrega os dados no Json

      for i in AlunosCadastrados:
        if DadosDoAluno[0] == i["Nome"] and DadosDoAluno[1] == i["Matricula"]:
          AlunosCadastrados.remove(i)
      
      #Regrava o Json sem os dados selecionados
      with open("Registros.json", "w") as JsonFile:
        dump(AlunosCadastrados, JsonFile, indent = 4)
    
      AtualizarTabela() #Atualiza a tabela
  #Interação com a tabela em caso de duplo clique
  TabelaAlunos.bind("<Double-1>", ExcluirAluno)
  #Excluir aluno do Json e da tabela }

BotaoAddAluno = Button(JanelaPrincipal, text = "Adicionar aluno", command = AdicionarAluno)
BotaoAddAluno.pack()

BotaoRemAluno = Button(JanelaPrincipal, text = "Remover aluno", command = RemoverAluno)
BotaoRemAluno.pack()

mainloop()

  

