from datetime import datetime
import filecmp 
from filecmp import dircmp
import os
from os import walk
import pandas as pd
import numpy as np 
import shutil
from itertools import compress


# Definindo o diretório para salvar os arquivos
# C:\Users\bolin\Desktop\codigos\mcti-sefip-ppfcd2020\output
# D:\Users\beatriz.simoes\Desktop\codigos\mcti-sefip-ppfcd2020\output
os.chdir(r'C:\Users\bolin\Desktop\codigos\mcti-sefip-ppfcd2020\output')
#-------------------------- Criação da pasta diária -------------------
dia = datetime.today().strftime('%y%m%d') # yy/mm/dd
if os.path.exists(dia):
 print('Diretório já existente')   #nada acontece
else:
    os.makedirs(dia) #cria o diretório 
    print('Diretório criado')


#---------------------------------------------------------------------------
#-------------------- SCRAPING PARA PASTA DIÁRIA:  -------------------------
#---------------------------------------------------------------------------
#  (aqui ficarão as importações dos arquivos py para scraping diário)

# from belmontforum import *
from ICGEB import *
from royalsociety import *
from wellcome import *
from tinker import *
from arcadia import *
from nationalgeographic import *
from simons import *
from cepf import *
from foundationfar import *
from itto import *
from roddenberry import *
from moore import *
from pbnf import *
from fapesp import *
from fundoamazonia import *
from biocodex import *
from fonplata import *
from impact import *
from iadb import *
from thegef import *
from erefdn import *
from funbio import *
from irdc import *
from nfwf import *
from forestgeo import *
from oceaninnovation import *
from tinybeam import *
from globalwomennet import *
from twas import *
from conservegrassland import *
from euraxess import *
from rufford import *


keywords='(low- or middle- income country|brazil|latin american region|member countries of fonplata|developing countries)'

try:
  royal1('.\\'+dia,keywords) #função que importa
  wellcome1('.\\'+dia,keywords)
  icgeb1('.\\'+dia,keywords)
  # belmont1('.\\'+dia,keywords)
  tinker1('.\\'+dia,keywords)
  nationalgeographic1('.\\'+dia,keywords)
  simonsfoundation1('.\\'+dia,keywords)
  cepf1('.\\'+dia,keywords)
  foundationfar1('.\\'+dia,keywords)
  roddenberry1('.\\'+dia,keywords)
  moore1('.\\'+dia,keywords)
  pbnf1('.\\'+dia,keywords)
  fapesp1('.\\'+dia,keywords)
  itto1('.\\'+dia,keywords)
  fonplata1('.\\'+dia,keywords)
  impact1('.\\'+dia,keywords)
  irdc1('.\\'+dia,keywords)
  nfwf1('.\\'+dia,keywords)
  forestgeo1('.\\'+dia,keywords)
  oceaninnovationchallenge1('.\\'+dia,keywords)
  tinybeamfund1('.\\'+dia,keywords)
  globalwomennet1('.\\'+dia,keywords)
  twas1('.\\'+dia,keywords)
  conservegrassland1('.\\'+dia,keywords)
  euraxess1('.\\'+dia,keywords)
  rufford1('.\\'+dia,keywords)
  # royal2('.\\'+dia)
  # simonsfoundation2('.\\'+dia)
  # fundoamazonia2('.\\'+dia)
  # iadb2('.\\'+dia)
  # arcadia2('.\\'+dia)
  # foundationfar2('.\\'+dia)
  # roddenberry2('.\\'+dia)
  # royal3('.\\'+dia)
  # wellcome2('.\\'+dia)
  # wellcome3('.\\'+dia)    
  # icgeb2('.\\'+dia)
  # icgeb3('.\\'+dia)    
  # thegef2('.\\'+dia)
  # thegef3('.\\'+dia)
  # erefdn3('.\\'+dia)
  # arcadia4('.\\'+dia,keywords)
  # fundoamazonia4('.\\'+dia,keywords)
  # iadb4('.\\'+dia,keywords)
  # thegef4('.\\'+dia)
  # tinker4('.\\'+dia)
  # erefdn4('.\\'+dia)
  # funbio4('.\\'+dia)
  # biocodexmicrobiotafundation4('.\\'+dia)
except Exception as e:
  pass
  print('Erro na função')
  print(e) 
  
  


#---------------------------------------------------------------------------
#--------------------------------- Funções  -----------------------------
#---------------------------------------------------------------------------
#--------------- função que define o caminho da pasta------------------
def paths(pasta,arquivo):
  path = '''.\\'''+pasta+'''\\'''+arquivo
  return(path)
#---------------------------------------------------------------------

# --------------------------- função que atualiza a base --------------

# -------------------------------------------------------------------
def atualizador(baseprincipal,diamaisrecente):
  diario = pd.read_csv(diamaisrecente)
  main = pd.read_csv(baseprincipal)
  # checando o que do 'diario' está no 'main'
  x = re.search('03.csv$', baseprincipal) # Se for campo de política, o que é comparado é texto.
  if(x!=None):
    a = diario['pol_texto'].isin(main['pol_texto'])   # usar o tag/id criado inves do link
    b = [not b for b in a] # inverter para o TRUE ser a linha que não tem no main
    novaslinhas = diario[b]
    main = main.append(novaslinhas,ignore_index=True) #novo main
    main.to_csv(baseprincipal,index=False,sep=",")
  elif(diario=="conservegrassland_01.csv"): # Esse site possui os links iguais
    a = diario['opo_texto'].isin(main['opo_texto'])   # usar o tag/id criado inves do link
    b = [not b for b in a] # inverter para o TRUE ser a linha que não tem no main
    novaslinhas = diario[b]
    main = main.append(novaslinhas,ignore_index=True) #novo main
    main.to_csv(baseprincipal,index=False,sep=",")
  else:
    a = diario['link'].isin(main['link'])   # usar o tag/id criado inves do link
    b = [not b for b in a] # inverter para o TRUE ser a linha que não tem no main
    novaslinhas = diario[b]
    main = main.append(novaslinhas,ignore_index=True) #novo main
    main.to_csv(baseprincipal,index=False,sep=",")
#---------------------------------------------------------------------------
#--------------------------------- Comparação  -----------------------------
#---------------------------------------------------------------------------

#------------   pegando todos os diretórios da pasta output

_,dirnames,_  = next(walk('.'))
dirnames.sort(reverse=True) # Os obj 0 vai ser a base principal. o 1 vai ser o dia mais recente e o 2 o dia anterior.
_,_,filenamesDia = next(walk('.\\'+dia)) # Arquivos extraídos no dia.
_,_,filenamesBase = next(walk('.\\baseprincipal')) # Arquivos extraídos na base.

# -------------------------------- Se o arquivo não tiver na base:
# Verificando se os nomes que estão no Dia estão na Base.
a = [i in filenamesBase for i in  filenamesDia]
a = [not b for b in a] # inversão pro True ser o arquivo faltante
arquivos = list(compress(filenamesDia, a)) # arquivo que está faltando na baseprincipal
for f in arquivos:
    shutil.copy('.\\'+dia+'\\'+f, '.\\baseprincipal')
# ------------------------------------------------------


#---------------------------------------------------------------------------
#--------------------------------- Atualização  ----------------------------
#---------------------------------------------------------------------------
filenames = filenamesDia

for i in range(0,len(filenames)):
    try:
        base = str(paths(dirnames[0],filenames[i])) #base 
        dia1 = paths(dirnames[1],filenames[i]) #dia mais recente 
        dia2 = paths(dirnames[2],filenames[i]) #dia anterior 
        x = re.search('03.csv$', dia1) # Se for campo de política, o que é comparado é texto.
        if(x!=None):
          comp = pd.read_csv(dia1)['pol_texto'].isin(pd.read_csv(dia2)['pol_texto']) #Lista boleana comparando os textos das politicas
        elif(dia1=="conservegrassland_01.csv"):
           comp = pd.read_csv(dia1)['opo_texto'].isin(pd.read_csv(dia2)['opo_texto'])
        else:
          comp = pd.read_csv(dia1)['link'].isin(pd.read_csv(dia2)['link']) #Lista boleana comparando os links
        if all(comp)==False: # Verifica se um dos itens da lista de comparação de links é falsa para atualizar
            print('arquivos diários são diferentes, base atualizada')
            atualizador(base,dia1)
        else:
            print('arquivos diários são iguais, base não atualizada')
    except:
      print("Arquivo do dia anterior não encontrado, novo arquivo incluido na base")

    print('Concluido arquivo '+str(i+1))

# como a coluna codigo contem o dia, os arquivos sempre vão ser diferentes.




