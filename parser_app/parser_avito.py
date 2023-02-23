from bs4 import BeautifulSoup
import requests

def parser_avito(url):
    headers = {
        "Accept": "*/*",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
    }

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup