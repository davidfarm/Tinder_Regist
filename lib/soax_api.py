import configparser, random, re, requests
from core.logger import log_dispatcher
from lib.proxy_preference import check_proxy, url

config = configparser.ConfigParser()
config.read('config.ini')
proxy_country = config.get('Settings', 'proxy_country')
proxy_city = config.get('Settings', 'proxy_city')

package_id = '76853'
package_login = 'AdrYQGEGnB2E9I7m'

ips_id = ['at', 'au', 'be', 'br', 'ca', 'cz', 'fi', 'fr', 'de', 'it', 'jp',
          'nl', 'pl', 'pt', 'ro', 'es', 'se', 'tr', 'ua', 'gb', 'us']  # 21


def stick(name_id):
    proxy_url = "@proxy.soax.com:5000"

    def get_proxy_path():
        if proxy_country == "none":
            rand_ips = ips_id[random.randint(0, 20)]
            proxy_path_url = f'package-{package_id}-country-{rand_ips}-sessionid-{name_id}-sessionlength-160'
        elif proxy_city == "none" or proxy_city == "":
            proxy_path_url = f'package-{package_id}-country-{proxy_country}-sessionid-{name_id}-sessionlength-160'
        else:
            proxy_path_url = f'package-{package_id}-country-{proxy_country}-city-{proxy_city}-sessionid-{name_id}-sessionlength-160'
        return proxy_path_url

    proxy_path_url = get_proxy_path()
    full_url = f"http://{proxy_path_url}:{package_login}{proxy_url}"
    print('Check proxy ...')

    if not check_proxy(full_url):

        for i in range(4):
            pattern = r'A-\d+$'

            if re.search(pattern, name_id):
                name_id = name_id[:-1] + str(int(name_id[-1]) + 1)
            else:
                name_id += 'A-1'

            get_proxy_path()
            full_url = f"http://{proxy_path_url}:{package_login}{proxy_url}"

            if check_proxy(full_url):
                break
            msg = 'Ошибка создания проски -_-'
            log_dispatcher.info(to_print=msg, to_write=msg, msg_type='error')

            if i == 3:
                msg = 'Не удалось создать прокси'
                log_dispatcher.info(to_print=msg, to_write=msg, msg_type='error')
                raise ValueError('Proxys is not a valid')

    requests.get(url, proxies={'http': full_url, 'https': full_url})

    return proxy_path_url


def proxy(proxy_path_url):
    proxy_host = "proxy.soax.com"
    proxy_type = "SOCKS"
    proxy_username = "AdrYQGEGnB2E9I7m"
    proxy_password = ""
    ports = "5000"

    return proxy_host, proxy_type, proxy_username
