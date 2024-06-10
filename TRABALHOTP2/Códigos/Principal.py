import sys 
import subprocess
import importlib
import tkinter as tk
import tkinter.ttk as ttk
import json
from typing import Callable
from tkinter import messagebox
from PIL import Image, ImageTk

libs = {
    "pillow" : "from PIL import Image, ImageTk",
    "typing_Callable" : "from typing import Callable",
    "tkinter_font" : "from tkinter import font, messagebox",
    "tkinter_all" : "import tkinter as tk",
    "json" : None
}

def check_import(lib, especifico=None):
    """Importa as bibliotecas no dicionário libs"""

    try:
        importlib.import_module(lib.split("_")[0])
    except ImportError:
        subprocess.check_call([sys.executable, "-n", "pip", "install", lib])
    finally:
        if especifico is None:
            globals()[lib] = __import__(lib)
        else:
            exec(especifico, globals())

#for lib, especifico in libs.items():
#    check_import(lib, especifico)

def criar_entry(
    wid_pai:str, 
    placeholder:str, 
    largura:float, 
    altura:float, 
    pos_y:float, 
    pos_x:float=0.5, 
    ancora:str="center",
    cor_texto:str="#495057", 
    relevo:str="groove", 
    mostrar:str=""
):
    """
    Função: 
        Cria um widget entry com as especificações definidas nos argumentos
    
    Args: 
        largura e altura (% em relação ao widget pai), 
        pos_y e pos_x(% com base no widget pai), caractere mostrado ao digitar. 
    
    Retorna:
        Retorna o valor digitado na caixa
    """
    entry = ttk.Entry(wid_pai, foreground=cor_texto)
    entry.insert(0, placeholder)
    entry["justify"] = "center"
    entry.place(relwidth=largura, relheight=altura, 
                rely=pos_y, relx=pos_x, anchor=ancora)
    
    def entry_clicado(evento):
        """Remove o texto de dentro do entry quando clicado"""
        if entry.get() == placeholder:
            entry.delete(0, "end") 
            entry.insert(0, "")
            entry["show"] = mostrar
            entry["foreground"] = "Black"
            entry["justify"] = "left"   

    def entry_padrao(evento):
        """Adiciona o texto caso o widget esteja em branco depois de clicado"""
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry["show"] = ""
            entry["foreground"] = "#495057"
            entry["justify"] = "center"
    
    #Eventos de interação com o entry 
    entry.bind("<FocusIn>", entry_clicado)
    entry.bind("<FocusOut>", entry_padrao)
    return entry

def criar_botao(
        wid_pai:str, 
        placeholder:str, 
        comando:Callable,
        largura:float, 
        altura:float, 
        pos_y:float, 
        pos_x:float=0.5, 
        ancora:str="center",
        cor_fundo:str="#495057",
        cor_interacao:str="#343A40",
        cor_clicado:str="#343A40",
        cor_texto_clicado:str="#ADB5BD", 
        cor_texto:str="#ADB5BD", 
        relevo:str="groove", 
        cursor:str="hand2"
):
    """
    Função: 
        Cria um widget botão com as especificações definidas nos argumentos
    Args:
        largura, altura, pos_x e pos_y(% com base no widget pai), 
    Retorna:
        Nada
    """
    botao = tk.Button(
        wid_pai, 
        text=placeholder, 
        command=comando, 
        background=cor_fundo, 
        activebackground=cor_clicado, 
        activeforeground=cor_texto_clicado, 
        foreground=cor_texto, 
        relief=relevo, 
        cursor=cursor
)
    botao.place(relwidth=largura, relheight=altura, rely=pos_y, relx=pos_x, anchor=ancora)
    def mouse_in(evento):
        botao["bg"] = cor_interacao
    def mouse_out(evento):
        botao["bg"] = cor_fundo

    botao.bind("<Enter>", mouse_in)
    botao.bind("<Leave>", mouse_out)

with open("registros.json", "r") as f:
    for i in json.load(f):
        if i["Logado"] is True:
            arquivo_json= i["Nome"] + ".json"

def adicionar_evento():
    """
    Função:
        Usa os dados no entry para registrar um novo evento
    """

    #Configurações do Pop-Up
    popup_add_evento = tk.Toplevel(bg="#212529")
    popup_add_evento.geometry("250x400")
    popup_add_evento.resizable(False, False)
    popup_add_evento.title("Adicionar evento")
    popup_add_evento.iconbitmap("Icones\\addeventicon.ico")

    #Frame para posicionar os widgets
    frame_add_evento = tk.Frame(
        popup_add_evento
    )
    frame_add_evento.place(
        anchor="center",
        relheight=0.9,
        relwidth=0.8,
        relx=0.5,
        rely=0.5
    )

    #Carrega a imagem e adapta para o tkinter
    img_add_evento = Image.open("frame_add_event.png")
    img_add_evento = ImageTk.PhotoImage(img_add_evento)

    #Label para posicionar a imagem
    image_add_evento = tk.Label(
        frame_add_evento, 
        image=img_add_evento
    )
    image_add_evento.place(anchor="center", relheight=1, relwidth=1, relx=0.5, rely=0.5)
    
    #Mantém a imagem para evitar ela de ser excluída pelo garbage collector
    image_add_evento.image=img_add_evento

    #Entrys para receber os dados
    descricao = criar_entry(
        frame_add_evento,
        "Digite a descrição do evento",
        0.8,
        0.08,
        0.1
    )
    data = criar_entry(
        frame_add_evento,
        "Digite a data do evento",
        0.8,
        0.08,
        0.25
    )
    hora = criar_entry(
        frame_add_evento,
        "Digite a hora do evento",
        0.8,
        0.08,
        0.4
    )
    
    #Dados para salvar
    evento = {
        "Descricao" : descricao.get(),
        "Data" : data.get(),
        "Hora" : hora.get()
    }

    with open(arquivo_json, "a+") as file_add_evento: #Abre o arquivo
        try:
            dados_no_json = json.load(file_add_evento) #Tenta ler os dados
        #Executa caso o arquivo esteja vazio
        except json.JSONDecodeError:
            dados = []
            dados.append(evento)
            json.dump(dados, file_add_evento, indent=4)
        #Executa caso tenha algum conteúdo
        else:
            for i in json.load(file_add_evento):
                if (i["Descricao"] == descricao and 
                    i["Data"] == data): #Checa se os dados existem se sim duplicado é verdadeiro
                    duplicado = True
                    check = messagebox.askyesno("O evento já existe!", 
                                                "O evento já existe na sua agenda, deseja adicionar mesmo assim?") 
                    if check is True: #Se o usuário selecionar sim no check executa
                        json.dump(dados, file_add_evento, indent=4)
                    else:
                        break

            if duplicado is False: #Executado se os dados não existirem no arquivo
                json.dump(dados, file_add_evento, indent=4)

#Configurações da janela principal
janela_principal = tk.Tk()
janela_principal.geometry("820x400")
janela_principal.resizable(False, False)
janela_principal.iconbitmap("Icones\\iconhome.ico")
janela_principal.configure(background="#212529", )

#Imagem de fundo dos botões
img_botoes = Image.open("frame_botoes.png")
img_botoes = ImageTk.PhotoImage(img_botoes)

#Estilo dos frames
estilo_frame = ttk.Style()
estilo_frame.configure(
    "Frames.TFrame",
    background="#212529" 
)

#Frame para posicionar os botões
frame_botoes = ttk.Frame(
    janela_principal,
    width=200,
    height=360,
    style="Frames.TFrame"
)
frame_botoes.place( 
    rely=0.5, 
    relx=0.15, 
    anchor="center"
)

#Imagem de fundo dos botões
imagem_botoes = tk.Label(
    frame_botoes, 
    image=img_botoes, 
    highlightthickness=0
)
imagem_botoes.place(relheight=1, relwidth=1)

botao_add_evento = criar_botao(
    frame_botoes,
    "Adicionar evento",
    adicionar_evento,
    0.8,
    0.08,
    0.5,
    0.5
)

#Linha no meio da tela 
linha_separar = ttk.Separator(janela_principal, orient="vertical")
linha_separar.place(x=250, relheight=1)

#Imagem de fundo da tabela
img_grade = Image.open("frame_tabela.png")
img_grade = ImageTk.PhotoImage(img_grade)

#Frame para posicionar a tabela
frame_grade = ttk.Frame(
    janela_principal,
    width=500,
    height=360,
    style="Frames.TFrame"
)
frame_grade.place(
    rely=0.5, 
    relx=0.68, 
    anchor="center"
)

#Imagem de fundo da tabela
imagem_grade = tk.Label(
    frame_grade, 
    image=img_grade, 
    highlightthickness=0
)
imagem_grade.place(relheight=1, relwidth=1)


#Estilo da tabela
estilo_tabela = ttk.Style()
estilo_tabela.configure(
    "estilo.Treeview", 
    background="#6C757D", 
    foreground="#CED4DA",
    fieldbackground="#6C757D")
estilo_tabela.configure(
    "estilo.Treeview.Heading",
    background="#495057",
    foreground="#CED4DA"
)

#Estrutura da tabela
tabela = ttk.Treeview(frame_grade, columns=(0, 1, 2), show="headings", style="estilo.Treeview")
tabela.heading(0, text="Descrição")
tabela.heading(1, text="Data")
tabela.heading(2, text="Hora")

tabela.column(0, width=200, anchor="center")
tabela.column(1, width=100, anchor="center")
tabela.column(2, width=100, anchor="center")

tabela.place(
    anchor="center",
    relheight=0.85,
    relwidth=0.85,
    rely=0.5,
    relx=0.5
)

tk.mainloop()
