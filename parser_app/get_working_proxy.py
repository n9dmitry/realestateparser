from bs4 import BeautifulSoup
import requests
import time

class get_proxy():
    best_proxies_ru = 'https://best-proxies.ru/proxylist/free/'
    
    def get_random_user_agents(self, count):
        user_agents = []
        response = requests.post(
            'https://user-agents.net/random',
            data={'limit':str(count), 'action':'generate'},
            
        )
        
        soup = BeautifulSoup(response.text, 'lxml')
        for li in soup.find('article').find('div').find('ol').find_all('li'):
            user_agents.append(li.find('a').text)
        
        return user_agents

    def test_proxy(self,proxy):
        for userAgent in self.get_random_user_agents(5):
            response = requests.get(
                'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?f=ASgBAgICA0SSA8gQ8AeQUsDBDbr9Nw&localPriority=0&s=104&user=1',
                proxies=proxy,
                headers={'User-Agent':userAgent}
            )
            soup = BeautifulSoup(response.text, 'lxml')
            if soup.find('title').text == 'Доступ ограничен: проблема с IP':
                continue
            else:
                return True
            
        return False

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
                time.sleep(4)
                return proxies
            else:
                print(f"Прокси {proxies['http']} - проверку не прошёл")
                time.sleep(4)
                continue
        return False
        

    def get_best_proxies_ru(self):
        pass

    def manager_get_proxy(self):
        proxy1 = self.get_free_proxy_list_net()


proxy = get_proxy()
proxy.get_free_proxy_list_net()