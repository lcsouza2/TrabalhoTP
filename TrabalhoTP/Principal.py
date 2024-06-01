import random
import json
import string
from faker import Faker
fake = Faker(["pt_BR"])
import unidecode

  
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

#Carrega os dados no Json {
def LoadJson(ArquivoJson):
  try:
    with open(ArquivoJson, "r") as Arquivo:
      DadosNoJson = json.load(Arquivo)
    return DadosNoJson
  
  #Caso o arquivo esteja vazio
  except json.JSONDecodeError:
    return []
  
  # Caso o arquivo não exista:
  except FileNotFoundError:
    return []
#Carrega os dados no Json }

#Adiciona um aluno no json {
def AddAluno(nome):
  
  Dados = {
    "Nome" : nome, 
    "Matricula" : GerarMatricula()
  }
  
  #Carrega o Json
  DadosJaGravados = LoadJson("Registros.json")
  DadosJaGravados.append(Dados)

  #Grava os dados formatados
  with open("Registros.json", "w") as arquivo:
    json.dump(DadosJaGravados, arquivo, indent = 4)
#Adiciona um aluno no json }

#Remover aluno dos registros {
def RemAluno():
  
  #Abre o arquivo e lê os dados
  AlunosExistentes = LoadJson("Registros.json")

def FalsificarNome():
  for i in range(5):
    NomeFalso = fake.name()
    AddAluno(unidecode.unidecode(NomeFalso))

FalsificarNome()
