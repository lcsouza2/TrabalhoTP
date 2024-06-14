import subprocess
import tkinter as tk
import tkinter.ttk as ttk
import json
from typing import Callable
from tkinter import messagebox

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

def logar():
    try:
        with open("TRABALHOTP2\\registros.json", "r+") as ler_json: #Tenta abrir o json
            try:
                dados_no_json = json.load(ler_json) #Tenta ler o json
            
            except json.JSONDecodeError: #Executa caso o arquivo esteja vazio
                messagebox.showwarning("Sem usuários", "O arquivo de registros está vazio, cadastre-se antes")
                janela_principal.destroy()
                subprocess.run(["python", "TRABALHOTP2\\codigos\\Cadastro.py"])
                return
            
    except FileNotFoundError: #Executa caso o arquivo não exista 
        messagebox.showwarning("Sem usuários", "O arquivo de registros está vazio, cadastre-se antes")
        janela_principal.destroy()
        subprocess.run(["python", "TRABALHOTP2\\codigos\\Cadastro.py"])

    else: #Executa caso não haja erros 
        with open("TRABALHOTP2\\registros.json", "w") as regravar:
            dados_regravar=[]
            encontrado = False
            for i in dados_no_json:
                if (i["Nome"] == entry_nome.get() and
                    i["Senha"] == entry_senha.get()):
                    i["Logado"] = True
                    encontrado = True
                dados_regravar.append(i)
            json.dump(dados_regravar, regravar, indent=4)

        if not encontrado:
            messagebox.showerror("Dados inválidos", 
                                "Os dados digitados estão incorretos, confira-os e tente novamente")
        else:
            messagebox.showinfo("Sucesso!", "Estamos te redirecionando!")
            janela_principal.destroy()
            subprocess.run(["python", "TRABALHOTP2\\codigos\\Principal.py"])

def trocar_senha():
    popup_trocar_senha = tk.Toplevel(janela_principal, bg="#343A40")
    popup_trocar_senha.geometry("300x170")
    popup_trocar_senha.iconbitmap("TRABALHOTP2\\icones\\change_pwd_icon.ico")
    popup_trocar_senha.resizable(False, False)

    nome_entry = criar_entry(
        popup_trocar_senha, 
        "Digite seu nome", 
        0.6, 
        0.15, 
        0.1
    )
    senha_entry = criar_entry(
        popup_trocar_senha,
        "Digite sua nova senha",
        0.6,
        0.15,
        0.3,
        mostrar="*"
    )

    def confirmar():
        try:
            with open("TRABALHOTP2\\registros.json", "r+") as ler_json: #Tenta abrir o json
                try:
                    dados_no_json = json.load(ler_json) #Tenta ler o json
                
                except json.JSONDecodeError: #Executa caso o arquivo esteja vazio
                    messagebox.showwarning("Sem usuários", "O arquivo de registros está vazio, cadastre-se antes")
                    janela_principal.destroy()
                    subprocess.run(["python", "TRABALHOTP2\\codigos\\Cadastro.py"])
                    return
                
        except FileNotFoundError: #Executa caso o arquivo não exista 
            messagebox.showwarning("Sem usuários", "O arquivo de registros está vazio, cadastre-se antes")
            janela_principal.destroy()
            subprocess.run(["python", "TRABALHOTP2\\codigos\\Cadastro.py"])

        else: #Executa caso não haja erros 
            encontrado = False
            with open("TRABALHOTP2\\registros.json", "w") as regravar:
                dados_regravar=[]

                for i in dados_no_json:
                    if i["Nome"] == nome_entry.get():
                        encontrado = True
                        i["Senha"] = senha_entry.get()
                        messagebox.showinfo("Sucesso", "senha alterada!")
                        popup_trocar_senha.destroy()

                    dados_regravar.append(i)
                json.dump(dados_regravar, regravar, indent=4)
            if encontrado is False:
                messagebox.showwarning("Cadastro não encontrado", "O cadastro informado não foi encontrado, verifique os dados!")
                        
    botao_confirmar = criar_botao(
        popup_trocar_senha, 
        "Confirmar", 
        confirmar, 
        0.4, 
        0.15, 
        0.6, 
        0.45, 
        "e", 
        cor_interacao="#1E4D2B"
    )
    botao_cancelar = criar_botao(
        popup_trocar_senha,
        "Cancelar",
        lambda: popup_trocar_senha.destroy(),
        0.4, 
        0.15,
        0.6, 
        0.55,
        "w",
        cor_interacao="#7C0902" 
)

janela_principal = tk.Tk()
janela_principal.title("Login")
janela_principal.geometry("280x350")
janela_principal.resizable(False, False)
janela_principal.iconbitmap("TRABALHOTP2\\icones\\login_icon.ico")
janela_principal["bg"] = "#212529"

frame_login = tk.Frame(
    janela_principal, 
    padx = 10,
    pady = 10, 
    bg = "#343A40"
    )
frame_login.place(
    anchor = "center", 
    relx = 0.5, 
    rely = 0.5, 
    relheight = 0.8, 
    relwidth = 0.8
    )

entry_nome = criar_entry(
    frame_login,
    "Digite seu nome",
    0.8,
    0.08,
    0.1,
)
entry_senha = criar_entry(
    frame_login,
    "Digite sua senha",
    0.8,
    0.08,
    0.25,
    mostrar="*"
)

botao_confirmar = criar_botao(
    frame_login,
    "Entrar",
    logar,
    0.8,
    0.1,
    0.8,
    cor_interacao="#1E4D2B",
    )
botao_cancelar = criar_botao(
    frame_login,
    "Cancelar",
    lambda: janela_principal.destroy(),
    0.8,
    0.1,
    0.95,
    cor_interacao="#7C0902")
botao_trocar_senha = criar_botao(
    frame_login,
    "Esqueci minha senha",
    trocar_senha,
    0.8,
    0.1,
    0.35,
    cor_fundo="#343A40",
    cor_texto="lightblue",
    relevo="flat"
)


tk.mainloop()