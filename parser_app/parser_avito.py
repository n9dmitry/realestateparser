from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import tzlocal
import pytz
import re

import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image

from multiprocessing import Pool

from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

def get_url_image():
    useragent = UserAgent()
    options = webdriver.FirefoxOptions()

    print('Установка фонового режима...')
    options.headless = True

    print('Отключение режима веб-драйвера')
    options.set_preference('dom.webdriver.enabled', False)
    print('Установка рандомного юзер-агента...')
    options.set_preference('general.useragent.override', useragent.random)

    url = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?f=ASgBAgICA0SSA8gQ8AeQUsDBDbr9Nw&localPriority=0&p=1&s=104&user=1'

    browser = webdriver.Firefox(
    executable_path='/home/denis/Рабочий стол/Projects/celenium/firefoxdriver/geckodriver',
    options=options,
    )   

    browser.get(url)
    print('Нахождение кнопки и нажатие на неё...')
    browser.find_element(By.CLASS_NAME, 'button-button-eBrUW button-button_phone-_Yo3v button-button-CmK9a button-size-s-r9SeD button-default-_Uj_C').click()
    print('Получение ссылки...')
    src = browser.find_element(By.CLASS_NAME, 'button-phone-image-LkzoU').get_attribute('src')

    return src

def get_target_date_ad(ad):

    local_timezone = tzlocal.get_localzone()
    date_now = datetime.now(pytz.utc)

    time = ad.find('div', {'class':'date-text-KmWDf text-text-LurtD text-size-s-BxGpL text-color-noaccent-P1Rfs'}).text
    time_split = time.split(' ')

    if time_split[1] == 'часa' or time_split[1] == 'час' or time_split[1] == 'часов':
        return (date_now - timedelta(hours=int(time_split[0]))).astimezone(local_timezone)
    elif time_split[1] == 'минут':
        return (date_now - timedelta(minutes=int(time_split[0]))).astimezone(local_timezone)
    else:
        return False

# returns: <bool>
def test_ad_on_time(ad):
    time = ad.find('div', {'class':'date-text-KmWDf text-text-LurtD text-size-s-BxGpL text-color-noaccent-P1Rfs'}).text
    time_split = time.split(' ')


    if time_split[1] == 'минут':
        return True
    elif time_split[1] == 'часа' or time_split[1] == 'час' or time_split[1] == 'часов':

        if int(time_split[0]) <= 12:
            return True
        else:
            return False
    else:
        return False


def get_adds(soup):
    res = []
    all_ad = soup.find_all('div', {'class': 'iva-item-content-rejJg'})
    for ad in all_ad:
        res.append(ad)
    return res


def get_data_on_adds(soup):
    res = []

    adds = get_adds(soup)

    for ad in adds:
        if test_ad_on_time(ad):

            date = str(get_target_date_ad(ad))
            url_data = ad.find('a', {'class':'link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH'})['href']
            title = ad.find('h3', {'class':'title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'}).text
            price = ad.find('span', {'class':'price-text-_YGDY'}).text

            appartment_square = re.search(r'\d{1,4},\d м²',ad.find('h3', {'class':'title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'}).text)

            if type(appartment_square) == type(None):

                appartment_square = re.search(r'\d{1,4} м²',ad.find('h3', {'class':'title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'}).text)

            appartment_square = appartment_square[0]

            floors_count = (re.search(r'\/\d{1,3}',ad.find('h3', {'class':'title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'}).text)[0])[-1:]

            appartment_floor = (re.search(r'\d{1,3}\/',ad.find('h3', {'class':'title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'}).text)[0])[:-1]
            marketing_source = 1

            res.append(
                {
                    "date":date,
                    "url_data":url_data,
                    "title":title,
                    "price":price,
                    "appartment_square":appartment_square,
                    "appartment_floor":appartment_floor,
                    "floors_count":floors_count,
                    "marketing_source": marketing_source
                }
                )

    return res

headers = {
    "Accept": "*/*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
}



