from bs4 import BeautifulSoup
import requests

class get_proxy():
    best_proxies_ru = 'https://best-proxies.ru/proxylist/free/'

    def test_proxy(self,proxy):
        response = requests.get(
            'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?f=ASgBAgICA0SSA8gQ8AeQUsDBDbr9Nw&localPriority=0&s=104&user=1',
            proxies=proxy
        )
        soup = BeautifulSoup(response.text, 'lxml')
        if soup.find('title').text == 'Доступ ограничен: проблема с IP':
            return False
        else:
            return True

    def get_free_proxy_list_net(self):
        proxies = {}
        response = requests.get('https://free-proxy-list.net/')
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('tbody')
        tr_all = table.find_all('tr')
        for tr in tr_all:
            td_all = tr.find_all('td')
            proxies['http'] = f'http://{td_all[0].text}:{td_all[1].text}'

            if self.test_proxy(proxies):
                print("Найден рабочий прокси: " + proxies['http'])
                return proxies
            else:
                print(f"Прокси {proxies['http']} - проверку не прошёл")
                continue
        return False
        

    def get_best_proxies_ru(self):
        pass

    def manager_get_proxy(self):
        proxy1 = self.get_free_proxy_list_net()





proxy = get_proxy()

proxy.manager_get_proxy()