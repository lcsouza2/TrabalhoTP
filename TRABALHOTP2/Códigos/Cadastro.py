import sys 
import subprocess
import importlib
import tkinter as tk
import json
from typing import Callable
from tkinter import messagebox

libs = {
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

# for lib, especifico in libs.items():
#     check_import(lib, especifico)

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
    entry = tk.Entry(wid_pai, fg=cor_texto, relief=relevo)
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
            entry["fg"] = "Black"
            entry["justify"] = "left"   

    def entry_padrao(evento):
        """Adiciona o texto caso o widget esteja em branco depois de clicado"""
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry["show"] = ""
            entry["fg"] = "#495057"
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
        bg=cor_fundo, 
        activebackground=cor_clicado, 
        activeforeground=cor_texto_clicado, 
        fg=cor_texto, 
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

def entry_valido(entry, placeholder):
    digitado = entry.get()
    return digitado and digitado.strip() and digitado != placeholder

def cadastrar(entry_nome, entry_email, entry_telefone, entry_senha):
    if not (entry_valido(entry_nome, placeholders[0]) and 
            entry_valido(entry_email, placeholders[1]) and
            entry_valido(entry_telefone, placeholders[2]) and
            entry_valido(entry_senha, placeholders[3])):
            messagebox.showerror("Erro!", "Preencha todos os campos corretamente")
    else:
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        senha = entry_senha.get()

        dados = {
            "Nome" : nome,
            "Email" : email,
            "Telefone" : telefone,
            "Senha" : senha,
            "Logado" : True,
            "Arquivos" : f"{nome}.json"
        }

        try:
            with open("registros.json", "r") as ler_json: #Abre o arquivo
                try:
                    usuarios_no_json = json.load(ler_json) #tenta ler o arquivo
                except json.JSONDecodeError:
                    usuarios_no_json = [] #retorna uma lista vazia se o arquivo também estiver
        except FileNotFoundError:
            usuarios_no_json = [] #retorna uma lista vazia se o arquivo não existir
        
        for i in usuarios_no_json:
            if dados["Nome"] == i["Nome"]: 
                messagebox.showerror("Usuário existente", "O usuário já existe!")
                break 
        else:
            usuarios_no_json.append(dados) #Adiciona os dados a lista

            with open("registros.json", "w") as gravar_dados:
                json.dump(usuarios_no_json, gravar_dados, indent= 4 )
            messagebox.showinfo("Cadastro efetuado", "Estamos te encaminhando a tela principal")

            janela_principal.destroy()
            subprocess.run(["python", "Códigos\\Principal.py"])

def logar():
    janela_principal.destroy() 
    subprocess.run(["python", "Códigos\\Login.py"])

janela_principal = tk.Tk()
janela_principal.title("Cadastro")
janela_principal.geometry("300x400")
janela_principal.resizable(False, False)
janela_principal.iconbitmap("Icones\\iconadd.ico")
janela_principal["bg"] = "#212529"
    
frame_cadastro = tk.Frame(
    janela_principal, 
    padx = 10,
    pady = 10, 
    bg = "#343A40"
)
frame_cadastro.place(
    anchor = "center", 
    relx = 0.5, 
    rely = 0.5, 
    relheight = 0.8, 
    relwidth = 0.8
)

placeholders = ("Digite seu nome", "Digite seu email", "Digite o seu telefone", "Digite sua senha")
entry_nome = criar_entry(
    frame_cadastro, 
    placeholders[0], 
    0.8, 
    0.08, 
    0.1
    )
entry_email = criar_entry(
    frame_cadastro, 
    placeholders[1], 
    0.8, 
    0.08, 
    0.25
    )
entry_telefone = criar_entry(
    frame_cadastro, 
    placeholders[2],
    0.8, 
    0.08, 
    0.4
    )
entry_senha = criar_entry(
    frame_cadastro, 
    placeholders[3], 
    0.8, 
    0.08,
    0.55, 
    mostrar="*"
    )

botao_confirmar = criar_botao(
    frame_cadastro, 
    "Confirmar", 
    lambda: cadastrar(entry_nome, entry_email, entry_telefone, entry_senha), 
    0.8, 
    0.1, 
    0.7, 
    cor_interacao="#1E4D2B" 
    )
botao_sair = criar_botao(
    frame_cadastro, 
    "Sair", 
    lambda: janela_principal.destroy(), 
    0.8, 
    0.1, 
    0.85, 
    cor_interacao="#7C0902"
    )
botao_logar = criar_botao(
    frame_cadastro, 
    "Já tenho conta", 
    logar, 
    0.8, 
    0.07, 
    0.95, 
    cor_fundo="#343A40", 
    relevo="flat")

tk.mainloop()