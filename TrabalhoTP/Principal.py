import random
import json
import string


#Gera uma matrícula aleatória {
def GerarMatricula():  

  NovaMatricula = ""
  
  for i in range(0,6): #Numero de caracteres
    
    i = random.choice([0,1])
    
    match i: #Sorteia se vai ser adicionado letra ou número na matrícula
      case 0:
        NovaMatricula += str(random.randint(0,10))
      case 1: 
        NovaMatricula += random.choice(string.ascii_uppercase)

  return NovaMatricula 
#}


#Adiciona um aluno no json {
def AddAluno(nome):
  
  Dados = {
    "Nome" : nome, 
    "Matricula" : GerarMatricula()
  }
   
  DadosARegistrar = json.dumps(Dados, indent= 2) 


  with open("Registros.json", "a+") as RegistrosAddAluno:
    if RegistrosAddAluno.tell() > 0:
      RegistrosAddAluno.write(",\n")
    RegistrosAddAluno.write(DadosARegistrar)

#}

#Remover aluno dos registros {
def RemAluno(dados):
  
  #Abre o arquivo e lê os dados
  with open("Registros.json", "r") as RegistrosRemAluno: 
    AlunosExistentes = json.load(RegistrosRemAluno)

  #Checa se os dados existem no json
  if dados in AlunosExistentes:
    del AlunosExistentes[dados]

  #Regrava os dados sem o registro a excluir
  with open("Registros.json", "w") as RegravarAlunos:
    RegravarAlunos.write(AlunosExistentes)


  