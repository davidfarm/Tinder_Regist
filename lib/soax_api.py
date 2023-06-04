import random

import requests, configparser

config = configparser.ConfigParser()
config.read('config.ini')
proxy_country = config.get('Settings', 'proxy_country')
proxy_city = config.get('Settings', 'proxy_city')

package_id = '76853'
package_login = 'rUfgRb6QMNgjiLYv'

url = 'http://checker.soax.com/api/ipinfo'

ips_id = ['at', 'au', 'be', 'br', 'ca', 'cz', 'fi', 'fr', 'de', 'it', 'jp',
          'nl', 'pl', 'pt', 'ro', 'es', 'se', 'tr', 'ua', 'gb', 'us'] # 21


def stick(name_id):
    proxy_url = "@proxy.soax.com:5000"
    if proxy_country == "none":
        rand_ips = ips_id[random.randint(0,20)]
        proxy_path_url = f'package-{package_id}-country-{rand_ips}-sessionid-{name_id}-sessionlength-160'
    elif proxy_city == "none" or proxy_city == "":
        proxy_path_url = f'package-{package_id}-country-{proxy_country}-sessionid-{name_id}-sessionlength-160'
    else:
        proxy_path_url = f'package-{package_id}-country-{proxy_country}-city-{proxy_city}-sessionid-{name_id}-sessionlength-160'
    full_url = f"http://{proxy_path_url}:{package_login}{proxy_url}"
    requests.get(url, proxies={'http': full_url, 'https': full_url})

    return proxy_path_url


def proxy(proxy_path_url):
    proxy_host = "proxy.soax.com"
    proxy_type = "SOCKS"
    proxy_username = "rUfgRb6QMNgjiLYv"
    proxy_password = ""
    ports = "5000"

    return proxy_host, proxy_type, proxy_username
