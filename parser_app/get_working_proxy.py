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

            response = requests.get(
                'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?f=ASgBAgICA0SSA8gQ8AeQUsDBDbr9Nw&localPriority=0&s=104&user=1',
                proxies=proxy,
                headers={'User-Agent':'Mozilla/5.0 (Linux; arm_64; Android 10; MI 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 YaApp_Android/20.90.0 YaSearchBrowser/20.90.0 BroPP/1.0 SA/3 TA/7.1 Mobile '}
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