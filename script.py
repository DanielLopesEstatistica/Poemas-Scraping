from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_title(soup):
    elements = soup.find_all('h3', {'class':"post-title entry-title"})
    text = elements[0].get_text()
    text = text.replace("\n", "")
    
    return text

def get_poem(soup):
    elements = soup.find_all('div', {'style': 'text-align: justify;'})
    elements += soup.find_all('span', {'style': 'font-family: Georgia, serif;'})

    lista = []

    for element in elements:
        text = element.get_text()
        text = text.replace("\n", " ")
        if text:
            lista.append(text)
        
    lista = lista[:-1]
    return lista



def get_author(soup):
    elements = soup.find_all('b', {'style': 'font-family: Georgia, serif;'})
    text = elements[0].get_text()
    text = text.replace("\n", " ")
    
    return text

def get_source(soup):
    elements = soup.find_all('i', {'style': 'font-family: Georgia, serif;'})
    lista = []
    for element in elements:
        text = element.get_text()
        text = text.replace("\n", " ")
        if text:
            lista.append(text)
        
    resultado = ' '.join(lista)
    return resultado

titulos = []
poemas = []
autores = []
fontes = []

# Configure the webdriver
options = webdriver.FirefoxOptions()
options.headless = True

driver = webdriver.Firefox(options=options)

# Define the URL to scrape
url = "http://rapaduracult.blogspot.com/search/label/Poema?max-results=1"

driver.get(url)

print("Registrando poemas")

for k in range(5000):
    if k%200 == 0:
        print(f"Estamos no poema {k}")
    
    html=driver.page_source
    soup=BeautifulSoup(html)
    
    try:
        titulo = get_title(soup)
    except:
        titulo = "NF"
    
    try:
        poema = get_poem(soup)
    except:
        poema = "NF"
        
    try:
        autor = get_author(soup)
    except:
        autor = "NF"
    
    try:
        fonte = get_source(soup)
    except:
        fonte = "NF"
        
    titulos.append(titulo)
    poemas.append(poema)
    autores.append(autor)
    fontes.append(fonte)
    
    driver.find_element("xpath", "//a[contains(text(),'Postagens mais antigas')]").click()
    
print("Fim")

import pickle

everything_list = [titulos, poemas, autores, fontes]

with open('everything.pickle', 'wb') as f:
    pickle.dump(everything_list, f)
