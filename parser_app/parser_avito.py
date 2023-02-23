from bs4 import BeautifulSoup
import requests

def parser_avito(url):
    page = requests.get(url)
    return page