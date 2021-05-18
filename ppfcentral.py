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

from wellcome import * #Importa todas as funções

keywords='(low- or middle- income country|brazil|latin american region|member countries of fonplata|developing countries)'

# Executa as funções do código dos sites:
try:
  wellcome1('.\\'+dia,keywords)
  wellcome2('.\\'+dia)
  wellcome3('.\\'+dia)    

except Exception as e:
  pass
  print('Erro na função')
  print(e) 
  

# Funções

#--------------- função que define o caminho da pasta------------------
def paths(pasta,arquivo):
  path = '''.\\'''+pasta+'''\\'''+arquivo
  return(path)


# --------------- função que atualiza a base --------------
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




