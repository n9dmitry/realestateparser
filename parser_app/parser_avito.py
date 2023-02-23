from bs4 import BeautifulSoup
import requests

def parser_avito(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    allNews = soup.find_all('div',{'class':'iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum'})
    return allNews