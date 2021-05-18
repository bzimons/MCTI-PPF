# AB#24
# 23/03: observação: Site sofreu alteração, código precisa ser reformulado
# 25/03: Link das oportunidades especificas fora do ar
# Definição da função: nomedosite_nº
# 1) Oportunidades, 2) Notícias, 3) Políticas, 4) Projetos
#-------- Bibliotecas utilizadas
import bs4
import requests
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from datetime import datetime
import os

# Função de oportunidade abertas 01
def wellcome1(path,keywords='low- or middle- income country'): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py e as palavras-chaves
  try:
    print('Início função das oportunidades wellcome')
    page = requests.get('https://wellcome.org/grant-funding/schemes') # Request para extrair a página html
    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
    #---------------------------------------------------------------------------------------
    mydivs = soup.findAll("h2", {"class": "cc-text-card__title"}) #definindo aonde queremos extrair
    # titulo = BeautifulSoup(str(mydivs), "html.parser").text # Extraindo os títulos (nomes das grants)
    # titulo = re.sub(r"(\[)|(\])","",titulo) # Removendo os []
    # titulo = titulo.split(" ,") #alguns nomes tem vírgula no meio, então precisa do espaço antes pra não separar esses nomes especificos
    #---------------------------------------------------------------------------------------
    soup2 = BeautifulSoup(str(mydivs),'html.parser') # Criando um novo soup para extrair um sub html só das partes dos links que interessam.
    glinks=[] #lista de links vazia para ser preenchida
    for lk in soup2.find_all('a'):
      glinks.append('https://wellcome.org' + (lk.get('href'))) #preenchendo cada link 'href'
      # print(glinks)

    #---------------------------------------------------------------------------------------
    # criando as listas vazias que se tornarão colunas do dataframe
    brazil=[]
    deadline = []
    cod=[]
    texto=[]
    texto_ele=[]
    tipo=[]
    titulo=[]
    dia = datetime.today().strftime('%y%m%d') #formatação do dia padronizado
    #---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    # looping para entrar em cada link e buscar as informações
    for i in range(0,len(glinks)):
      #---------------------------------------------------------------------------------------
      cod.append('wellcome_'+dia+'_01_'+str("{0:0=3d}".format(i))) #formato de código padronizado, ex de saida: wellcome_210224_01_001
      r = requests.get(glinks[i])
      soup = BeautifulSoup(r.content, 'lxml') #novo soup para cada oportunidade específica
      #titulo
      tit=soup.find("h1", class_="cc-page-title").text
      titulo.append(tit)
      #---------------------------------------------------------------------------------------
      # O titulo já foram extraídos e  tem o mesmo tamanho dos links
      gtit = tit.lower() # Deixar tudo minúscula
      if ('grant' in gtit):         #busca a palavra 'grant' no título
        tipo.append('grant')                #salva a palavra 'grant' no tipo de oportunidade
      elif ('fellowship'in gtit):  #busca a palavra 'fellowship' no título
        tipo.append('fellowship')           #salva a palavra 'fellowship' no tipo de oportunidade
      elif ('scholarship' in gtit): #busca a palavra 'scholarship' no título
        tipo.append('scholarship')          #salva a palavra 'scholarship'' no tipo de oportunidade           
      else:
        tipo.append('other') # caso não encontre o tipo, retorna 'other
      #---------------------------------------------------------------------------------------
      txt = soup.find('main').text #procurando o breve texto
      txt = re.sub("(\n+)","",txt) #excluindo o 'pular linha' extra
      texto.append(txt) # salvando na lista texto

      # TEXO ELEGIIBLIDADE:
      mydivs = soup.findAll("dd", id="eligibility-and-suitability-content")
      soup2 = BeautifulSoup(str(mydivs),'html.parser')
      if 'a' in soup2.text:
        aa = re.sub(r"(\[)|(\])","",soup2.text) #substituindo os colchetes
        aa = re.sub(r"\n+","",aa) #excluindo o 'pular linha' extra
        texto_ele.append(aa)
      else:
        texto_ele.append(txt)
      #--------------------------------------------------------------------------------------- (deadline)
      highlightpage = soup.findAll("li", {"class": "list-highlight__item"}) # pré-definindo um sub HTML para encontrar melhor a info
      soup4 = BeautifulSoup(str(highlightpage),'html.parser') # lendo o sub HTML
      aa = re.sub(r"(\[)|(\])","",soup4.text) #substituindo os colchetes
      aa = re.sub(r"\n+","",aa) #excluindo o 'pular linha' extra
      deadline.append(aa) # salvando o breve texto (informacoes da deadline)
      #---------------------------------------------------------------------------------------
      a = findall(keywords, txt) #procurando as keywords definidas
      if len(a) != 0: #Se encontrar alguma keyword salva Y, caso contrário salva N
        brazil.append("Y")
      else:
        brazil.append("N")
      #-------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------
    # Criação do dataframe com as listas feitas
    # Função que remove a parte "Who can't apply"
    def remove_texto_apos(lista,remocao):
      retorno=[]
      for i in lista:
        removida= i.split(remocao, 1)
        retorno.append(removida[0])
      return(retorno)
    texto_ele = remove_texto_apos(texto_ele, "Who can't apply")

    df = pd.DataFrame({'opo_titulo':titulo,'link':glinks,'opo_brazil':brazil,
    'opo_deadline':deadline,'codigo':cod,'opo_texto':texto,'opo_texto_ele':texto_ele,'opo_tipo':tipo}) 
    df['atualizacao']=[dia]*len(glinks) #criando a variável atualizacao (dia que foi extraido do tamanho dos links)

    # Definindo o path que o arquivo será salvo
    path = path+'''\\wellcome_01.csv''' #padrão de saída do arquivo: nomedosite_numeral.csv
    df.to_csv(path,index=False,sep=",") # salvando o csv
    return(df)
    print('Fim função das oportunidades  wellcome')
  except Exception as e:
    print(e) 
    print("Erro na função wellcome1")

# Função de notícias 02
def wellcome2(path):
  try:
    print('Início função das noticias  wellcome')
    page = requests.get('https://wellcome.org/news/all?&field_article_type[news]=news') # Request para extrair a página html
    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html 
    texto=[]
    for c in soup.find_all('p',class_='tile__description'):
      texto.append(c.text)

    a = soup.find_all('h3')
    soup = BeautifulSoup(str(a),'html.parser')
    nlink=[]
    for a in soup.find_all('a', href=True):
      if len(a['href'])>=20: # número arbitrário, só pra identificar algum links
        nlink.append('https://wellcome.org'+a['href'])
        # print('https://wellcome.org'+a['href'])
    titulo=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')
    for i in range(0,len(nlink)):
      cod.append('wellcome_'+dia+'_02_'+str("{0:0=3d}".format(i))) # codigo indexador padrao: nomedosite_data_nºgrupoextracao_indexador
      page = requests.get(nlink[i]) 
      soup = BeautifulSoup(page.text,'html.parser') # parser que lê o HTML
      b = soup.find('h1').text # procura o título que está na tag <h1>
      # print(b)
      titulo.append(b) 

    df = pd.DataFrame({'not_titulo':titulo,'link':nlink,'not_texto':texto,'codigo':cod}) #criando o dataframe
    df['atualizacao']=[dia]*len(nlink)
    path = path+'''\\wellcome_02.csv'''
    df.to_csv(path,index=False,sep=",")  
    print('Fim função das notícias wellcome')
    return(df)
  except Exception as e:
    print(e) 
    print("Erro na função wellcome2")

    # # Função de políticas 03
def wellcome3(path):
  try:
    print('Início função de política  wellcome')
    def soups(paginas):
      page = requests.get(paginas) # Request para extrair a página html
      soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html 
      a = soup.find('h1',class_="cc-page-title")
      b = soup.find('main')
      return(a.text.encode('utf-8'),b.text.encode('utf-8'))
    pags=['https://wellcome.org/about-us','https://wellcome.org/grant-funding','https://wellcome.org/how-we-work','https://wellcome.org/about-us/strategy']
    nomes=[]
    texto=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')
    for i in range(0,len(pags)):
      elementos = soups(pags[i])
      nomes.append(elementos[0])
      texto.append(elementos[1])
      cod.append('wellcome_'+dia+'_03_'+str("{0:0=3d}".format(i)))
    instituto = ['Wellcome']*len(pags)
    atualizacao = [dia]*len(pags)

    df = pd.DataFrame({'pol_titulo':nomes,'link':pags,'pol_texto':texto,'codigo':cod,'atualizacao':atualizacao,'pol_instituicao':instituto}) 
    path = path+'''\\wellcome_03.csv'''
    df.to_csv(path,index=False,sep=",")  
    print('Fim função de política wellcome')
    return(df)
  except Exception as e:
    print(e) 
    print("Erro na função wellcome3")





