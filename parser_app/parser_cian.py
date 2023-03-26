from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import tzlocal
import pytz
import re
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from fake_useragent import UserAgent


def get_phone_number(browser, ad):
    browser.execute_script(f"document.getElementsByClassName('_93444fe79c--button--Cp1dl _93444fe79c--button--IqIpq _93444fe79c--XS--Q3OqJ _93444fe79c--button--OhHnj _93444fe79c--full-width--MF714')[0].click()")
    
    time.sleep(5)
    phone_number = browser.execute_script(f'return document.getElementsByClassName("_93444fe79c--color_black_100--kPHhJ _93444fe79c--lineHeight_5u--cJ35s _93444fe79c--fontWeight_bold--ePDnv _93444fe79c--fontSize_14px--TCfeJ _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG")[0].textContent')
    if phone_number != 'null':
        return phone_number
    else:
        return 'Не известен'
def get_target_date_ad(ad):

    local_timezone = tzlocal.get_localzone()
    date_now = datetime.now(pytz.utc)

    time = ad.find('div', {'class':'_93444fe79c--relative--IYgur'}).text
    time_split = time.split(' ')

    if 'час' in time_split[1]:
        return datetime.now() - timedelta(hours=int(time_split[0])) - timedelta(hours=3)
    elif 'мин' in time_split[1]:
        return datetime.now()- timedelta(minutes=int(time_split[0])) - timedelta(hours=3)

def get_adds(soup):
    res = []
    all_ad = soup.find('div', {'class': '_93444fe79c--wrapper--W0WqH'}).find_all('article', {'class': '_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc'})
    res.append(all_ad[0])
    return res

def get_info_post(ad, browser):
    title = ad.find('span', {'class':'_93444fe79c--color_black_100--kPHhJ _93444fe79c--lineHeight_28px--whmWV _93444fe79c--fontWeight_bold--ePDnv _93444fe79c--fontSize_22px--viEqA _93444fe79c--display_block--pDAEx _93444fe79c--text--g9xAG _93444fe79c--text_letterSpacing__normal--xbqP6'})
    url = ad.find('a', {'class':'_93444fe79c--media--9P6wN'})['href']
    price = ad.find('span', {'data-mark':'MainPrice'})
    address = ad.find('div', {'class':'_93444fe79c--labels--L8WyJ'})
    phone = get_phone_number(browser, ad)
    date = get_target_date_ad(ad)

    res = {
        "title": title.text,
        "url": url,
        "price": price.text,
        'address':address.text,
        "marketing_source": 2,
        'date': date,
        'phone':phone
    }
    return res

url = 'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&is_by_homeowner=1&offer_type=flat&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&sort=creation_date_desc&type=4'

page = requests.get(url)


soup = BeautifulSoup(page.text, 'lxml')



options = webdriver.FirefoxOptions()

print('Установка фонового режима...')
options.headless = True

print('Отключение режима веб-драйвера')
options.set_preference('dom.webdriver.enabled', False)

while True:

    try:
        browser = webdriver.Firefox(
                executable_path='/home/denis/Рабочий стол/Projects/celenium/firefoxdriver/geckodriver',
                options=options,
                )

        browser.get(url)
        
        browser.refresh()
        
        ad = get_info_post(get_adds(soup)[0], browser)
        print(ad)
        requests.post('http://127.0.0.1:8000/adds/request_proceed/', data={
        'date':str(ad['date']),
        'phone':ad['phone'],
        'url': ad['url'],
        'title': ad['title'],
        'price': int(ad['price'][:-7].replace(' ','')),
        'marketing_source': int(ad['marketing_source']),
        'address':ad['address']
        })
        print(f'Add - complate!')
    except Exception as ex:
        print(traceback.format_exc())
    finally:
        browser.close()
        browser.quit()
        continue