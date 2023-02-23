from bs4 import BeautifulSoup
import requests

def parser_avito(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup