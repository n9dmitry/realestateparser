from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import tzlocal
import pytz
import re
import time
import pytesseract
from base64 import b64decode
import os
import traceback
import lxml
from selenium.webdriver.common.keys import Keys 

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent


"""

    Забираем первый пост в самое первой итерации while это можно сделать
    с помощью внешней переменной которая будет обозначать первую итерацию 
    и в конце первой итерации поставить её в False

    Потом просто ожидать 1 минуту и смотреть первый пость время <= 2 минутам
    если пост подходит суем его в res или возвращаем пустой список 

"""

def list_post_formation(ad,id):
        date = get_target_date_ad(ad)
        url_data = ad.find('a', {'class':'link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH'})['href']
        title = ad.find('h3', {'class':'title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'}).text
        price = ad.find('span', {'class':'price-text-_YGDY'}).text
        address = ad.find('div', {'class':'geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL'}).text
        
        marketing_source = 1

        src_image = get_src_image(id, browser)
        saved_image_name = save_img_on_src(src_image, title)
        str_img = read_img(saved_image_name)

        return {
            "date":date,
            "url_data":url_data,
            "title":title,
            "price":price,
            "marketing_source": marketing_source,
            "phone": str_img,
            "address":address
        }
        

def read_img(img_name):
    img_str = pytesseract.image_to_string(img_name)
    os.remove(img_name)
    return img_str

def save_img_on_src(img_src, title_ad):
    header, encoded = img_src.split("base64,", 1)
    data = b64decode(encoded)

    out = open("title_ad.png", 'wb')
    out.write(data)
    out.close()

    return 'title_ad.png'

def get_src_image(target_add_number, browser):

    browser.execute_script(f"document.getElementsByClassName('styles-module-root-_KFFt styles-module-size_s-awPvv styles-module-size_s-_P6ZA styles-module-textAlign_center-bu_u5 stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-s-J4nuX')[{target_add_number}].click()")
    
    time.sleep(5)


    src = browser.execute_script(f'return document.getElementsByClassName("button-phone-image-LkzoU")[{target_add_number}].getAttribute("src")')
    
    return src

def validate_date_ad(ad, newst_title, newst_price):
        title = ad.find('h3', {'class':'title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'}).text
        price = ad.find('span', {'class':'price-text-_YGDY'}).text
        if title != newst_title and price != newst_price:
            print(f"VALIDATE_DATE_AD: TRUE \n NEWST_TITLE:{newst_title} != TITLE_AD:{title} \n NEWST_PRICE:{newst_price} != PRICE_AD:{price}")
            return {"validate": True, 'title':title, 'price':price}
        else:
            print(f"VALIDATE_DATE_AD: FALSE \n NEWST_TITLE:{newst_title} = TITLE_AD:{title} \n NEWST_PRICE:{newst_price} = PRICE_AD:{price}")
            return {"validate": False}
def get_target_date_ad(ad):

    local_timezone = tzlocal.get_localzone()
    date_now = datetime.now(pytz.utc)

    time = ad.find('div', {'class':'date-text-KmWDf text-text-LurtD text-size-s-BxGpL text-color-noaccent-P1Rfs'}).text
    time_split = time.split(' ')

    if time_split[1] == 'часа' or time_split[1] == 'час' or time_split[1] == 'часов':
        return datetime.now() - timedelta(hours=int(time_split[0]))
    elif time_split[1] == 'минут' or time_split[1] == 'минуту' or time_split[1] == 'минуты':
        return datetime.now()- timedelta(minutes=int(time_split[0]))
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
    res.append(all_ad[0])
    return res

def get_data_on_adds(soup, browser, newst_title, news_price):
    browser.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
    adds = get_adds(soup)
    res = []

    for id,ad in enumerate(adds):
            print("\n ITERATION \n")

            # target_ad_date = get_target_date_ad(ad)
            # if newst_entry == '' and target_ad_date:
            #     ad_dict = list_post_formation(ad,id)
            #     if ad_dict:
            #         res.append(ad_dict)
            #         if target_ad_date and id == 0:
            #             print('CHANGE NEWST_ENTRY BECAUSE NEWST ENTRY NULL')
            #             newst_entry = target_ad_date
            #             print('newst_entry' + ' = ' + str(target_ad_date))

            #             continue
                    
            #     else:
            #         print("ID IS OUT OF RANGE")
            #         return [res, newst_entry]
            
            # elif target_ad_date:

            ad_dict = list_post_formation(ad,id)
            # print(str(newst_entry) + ' > ' + str(target_ad_date))
            if ad_dict:
                res.append(ad_dict)
                print("AD IS APPEND IN RES")

                # if target_ad_date:
                #     newst_entry = target_ad_date
                #     print('res append and update newst_entry')
                #     print(newst_entry)
                #     continue
                # else:
                #     print("ID OUT IN RANGE RETURNED RES, NEWST_ENTRY")
                return [res,ad_dict['title'], ad_dict['price']]

            
                # print("target_ad_date - FALSE")
                # return [res, newst_entry]
    # return [res, target_ad_date]

headers = {
    "Accept": "*/*",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'

}

while True:
    try:

        # useragent = UserAgent()
        options = webdriver.FirefoxOptions()

        print('Установка фонового режима...')
        options.headless = True

        print('Отключение режима веб-драйвера')
        options.set_preference('dom.webdriver.enabled', False)

        # print('Установка рандомного юзер-агента...')
        # options.set_preference('general.useragent.override', useragent.random)

        url = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?f=ASgBAgICA0SSA8gQ8AeQUsDBDbr9Nw&localPriority=0&p=1&s=104&user=1'

        newst_title = ''
        newst_price = 0

    
        browser = webdriver.Firefox(
        executable_path='/home/denis/Рабочий стол/Projects/celenium/firefoxdriver/geckodriver',
        options=options,
        )

        browser.get(url)
        print("GLOBAL NEWST TITLE = " + str(newst_title) )
        print("GLOBAL NEWST PRICE = " + str(newst_price) )
        browser.refresh()
        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'lxml')
        print("START PARSE")

        adds = get_data_on_adds(soup, browser, newst_title, newst_price)

        newst_title = adds[1]
        newst_price = adds[2]
        if len(adds[0]) > 0:
            print('ADDS IS NOT CLEAR')
            for ad in adds[0]:
                requests.post('http://127.0.0.1:8000/adds/request_proceed/', data={
                    'date':str(ad['date']),
                    'phone':ad['phone'],
                    'url': ad['url_data'],
                    'title': ad['title'],
                    'price': int(ad['price'].replace('\xa0','')[:-8]),
                    'marketing_source': int(ad['marketing_source']),
                    'address':ad['address']
                    })
                print(f'Add - complate!')
        else:
            print('RES IS CLEAR')
            print(f'NEWST_TITLE: {newst_title}')
            print(f'NEWST_PRICE: {newst_price}')
            browser.close()
            browser.quit()


    except Exception as ex:
        print(traceback.format_exc())

    finally:
        browser.close()
        browser.quit()
        continue