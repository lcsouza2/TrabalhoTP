import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from typing import Callable

with open("TRABALHOTP2\\registros.json", "r") as f:
    users=[]
    for i in json.load(f):
        users.append(i)
        if i["Logado"] is True:
            i["Logado"] = False #Determina o estado de login como false
            arquivo_json= f"TRABALHOTP2\\dados\\"+i["Nome"]+".json" #Determina o arquivo do usuário
            
            try:
                with open(arquivo_json, "r") as file_read:
                    try:
                        json.load(file_read)
                    except json.JSONDecodeError: #Exceção para arquivo vazio 
                        with open(arquivo_json, "w") as file_write:
                            json.dump([], file_write)
            except FileNotFoundError: #Exceção arquivo inexistente 
                with open(arquivo_json, "w") as file_write:
                            json.dump([], file_write)

with open("TRABALHOTP2\\registros.json", "w") as file:
    json.dump(users, file, indent=4)


def ler_json():
    try:
        with open(arquivo_json, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError: #Arquivo vazio
                return []
    except FileNotFoundError: #Arquivo inexistente
        with open(arquivo_json, "w"):
            return []   

def regravar_json(dados_antigos, dados_adicionar):
    with open(arquivo_json, "w") as file:
        dados_antigos.append(dados_adicionar)
        json.dump(dados_antigos, file, indent=4)


def carregar_imagem(caminho):
    #Carrega a imagem e adapta para o tkinter

    img = Image.open(caminho)
    img = ImageTk(img)
    return img

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
    entry.place(
        relwidth=largura, 
        relheight=altura, 
        rely=pos_y, 
        relx=pos_x, 
        anchor=ancora
    )
    
    def entry_clicado(evento):
        """Remove o texto de dentro do entry quando clicado"""

        if entry.get() == placeholder:
            entry.delete(0, "end") 
            entry.insert(0, "")
            entry["show"]=mostrar
            entry["foreground"]="Black"
            entry["justify"]="left"   

    def entry_padrao(evento):
        """Adiciona o texto caso o widget esteja em branco depois de clicado"""

        if entry.get() == "":
            entry.insert(0, placeholder)
            entry["show"]=""
            entry["foreground",]="#495057"
            entry["justify"]="center"
    
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

    botao.place(
    relwidth=largura, 
    relheight=altura, 
    rely=pos_y, 
    relx=pos_x, 
    anchor=ancora
    )
    
    def mouse_in(evento):
        botao["bg"] = cor_interacao

    def mouse_out(evento):
        botao["bg"] = cor_fundo

    botao.bind("<Enter>", mouse_in)
    botao.bind("<Leave>", mouse_out)

def entry_valido(entry, placeholder):
    digitado = entry.get()
    return digitado and digitado.strip() and digitado != placeholder

def atualizar_tabela():
    for i in tabela.get_children():
        tabela.delete(i)

    with open(arquivo_json, "r") as arq_eventos:
        try:
            for i in json.load(arq_eventos):
                tabela.insert("", "end", values=(i["Descricao"], i["Data"], i["Hora"]))
        except json.JSONDecodeError:
            return []

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
    popup_add_evento.iconbitmap("TRABALHOTP2\\icones\\add_event_icon.ico")

    #Frame para posicionar os widgets
    frame_add_evento = tk.Frame(popup_add_evento)
    frame_add_evento.place(
        anchor="center",
        relheight=0.9,
        relwidth=0.8,
        relx=0.5,
        rely=0.5
    )

    #Label para posicionar a imagem
    image_add_evento = tk.Label(
        frame_add_evento, 
        image=carregar_imagem("TRABALHOTP2\\imagens\\frame_add_event.png")
    )
    image_add_evento.place(anchor="center", relheight=1, relwidth=1, relx=0.5, rely=0.5)
    
    #Mantém a imagem para evitar ela de ser excluída pelo garbage collector
    image_add_evento.image=carregar_imagem("TRABALHOTP2\\imagens\\frame_add_event.png")

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

    def confirmar():
        if (entry_valido(descricao, "Digite a descrição do evento") and 
            entry_valido(data, "Digite a data do evento") and 
            entry_valido(hora, "Digite a hora do evento")):
            
            #Dados para salvar
            evento = {
            "Descricao" : descricao.get(),
            "Data" : data.get(),
            "Hora" : hora.get()
            }
        else:
            messagebox.showerror("Erro!", "Preencha todos os campos corretamente")
            return
        
        duplicado = False

        dados_no_json = ler_json()
        
        for i in dados_no_json:
            if (i["Descricao"] == evento["Descricao"] and 
                i["Data"] == evento["Data"]): #Checa se os dados existem se sim duplicado é verdadeiro
                duplicado = True
                check = messagebox.askyesno(
                    "O evento já existe!", #Título
                    "O evento já existe na sua agenda, deseja adicionar mesmo assim?" #Mensagem
                ) 
                if check is True: #Se o usuário selecionar sim no check executa
                    regravar_json(dados_no_json, evento)
                    messagebox.showinfo("Feito!", "Evento adicionado com sucesso")
                    popup_add_evento.destroy()
                    return
                else:
                    popup_add_evento.destroy()
                    return
                        
        if duplicado is False: #Executado se os dados não existirem no arquivo
            regravar_json(dados_no_json, evento)
            messagebox.showinfo("Feito!", "Evento adicionado com sucesso")
            popup_add_evento.destroy()
    
    botao_confirmar = criar_botao(
        frame_add_evento,
        "Confirmar",
        confirmar, 
        0.8, #% largura
        0.07, #% altura
        0.7, #% pos_y
        cor_interacao="#1E4D2B"
    )
    botao_cancelar = criar_botao(
        frame_add_evento,
        "Cancelar",
        lambda:popup_add_evento.destroy(),
        0.8, #% largura
        0.07, #% altura
        0.85, #% pos_y
        cor_interacao="#7C0902"
    )

def remover_evento():
    """
    Função:
        Usa os dados no entry para remover um evento
    """

    #Configurações do Pop-Up
    popup_rem_evento = tk.Toplevel(bg="#212529")
    popup_rem_evento.geometry("400x250")
    popup_rem_evento.resizable(False, False)
    popup_rem_evento.title("Remover evento")
    popup_rem_evento.iconbitmap("TRABALHOTP2\\icones\\remove_event_icon.ico")

    #Frame para posicionar os widgets
    frame_rem_evento = tk.Frame(
        popup_rem_evento
    )
    frame_rem_evento.place(
        anchor="center",
        relheight=0.79,
        relwidth=0.79,
        relx=0.5,
        rely=0.5
    )

    #Carrega a imagem e adapta para o tkinter
    img_rem_evento = Image.open("TRABALHOTP2\\imagens\\frame_rem_event.png")
    img_rem_evento = ImageTk.PhotoImage(img_rem_evento)

    #Label para posicionar a imagem
    image_rem_evento = tk.Label(
        frame_rem_evento, 
        image=img_rem_evento
    )
    image_rem_evento.place(anchor="center", relheight=1, relwidth=1, relx=0.5, rely=0.5)
    
    #Mantém a imagem para evitar ela de ser excluída pelo garbage collector
    image_rem_evento.image=img_rem_evento

    def carregar_eventos():
        eventos = [] 

        for i in ler_json():
            eventos.append(i["Descricao"]) 
        return eventos              

    #Combobox para mostrar os eventos
    menu_eventos = ttk.Combobox(
        frame_rem_evento, 
        values=carregar_eventos(), 
        state="readonly", 
        width=35
    )
    menu_eventos.place(anchor="center", rely=0.1, relx=0.5)
    
    def remover_evento():
        confirm = messagebox.askyesno("Certeza?", "Deseja mesmo remover esse evento?")
        
        dados = ler_json()

        if confirm is True:
            for i in dados:
                if i["Descricao"] == menu_eventos.get():
                    dados.remove(i)
                    with open(arquivo_json, "w") as f:
                        json.dump(dados, f, indent=4)
                    messagebox.showinfo("Feito!", "O evento foi removido com sucesso")
                    menu_eventos["values"] = carregar_eventos()
            popup_rem_evento.destroy()

    botao_confirmar = criar_botao(
        frame_rem_evento, 
        "Excluir", 
        remover_evento, 
        0.5,
        0.1,
        0.8,
        0.5,
    )

def alterar_evento():
    #Configurações do Pop-Up
    popup_alt_evento = tk.Toplevel(bg="#212529")
    popup_alt_evento.geometry("250x400")
    popup_alt_evento.resizable(False, False)
    popup_alt_evento.title("Alterar evento")
    popup_alt_evento.iconbitmap("TRABALHOTP2\\icones\\change_pwd_icon.ico")
    
    frame_alt_evento = tk.Frame(
        popup_alt_evento
    )
    frame_alt_evento.place(
        anchor="center",
        relheight=0.79,
        relwidth=0.79,
        relx=0.5,
        rely=0.5
    )

    #Carrega a imagem e adapta para o tkinter
    img_alt_evento = Image.open("TRABALHOTP2\\imagens\\frame_alt_event.png")
    img_alt_evento = ImageTk.PhotoImage(img_alt_evento)

    #Label para posicionar a imagem
    image_alt_evento = tk.Label(
        frame_alt_evento, 
        image=img_alt_evento
    )
    image_alt_evento.place(anchor="center", relheight=1, relwidth=1, relx=0.5, rely=0.5)
    
    #Mantém a imagem para evitar ela de ser excluída pelo garbage collector
    image_alt_evento.image=img_alt_evento

    def carregar_eventos():
        eventos = [] 

        for i in ler_json():
            eventos.append(i["Descricao"]) 
        return eventos   

    combobox_eventos = ttk.Combobox(
        frame_alt_evento, 
        values=carregar_eventos(), 
        state="readonly"
    )
    combobox_eventos.place(anchor="center", rely=0.1, relx=0.5)

    entry_descricao = criar_entry(
        frame_alt_evento,
        "",
        0.8,
        0.1,
        0.3
    )
    entry_data = criar_entry(
        frame_alt_evento,
        "",
        0.8,
        0.1,
        0.45
    )
    entry_hora = criar_entry(
        frame_alt_evento,
        "",
        0.8,
        0.1,
        0.6
    )

    def atualizar_placeholders(evento):
        for i in ler_json():
            if i["Descricao"] == combobox_eventos.get():
                entry_descricao.delete(0, "end")
                entry_descricao.insert(0, i["Descricao"])
                entry_data.delete(0, "end")
                entry_data.insert(0, i["Data"])
                entry_hora.delete(0, "end")
                entry_hora.insert(0, i["Hora"])
                break


    combobox_eventos.bind("<<ComboboxSelected>>", atualizar_placeholders)

    def confirmar():
        dados = []
        for i in ler_json():
            if i["Descricao"] == combobox_eventos.get():
                i["Descricao"]=entry_descricao.get()
                i["Data"]=entry_data.get()
                i["Hora"]=entry_hora.get()
            dados.append(i)    
        
        with open(arquivo_json, "w") as f:
            json.dump(dados, f, indent = 4)
        combobox_eventos["values"] = carregar_eventos()
        messagebox.showinfo("Sucesso!", "O evento foi alterado!")
        popup_alt_evento.destroy()

    botao_confimrar = criar_botao(
        frame_alt_evento,
        "Confirmar",
        confirmar,
        0.8,
        0.08,
        0.9
    )

#Configurações da janela principal
janela_principal = tk.Tk()
janela_principal.geometry("820x400")
janela_principal.resizable(False, False)
janela_principal.iconbitmap("TRABALHOTP2\\icones\\home_icon.ico")
janela_principal.configure(background="#212529", )

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
    image=carregar_imagem("TRABALHOTP2\\imagens\\frame_botoes.png"), 
    highlightthickness=0
)
imagem_botoes.place(relheight=1, relwidth=1)

botao_att_tabela = criar_botao(
    frame_botoes,
    "Atualizar tabela",
    atualizar_tabela,
    0.8, #% comprimento
    0.08, #% largura
    0.45 #% altura
)
botao_add_evento = criar_botao(
    frame_botoes,
    "Adicionar evento",
    adicionar_evento,
    0.8,  #% comprimento
    0.08,  #% largura
    0.6, #% altura
)
botao_rem_evento = criar_botao(
    frame_botoes,
    "Remover evento",
    remover_evento,
    0.8, #% comprimento
    0.08, #% largura
    0.75, #% altura
)
botao_alt_evento = criar_botao(
    frame_botoes,
    "Alterar evento",
    alterar_evento,
    0.8, #% comprimento 
    0.08, #% largura
    0.9 #% altura
)

#Linha no meio da tela 
linha_separar = ttk.Separator(janela_principal, orient="vertical")
linha_separar.place(x=250, relheight=1)

#Frame para posicionar a tabela
frame_grade = ttk.Frame(
    janela_principal,
    width=503,
    height=365,
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
    image=carregar_imagem("TRABALHOTP2\\imagens\\frame_tabela.png"), 
    highlightthickness=0
)
imagem_grade.place(relheight=1, relwidth=1)

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
atualizar_tabela()
tk.mainloop()